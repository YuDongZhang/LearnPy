"""
7. GQA 与 MLA - 代码示例
GQA (Grouped Query Attention): Llama 3 / Qwen3 / Mistral / gpt-oss 的标准配置
MLA (Multi-head Latent Attention): DeepSeek V2/V3 首创, Kimi K2 / GLM 沿用,
     通过低秩压缩把 KV Cache 压到 MHA 的零头。
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def causal_mask(T, S, device):
    """T 个新 token 对 S 个历史 token 的因果mask (S >= T)。
    prefill 时 S == T, 得到标准下三角; 解码时 T == 1, 全部可见。
    (比第4章的写法更通用: 带cache一次喂多个token也正确)
    """
    return torch.ones(T, S, device=device).tril(diagonal=S - T)


# ============================================================
# 1. GQA 分组查询注意力
# ============================================================
class GroupedQueryAttention(nn.Module):
    """每 group_size = num_heads // num_kv_heads 个Q头共享一组KV。
    num_kv_heads == num_heads 时退化为MHA; == 1 时退化为MQA。
    收益: KV Cache 和 W_K/W_V 参数量都按 kv/heads 比例缩小。
    """

    def __init__(self, d_model, num_heads, num_kv_heads):
        super().__init__()
        assert num_heads % num_kv_heads == 0, "num_heads 必须能被 num_kv_heads 整除"
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.group_size = num_heads // num_kv_heads
        self.d_k = d_model // num_heads

        # K/V 投影只按 KV 头数算 → 参数和 KV Cache 同步变省
        self.W_Q = nn.Linear(d_model, num_heads * self.d_k, bias=False)
        self.W_K = nn.Linear(d_model, num_kv_heads * self.d_k, bias=False)
        self.W_V = nn.Linear(d_model, num_kv_heads * self.d_k, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, kv_cache=None):
        B, T, C = x.shape
        Q = self.W_Q(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_K(x).view(B, T, self.num_kv_heads, self.d_k).transpose(1, 2)
        V = self.W_V(x).view(B, T, self.num_kv_heads, self.d_k).transpose(1, 2)

        # 增量解码: 拼接历史KV (cache里只存KV头, 本来就小)
        if kv_cache is not None:
            K = torch.cat([kv_cache[0], K], dim=2)
            V = torch.cat([kv_cache[1], V], dim=2)
        new_cache = (K, V)
        S = K.size(2)

        # GQA核心: 每组Q头共享同一个KV头
        # (真实推理框架用 view→expand 零拷贝实现, 这里用直观的复制)
        K = K.repeat_interleave(self.group_size, dim=1)  # (B,kv,S,d) → (B,heads,S,d)
        V = V.repeat_interleave(self.group_size, dim=1)

        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        scores = scores.masked_fill(causal_mask(T, S, x.device) == 0, float('-inf'))
        out = F.softmax(scores, dim=-1) @ V
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        return self.W_O(out), new_cache


def demo_gqa():
    d_model, num_heads, num_kv_heads = 128, 8, 2
    gqa = GroupedQueryAttention(d_model, num_heads, num_kv_heads)

    x = torch.randn(2, 16, d_model)
    out, cache = gqa(x)

    print(f"GQA (heads={num_heads}, kv_heads={num_kv_heads}):")
    print(f"  输入 {tuple(x.shape)} → 输出 {tuple(out.shape)}")
    print(f"  KV Cache: K={tuple(cache[0].shape)}, V={tuple(cache[1].shape)}")
    print(f"  分组: 每 {gqa.group_size} 个Q头共享一组KV (头0-3→kv0, 头4-7→kv1)")

    # MQA 是 GQA 的特例 (kv_heads=1)
    mqa = GroupedQueryAttention(d_model, num_heads, 1)
    _, cache_mqa = mqa(x)
    print(f"  MQA特例 (kv_heads=1): KV Cache K={tuple(cache_mqa[0].shape)}")

    # 参数量对比: kv_heads == num_heads 即等价MHA
    mha = GroupedQueryAttention(d_model, num_heads, num_heads)
    p_mha = sum(p.numel() for p in mha.parameters())
    p_gqa = sum(p.numel() for p in gqa.parameters())
    print(f"  参数量: MHA {p_mha:,} → GQA {p_gqa:,} (省 {1 - p_gqa / p_mha:.0%}, 全在K/V投影上)")


# ============================================================
# 2. MLA 多头潜在注意力
# ============================================================
class MultiHeadLatentAttention(nn.Module):
    """MLA (DeepSeek V2/V3):
    1. K/V 不直接算, 先把整个token压到 d_latent 维潜在向量 c_kv;
       推理时 cache 只存 c_kv (+ RoPE用的 k_rope), 每token维度从
       2*num_heads*(d_h+d_rope) 降到 d_latent + d_rope。
    2. RoPE 与 "先压缩再解压" 不兼容 (旋转矩阵插不进低秩分解),
       所以位置信息单独走一条低维通路 —— "解耦RoPE"。
    进阶: 实际推理引擎用"矩阵吸收"把 W_UK 吸收进 Q, 连解压都省了
    (见 DeepSeek-V2 论文附录), 这里为了可读性保留显式解压。
    """

    def __init__(self, d_model, num_heads, d_latent=512, d_rope=64, rope_base=10000.0):
        super().__init__()
        self.num_heads = num_heads
        self.d_h = d_model // num_heads  # 每头的"内容"维度 (无位置部分)
        self.d_latent = d_latent
        self.d_rope = d_rope

        # Q: 每头 = [内容 d_h | 位置 d_rope]
        self.W_Q = nn.Linear(d_model, num_heads * (self.d_h + d_rope), bias=False)
        # 下投影 (压缩): 压出共享的潜在向量
        self.W_DKV = nn.Linear(d_model, d_latent, bias=False)
        # 上投影 (解压): 从潜在向量恢复每头的 K / V
        self.W_UK = nn.Linear(d_latent, num_heads * self.d_h, bias=False)
        self.W_UV = nn.Linear(d_latent, num_heads * self.d_h, bias=False)
        # RoPE 用的 K (所有头共享一份, 维度很低)
        self.W_KR = nn.Linear(d_model, d_rope, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

        inv_freq = 1.0 / (rope_base ** (torch.arange(0, d_rope, 2).float() / d_rope))
        self.register_buffer('inv_freq', inv_freq)

    def _rope(self, x, positions):
        """旋转位置编码, 前后对半拆分。x: (..., T, d), positions: (T,)"""
        half = x.shape[-1] // 2
        freqs = torch.outer(positions.float(), self.inv_freq)  # (T, d/2)
        cos, sin = freqs.cos(), freqs.sin()
        x1, x2 = x[..., :half], x[..., half:]
        return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)

    def forward(self, x, kv_cache=None):
        B, T, C = x.shape

        # --- Q ---
        Q = self.W_Q(x).view(B, T, self.num_heads, self.d_h + self.d_rope).transpose(1, 2)
        q_nope = Q[..., :self.d_h]   # 内容部分, 不加位置
        q_pe = Q[..., self.d_h:]     # 位置部分, 待旋转

        # --- 压缩: 只有这两个要进 cache ---
        c_kv = self.W_DKV(x)   # (B, T, d_latent)  ← K/V的压缩表示
        k_rope = self.W_KR(x)  # (B, T, d_rope)    ← 位置信息单独通路

        if kv_cache is not None:
            c_kv = torch.cat([kv_cache[0], c_kv], dim=1)
            k_rope = torch.cat([kv_cache[1], k_rope], dim=1)
        new_cache = (c_kv, k_rope)
        S = c_kv.size(1)

        # --- 解压: 恢复每头K/V (只在计算时需要, 不占cache) ---
        K = self.W_UK(c_kv).view(B, S, self.num_heads, self.d_h).transpose(1, 2)
        V = self.W_UV(c_kv).view(B, S, self.num_heads, self.d_h).transpose(1, 2)

        # 位置: K 覆盖全部 S 个token, Q 只覆盖新token [S-T, S)
        k_pe = self._rope(k_rope.unsqueeze(1), torch.arange(S, device=x.device))
        q_pe = self._rope(q_pe, torch.arange(S - T, S, device=x.device))

        # Q/K = [内容 | 位置] 拼接后做标准注意力
        Q_full = torch.cat([q_nope, q_pe], dim=-1)
        K_full = torch.cat([K, k_pe.expand(B, self.num_heads, S, self.d_rope)], dim=-1)

        scores = (Q_full @ K_full.transpose(-2, -1)) / math.sqrt(self.d_h + self.d_rope)
        scores = scores.masked_fill(causal_mask(T, S, x.device) == 0, float('-inf'))
        out = F.softmax(scores, dim=-1) @ V
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        return self.W_O(out), new_cache


def demo_mla():
    d_model, num_heads = 256, 8
    mla = MultiHeadLatentAttention(d_model, num_heads, d_latent=128, d_rope=32)

    x = torch.randn(1, 10, d_model)
    out_full, _ = mla(x)  # 一次算全部

    # 增量解码: prefill前5个 + 逐token解码后5个, 结果应与一次前向一致
    out1, cache = mla(x[:, :5])
    outs = [out1]
    for t in range(5, 10):
        out_t, cache = mla(x[:, t:t + 1], kv_cache=cache)
        outs.append(out_t)
    out_inc = torch.cat(outs, dim=1)
    diff = (out_full - out_inc).abs().max().item()

    print(f"MLA (d_model={d_model}, heads={num_heads}, d_latent=128, d_rope=32):")
    print(f"  输入 {tuple(x.shape)} → 输出 {tuple(out_full.shape)}")
    print(f"  Cache内容: c_kv{tuple(cache[0].shape)} + k_rope{tuple(cache[1].shape)}  ← 只存压缩向量")
    print(f"  增量解码 vs 一次前向 最大误差: {diff:.2e} (≈0 说明cache逻辑正确)")


# ============================================================
# 3. KV Cache 大小对比
# ============================================================
def compare_kv_cache():
    """按 DeepSeek-V3 量级估算: 128头, d_h=128, d_rope=64, d_latent=512。
    MLA 用低秩压缩达到接近 MHA 的质量, cache 却只有零头;
    MQA cache 更小, 但质量损失明显。
    """
    heads, d_h, d_rope, d_latent = 128, 128, 64, 512
    seq_len = 4096
    bytes_per = 2  # fp16

    head_dim = d_h + d_rope  # 带RoPE的注意力, 每头实际cache维度
    variants = [
        ("MHA  (2 × 128头 × head_dim)", 2 * heads * head_dim),
        ("GQA  (2 × 8KV头 × head_dim)", 2 * 8 * head_dim),   # Llama-3: 8个KV头
        ("MQA  (2 × 1KV头 × head_dim)", 2 * head_dim),
        ("MLA  (d_latent + d_rope)", d_latent + d_rope),
    ]

    print(f"KV Cache对比 (128头, seq={seq_len}, fp16, 单层, batch=1):")
    mha_elems = variants[0][1]
    for name, elems in variants:
        mem = elems * seq_len * bytes_per / 1024**2
        print(f"  {name:30s}: {mem:6.1f} MB  ({elems / mha_elems:5.1%} of MHA)")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. GQA 分组查询注意力")
    print("=" * 60)
    demo_gqa()

    print("\n" + "=" * 60)
    print("2. MLA 多头潜在注意力")
    print("=" * 60)
    demo_mla()

    print("\n" + "=" * 60)
    print("3. KV Cache 大小对比")
    print("=" * 60)
    compare_kv_cache()
