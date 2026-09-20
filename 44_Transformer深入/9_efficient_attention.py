"""
9. 高效注意力 - 代码示例
1. 滑动窗口注意力 SWA (Mistral引入, Gemma广泛采用)
2. Flash Attention: IO-aware分块计算思想 (在线softmax) + PyTorch SDPA接口
3. 稀疏注意力与混合架构概览 (NSA/DSA, Mamba混合)
长上下文的两大方向: 少算 (稀疏/窗口) 和 少存 (MLA, 见第7章)。
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================
# 1. 滑动窗口注意力 (SWA)
# ============================================================
class SlidingWindowAttention(nn.Module):
    """每个token只看最近 window 个token (含自身)。
    - 计算量 O(T×window), KV Cache也只需保留最近window个 → 恒定显存
    - 实际模型常分层混用: 底层小窗口抓局部, 顶层全注意力抓全局 (Gemma)
    """

    def __init__(self, d_model, num_heads, window):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.window = window
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):
        B, T, C = x.shape
        Q, K, V = self.qkv(x).chunk(3, dim=-1)
        Q = Q.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(B, T, self.num_heads, self.d_k).transpose(1, 2)

        # 带状因果mask: 因果(tril) ∩ 最近window个(triu)
        mask = torch.ones(T, T, device=x.device).tril().triu(-(self.window - 1))

        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        scores = scores.masked_fill(mask == 0, float('-inf'))
        out = F.softmax(scores, dim=-1) @ V
        return self.proj(out.transpose(1, 2).contiguous().view(B, T, C))


def demo_swa():
    d_model, num_heads, window = 64, 4, 4
    swa = SlidingWindowAttention(d_model, num_heads, window)

    x = torch.randn(2, 12, d_model)
    out = swa(x)
    print(f"滑动窗口注意力 (window={window}):")
    print(f"  输入 {tuple(x.shape)} → 输出 {tuple(out.shape)}")

    print(f"  T=12, window=4 的可见性 (#=可见):")
    mask = torch.ones(12, 12).tril().triu(-(window - 1))
    for row in mask:
        print("    " + "".join("#" if v else "." for v in row.tolist()))

    T = 32768
    print(f"\n  计算量对比 (T={T}):")
    print(f"    全注意力:      T×T      = {T * T / 1e9:.1f}G 次打分")
    print(f"    SWA (w=4096): T×window = {T * 4096 / 1e9:.1f}G 次打分")


# ============================================================
# 2. Flash Attention: 分块 + 在线softmax
# ============================================================
def flash_attention_reference(Q, K, V, block_size=64):
    """Flash Attention的数学核心 (教学版, 单头, 无mask):
    1. 分块: Q/K/V切成小块, 逐块计算, 从不完整物化 (T,T) 打分矩阵
    2. 在线softmax: 每读入一块K/V, 用 running max / running sum 增量修正
    输出与naive注意力数值一致。
    真正的Flash Attention (FA2/FA3) 还把块驻留在GPU SRAM、跳过因果上三角块,
    收益主要在IO (少读写HBM) 而不是FLOP —— "IO-aware" 由此得名。
    """
    T_q, d = Q.shape
    out = torch.zeros(T_q, d)
    m = torch.full((T_q,), float('-inf'))  # 每行的running max
    l = torch.zeros(T_q)                   # 每行的running sum

    for start in range(0, K.shape[0], block_size):
        Kb = K[start:start + block_size]
        Vb = V[start:start + block_size]
        scores = Q @ Kb.T / math.sqrt(d)          # (T_q, bs) ← 只物化一个块!

        m_new = torch.maximum(m, scores.max(dim=-1).values)
        p = torch.exp(scores - m_new[:, None])    # 本块的"未归一化"softmax
        l = l * torch.exp(m - m_new) + p.sum(dim=-1)     # 修正历史累积
        out = out * torch.exp(m - m_new)[:, None] + p @ Vb
        m = m_new

    return out / l[:, None]  # 最后统一归一化


def demo_flash_attention():
    torch.manual_seed(0)
    T, d = 256, 64
    Q, K, V = torch.randn(T, d), torch.randn(T, d), torch.randn(T, d)

    naive = torch.softmax(Q @ K.T / math.sqrt(d), dim=-1) @ V
    flash = flash_attention_reference(Q, K, V, block_size=64)
    diff = (naive - flash).abs().max().item()

    print(f"Flash Attention 数学验证:")
    print(f"  分块在线softmax vs naive: 最大误差 {diff:.2e} (≈0 即正确)")


def demo_sdpa():
    """PyTorch 2.0+ 官方接口: 生产代码直接用它, 不要手写注意力。
    自动选择后端: Flash Attention / memory-efficient / math。
    """
    q = torch.randn(2, 8, 512, 64)
    k = torch.randn(2, 8, 512, 64)
    v = torch.randn(2, 8, 512, 64)
    out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    print(f"SDPA接口 (is_causal=True):")
    print(f"  输出 {tuple(out.shape)}  ← 一行替代手写的打分/mask/softmax")

    # 手写注意力要物化整个打分矩阵, SDPA不用
    T = 8192
    score_mem = 1 * 4 * T * T * 4 / 1024**2  # (batch×heads×T×T, fp32)
    print(f"  seq={T}时手写需物化打分矩阵 ≈ {score_mem:.0f} MB; SDPA全程不物化")


# ============================================================
# 3. 稀疏注意力与混合架构概览
# ============================================================
def efficiency_overview():
    """2025-2026 长上下文效率的主要路线 (打印概览)"""
    rows = [
        ("SWA 滑动窗口", "固定窗口内可见", "Mistral / Gemma", "KV Cache恒定"),
        ("NSA 原生稀疏", "学习的块级Top-K + 窗口", "DeepSeek-V3", "训练也可加速"),
        ("DSA 稀疏注意力", "轻量indexer选关键token", "DeepSeek-V3.2-Exp", "API降价50%+"),
        ("MLA + 序列压缩", "latent压缩+沿序列维度压缩", "DeepSeek-V4", "1M上下文"),
        ("Mamba混合架构", "SSM层为主+少量注意力锚点", "Nemotron 3 / Kimi Linear", "推理吞吐数倍"),
    ]
    print("稀疏注意力与混合架构 (少算 vs 少存 vs 换骨架):")
    print(f"  {'技术':14s} {'思路':20s} {'代表':24s} {'收益'}")
    print("  " + "-" * 76)
    for name, idea, model, benefit in rows:
        print(f"  {name:14s} {idea:20s} {model:24s} {benefit}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 滑动窗口注意力 SWA")
    print("=" * 60)
    demo_swa()

    print("\n" + "=" * 60)
    print("2. Flash Attention 与 SDPA")
    print("=" * 60)
    demo_flash_attention()
    print()
    demo_sdpa()

    print("\n" + "=" * 60)
    print("3. 稀疏注意力与混合架构概览")
    print("=" * 60)
    efficiency_overview()
