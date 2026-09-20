"""
5. 从零搭建mini GPT
一个完整的小型GPT模型，可以在简单数据上训练。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# ============================================================
# 模型组件
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


class FFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        return self.w2(F.gelu(self.w1(x)))


class Block(nn.Module):
    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalAttention(d_model, num_heads)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = FFN(d_model, d_ff)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ffn(self.ln2(x))
        return x


class MiniGPT(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_len):
        super().__init__()
        self.max_len = max_len
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList([Block(d_model, num_heads, d_ff) for _ in range(num_layers)])
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx):
        B, T = idx.shape
        tok = self.token_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = tok + pos
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.lm_head(x)

    @torch.no_grad()
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits = self(idx[:, -self.max_len:])  # 截断到max_len
            next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            idx = torch.cat([idx, next_token], dim=1)
        return idx


# ============================================================
# 训练
# ============================================================
def train():
    # 简单数据：重复模式 (纯随机数据loss只会停在ln(50)≈3.91, 学不到东西)
    vocab_size = 50
    data = torch.stack([torch.randint(0, vocab_size, (8,)).repeat(5) for _ in range(100)])
    print(f"随机基线: ln(50) = {math.log(vocab_size):.2f} (loss降到它以下才算学到规律)")

    model = MiniGPT(vocab_size=vocab_size, d_model=64, num_heads=4,
                    num_layers=4, d_ff=256, max_len=256)
    params = sum(p.numel() for p in model.parameters())
    print(f"MiniGPT 参数量: {params:,}")

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(60):
        total_loss, n_batches = 0.0, 0
        for batch in data.split(10):
            x = batch[:, :-1]
            y = batch[:, 1:]
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, vocab_size), y.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            n_batches += 1
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}: loss={total_loss/n_batches:.4f}")

    # 生成: 用模式开头做提示, 看模型能否正确续写 (形成"归纳头"后可以)
    prompt = data[0, :8].unsqueeze(0)
    generated = model.generate(prompt, max_new_tokens=20)
    print(f"\n  提示(模式): {prompt[0].tolist()}")
    print(f"  模型续写:   {generated[0, 8:].tolist()}")
    print(f"  期望续写:   {data[0, 8:28].tolist()}")


if __name__ == "__main__":
    train()
