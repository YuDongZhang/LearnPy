"""
11. 投机解码与多Token预测 (MTP) - 代码示例
自回归解码每步只产1个token且必须跑完整模型, decode阶段GPU严重吃不饱
(Mamba-3称之为"冷GPU"问题)。
投机解码 (Speculative Decoding): 小draft模型起草k个, 大target模型
一次前向同时验证 → 无损加速 (vLLM/SGLang等推理框架已标配)。
MTP (Multi-Token Prediction): DeepSeek-V3/Nemotron 3 训练时同时预测
未来多个token, 推理时MTP头就是"原生草稿", 免掉独立draft模型。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# ============================================================
# 1. 紧凑因果LM (target/draft共用, 靠层数区分大小)
# ============================================================
class CausalAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):
        B, T, C = x.shape
        Q, K, V = self.qkv(x).chunk(3, dim=-1)
        Q = Q.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        mask = torch.tril(torch.ones(T, T, device=x.device))
        scores = scores.masked_fill(mask == 0, float('-inf'))
        out = F.softmax(scores, dim=-1) @ V
        return self.proj(out.transpose(1, 2).contiguous().view(B, T, C))


class Block(nn.Module):
    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalAttention(d_model, num_heads)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model))

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        return x + self.ffn(self.ln2(x))


class MiniLM(nn.Module):
    """返回 (logits, hidden), hidden供MTP头复用"""

    def __init__(self, vocab_size, d_model=64, num_heads=4, n_layers=2, d_ff=128, max_len=64):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList([Block(d_model, num_heads, d_ff) for _ in range(n_layers)])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx):
        T = idx.size(1)
        x = self.token_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.head(x), x


class MTPHead(nn.Module):
    """DeepSeek-V3式MTP模块: 预测t+2。
    输入 = 主模型hidden(t) ⊕ emb(t+1) → 投影 → 额外block → 输出头。
    训练时t+1用ground truth (teacher forcing); 推理时用主头的预测。"""

    def __init__(self, d_model, vocab_size, num_heads, d_ff):
        super().__init__()
        self.combine = nn.Linear(2 * d_model, d_model, bias=False)
        self.block = Block(d_model, num_heads, d_ff)
        self.head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, h, emb_next):
        return self.head(self.block(self.combine(torch.cat([h, emb_next], dim=-1))))


# ============================================================
# 2. 训练 (循环序列: next = 周期表中的下一个 → 确定性, 小模型能学满)
# ============================================================
def train_lm(model, x, y, mtp=None, steps=400, lr=3e-3):
    params = list(model.parameters()) + (list(mtp.parameters()) if mtp else [])
    opt = torch.optim.Adam(params, lr=lr)
    model.train()
    for _ in range(steps):
        logits, h = model(x)
        V = logits.size(-1)
        loss = F.cross_entropy(logits.reshape(-1, V), y.reshape(-1))
        if mtp is not None:
            # MTP: 位置t (h[:, :-1]) + 正确的t+1 → 预测t+2 (y[:, 1:])
            mtp_logits = mtp(h[:, :-1], model.token_emb(y[:, :-1]))
            loss = loss + F.cross_entropy(mtp_logits.reshape(-1, V), y[:, 1:].reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()


@torch.no_grad()
def accuracy(model, x, y):
    logits, _ = model(x)
    return (logits.argmax(-1) == y).float().mean().item()


@torch.no_grad()
def mtp_accuracy(model, mtp, x, y):
    _, h = model(x)
    pred = mtp(h[:, :-1], model.token_emb(y[:, :-1])).argmax(-1)
    return (pred == y[:, 1:]).float().mean().item()


# ============================================================
# 3. 三种生成方式
# ============================================================
@torch.no_grad()
def naive_generate(model, idx, n_tokens):
    """朴素解码: n个token = n次完整前向"""
    passes = 0
    for _ in range(n_tokens):
        logits, _ = model(idx)
        passes += 1
        idx = torch.cat([idx, logits[:, -1:].argmax(-1)], dim=1)
    return idx, passes


@torch.no_grad()
def speculative_generate(target, draft, idx, n_tokens, k=4):
    """投机解码 (贪心版, 对贪心解码无损):
    1) draft连写k个候选 (draft小, 前向便宜)
    2) target对 [x+候选] 一次前向, 同时验证全部k个
    3) 接受最长正确前缀; 全对时附赠target自己的下一个token
    (采样模式的完整算法用拒绝采样保证分布一致, 见md)
    返回: 序列, target前向次数, 接受率"""
    x = idx
    target_passes = 0
    n_accepted = n_rounds = 0
    while x.size(1) - idx.size(1) < n_tokens:
        # 1) 起草
        dx = x
        proposals = []
        for _ in range(k):
            d_logits, _ = draft(dx)
            nxt = d_logits[:, -1:].argmax(-1)
            proposals.append(nxt)
            dx = torch.cat([dx, nxt], dim=1)
        prop = torch.cat(proposals, dim=1)              # (1, k)
        # 2) 一次验证
        logits, _ = target(dx)
        target_passes += 1
        greedy = logits[:, -k - 1:-1].argmax(-1)        # 各候选位置的target贪心token
        match = (greedy == prop)[0].tolist()
        n_acc = match.index(0) if 0 in match else k
        n_rounds += 1
        n_accepted += n_acc
        # 3) 接受前缀 + 修正 (全对时bonus)
        if n_acc == k:
            bonus = logits[:, -1:].argmax(-1)
            x = torch.cat([x, prop, bonus], dim=1)      # k+1个token, 1次target前向!
        else:
            fixed = greedy[:, n_acc:n_acc + 1]
            x = torch.cat([x, prop[:, :n_acc], fixed], dim=1)
    return x[:, :idx.size(1) + n_tokens], target_passes, n_accepted / max(n_rounds * k, 1)


@torch.no_grad()
def mtp_generate(model, mtp, idx, n_tokens):
    """MTP自投机 (k=1): 每次前向 = 主头出1个token + 顺带验证上轮MTP押注。
    押对: 每次前向产2个token (≈2x); 押错: 修正后只得1个。
    免掉独立draft模型 —— Nemotron 3的"原生投机解码"。"""
    x = idx
    passes = 0
    logits, h = model(x)
    passes += 1
    nxt = logits[:, -1:].argmax(-1)                      # 主头: t+1
    prop = mtp(h[:, -1:], model.token_emb(nxt)).argmax(-1)  # MTP押注: t+2
    x = torch.cat([x, nxt, prop], dim=1)                 # 末位是待验证押注
    committed = 1                                        # 已确认的生成token数

    while committed < n_tokens:
        logits, h = model(x)
        passes += 1
        verify = logits[:, -2:-1].argmax(-1)             # target对押注位置的预测
        if torch.equal(verify, x[:, -1:]):               # 押对: 转正+主头再出1个
            nxt2 = logits[:, -1:].argmax(-1)
            prop2 = mtp(h[:, -1:], model.token_emb(nxt2)).argmax(-1)
            x = torch.cat([x, nxt2, prop2], dim=1)
            committed += 2
        else:                                            # 押错: 修正, 重新起步
            x = torch.cat([x[:, :-1], verify], dim=1)
            committed += 1
            logits, h = model(x)
            passes += 1
            nxt2 = logits[:, -1:].argmax(-1)
            prop2 = mtp(h[:, -1:], model.token_emb(nxt2)).argmax(-1)
            x = torch.cat([x, nxt2, prop2], dim=1)
            committed += 1
    return x[:, :idx.size(1) + n_tokens], passes


# ============================================================
# 演示
# ============================================================
if __name__ == "__main__":
    torch.manual_seed(0)
    V, N = 16, 32

    # 数据: 16-token循环序列 (确定性, 小模型可学到接近100%)
    cycle = torch.randperm(V)
    seq = cycle.repeat(8)[:48]
    x, y = seq[:-1].unsqueeze(0), seq[1:].unsqueeze(0)

    print("=" * 60)
    print("1. 训练 target / draft / MTP")
    print("=" * 60)
    target = MiniLM(V, n_layers=2)                 # 大模型
    draft = MiniLM(V, n_layers=1)                  # 小模型 (draft)
    bad_draft = MiniLM(V, n_layers=1)              # 随机draft (不训练)
    mtp = MTPHead(64, V, 4, 128)
    train_lm(target, x, y, mtp=mtp)                # target带MTP头一起训
    train_lm(draft, x, y)
    print(f"  target(t+1)准确率: {accuracy(target, x, y):.0%}")
    print(f"  draft (t+1)准确率: {accuracy(draft, x, y):.0%}")
    print(f"  MTP   (t+2)准确率: {mtp_accuracy(target, mtp, x, y):.0%}")

    prompt = seq[:8].unsqueeze(0)
    truth = seq[8:8 + N]

    print(f"\n生成 {N} 个token (前向次数 / 加速比):")
    gen, passes = naive_generate(target, prompt, N)
    print(f"  朴素解码:            {passes:3d}次  (1.0x)  "
          f"正确: {'✓' if torch.equal(gen[0, 8:], truth) else '✗'}")

    gen, passes, acc = speculative_generate(target, draft, prompt, N, k=4)
    print(f"  投机解码 (训练draft): {passes:3d}次  ({N / passes:.1f}x)  "
          f"接受率{acc:.0%}  正确: {'✓' if torch.equal(gen[0, 8:], truth) else '✗'}")

    gen, passes, acc = speculative_generate(target, bad_draft, prompt, N, k=4)
    print(f"  投机解码 (随机draft): {passes:3d}次  ({N / passes:.1f}x)  "
          f"接受率{acc:.0%}  ← draft不对齐时反而白付起草开销")

    gen, passes = mtp_generate(target, mtp, prompt, N)
    print(f"  MTP自投机:           {passes:3d}次  ({N / passes:.1f}x)  "
          f"正确: {'✓' if torch.equal(gen[0, 8:], truth) else '✗'}")
