"""
2. 位置编码 - 代码示例
实现Sinusoidal、Learned和RoPE三种位置编码。
"""

import torch
import torch.nn as nn
import math


# ============================================================
# 1. Sinusoidal位置编码（原始Transformer）
# ============================================================
class SinusoidalPE(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]


# ============================================================
# 2. 可学习位置编码（GPT-2）
# ============================================================
class LearnedPE(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        self.pe = nn.Embedding(max_len, d_model)

    def forward(self, x):
        positions = torch.arange(x.size(1), device=x.device)
        return x + self.pe(positions)


# ============================================================
# 3. RoPE旋转位置编码（LLaMA）
# ============================================================
class RoPE(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000, base: float = 10000.0):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, d_model, 2).float() / d_model))
        self.register_buffer('inv_freq', inv_freq)

    def forward(self, q, k):
        """对Q和K应用旋转位置编码"""
        seq_len = q.size(-2)
        t = torch.arange(seq_len, device=q.device).float()
        freqs = torch.outer(t, self.inv_freq)  # (seq_len, d/2)
        cos_val = freqs.cos()
        sin_val = freqs.sin()

        q_rotated = self._rotate(q, cos_val, sin_val)
        k_rotated = self._rotate(k, cos_val, sin_val)
        return q_rotated, k_rotated

    def _rotate(self, x, cos_val, sin_val):
        # x: (..., seq_len, d)
        d = x.shape[-1]
        x1 = x[..., :d//2]
        x2 = x[..., d//2:]
        rotated = torch.cat([
            x1 * cos_val - x2 * sin_val,
            x1 * sin_val + x2 * cos_val,
        ], dim=-1)
        return rotated


# ============================================================
# 演示
# ============================================================
def demo():
    d_model, seq_len, batch = 64, 20, 2
    x = torch.randn(batch, seq_len, d_model)

    # Sinusoidal
    sin_pe = SinusoidalPE(d_model)
    out1 = sin_pe(x)
    print(f"Sinusoidal PE: {x.shape} → {out1.shape}")

    # Learned
    learn_pe = LearnedPE(d_model)
    out2 = learn_pe(x)
    print(f"Learned PE: {x.shape} → {out2.shape}")

    # RoPE
    rope = RoPE(d_model)
    q = torch.randn(batch, 4, seq_len, d_model // 4)  # (batch, heads, seq, d_k)
    k = torch.randn(batch, 4, seq_len, d_model // 4)
    q_rot, k_rot = rope(q, k)
    print(f"RoPE: Q {q.shape} → {q_rot.shape}")


if __name__ == "__main__":
    demo()
