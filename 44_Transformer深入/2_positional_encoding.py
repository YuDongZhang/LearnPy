"""
2. 位置编码 - 代码示例
实现Sinusoidal、Learned和RoPE三种位置编码,
以及长上下文外推缩放: Linear PI / NTK-aware / YaRN。
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
    def __init__(self, head_dim: int, base: float = 10000.0):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, head_dim, 2).float() / head_dim))
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
# 4. 长上下文外推：Linear PI / NTK-aware / YaRN
# ============================================================
class ScaledRoPE(nn.Module):
    """用短上下文(如4K)训练的模型, 外推到 s 倍长度(如128K)。

    RoPE的每个维度对是一根"不同转速的指针":
    - 高频维(波长短)转得快 → 编码局部相对位置
    - 低频维(波长长)转得慢 → 编码远距离依赖
    训练时模型只见过指针在train_len内的转法; 外推 = 让指针在更远
    位置依然"可分辨"。三种方案都只改inv_freq, 不改模型权重:

    - linear: 所有频率÷s (位置插值PI) — 远处对了, 但局部分辨率下降
    - ntk:    改base: base×s^(d/(d-2)) — 自动只压低频、保留高频
    - yarn:   按波长分段处理 + 注意力温度补偿, 效果最好
              (Qwen/LLaMA-3的rope_scaling就是这个思路的变体)
    """

    def __init__(self, head_dim, train_len=512, scale=4.0, method="yarn",
                 base=10000.0, low_factor=1.0, high_factor=4.0):
        super().__init__()
        idx = torch.arange(0, head_dim, 2).float()
        inv_freq = base ** (-idx / head_dim)

        if method == "linear":
            inv_freq = inv_freq / scale
        elif method == "ntk":
            new_base = base * scale ** (head_dim / (head_dim - 2))
            inv_freq = new_base ** (-idx / head_dim)
        else:  # yarn: NTK-by-parts, 按波长分段
            wavelen = 2 * math.pi / inv_freq
            scaled = inv_freq / scale
            keep = wavelen < train_len / high_factor    # 高频维: 原样保留
            interp = wavelen > train_len / low_factor   # 低频维: 完全插值
            # 中间频段: 线性混合
            smooth = ((train_len / wavelen - low_factor) /
                      (high_factor - low_factor)).clamp(0, 1)
            inv_freq = torch.where(
                keep, inv_freq,
                torch.where(interp, scaled,
                            (1 - smooth) * scaled + smooth * inv_freq))

        self.register_buffer('inv_freq', inv_freq)
        # YaRN的注意力温度: 外推后远处注意力变"钝", 降温补偿
        self.attn_scale = 1.0 / (0.1 * math.log(scale) + 1.0) if method == "yarn" else 1.0

    def forward(self, q, k):
        """对Q/K应用缩放RoPE (YaRN时注意力分数记得乘attn_scale)"""
        seq_len = q.size(-2)
        t = torch.arange(seq_len, device=q.device).float()
        freqs = torch.outer(t, self.inv_freq)
        cos_val, sin_val = freqs.cos(), freqs.sin()
        return self._rotate(q, cos_val, sin_val), self._rotate(k, cos_val, sin_val)

    def _rotate(self, x, cos_val, sin_val):
        d = x.shape[-1]
        x1, x2 = x[..., :d // 2], x[..., d // 2:]
        return torch.cat([x1 * cos_val - x2 * sin_val,
                          x1 * sin_val + x2 * cos_val], dim=-1)


def demo_scaling():
    """对比三种外推方案对各频率维度的处理 (1=保留, 0.25=压缩到1/4)"""
    head_dim, train_len, scale = 64, 512, 4
    print(f"\n长上下文外推: {train_len} → {train_len * scale} (scale={scale})")

    base_freq = 10000.0 ** (-torch.arange(0, head_dim, 2).float() / head_dim)
    for method in ["linear", "ntk", "yarn"]:
        rope = ScaledRoPE(head_dim, train_len, scale, method)
        ratio = rope.inv_freq / base_freq
        n_keep = (ratio > 0.99).sum().item()
        line = (f"  {method:6s}: 高频维 {ratio[0]:.2f}, 低频维 {ratio[-1]:.2f}, "
                f"完整保留 {n_keep}/{head_dim // 2} 维")
        if method == "yarn":
            line += f", 注意力温度×{rope.attn_scale:.2f}"
        print(line)

    q = torch.randn(2, 4, train_len * scale, head_dim)
    k = torch.randn(2, 4, train_len * scale, head_dim)
    q_rot, k_rot = ScaledRoPE(head_dim, train_len, scale, "yarn")(q, k)
    print(f"  外推后RoPE正常工作: Q {tuple(q.shape)} → {tuple(q_rot.shape)}")


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

    # RoPE 作用在每头的维度d_k上 (不是d_model!)
    head_dim = d_model // 4
    rope = RoPE(head_dim)
    q = torch.randn(batch, 4, seq_len, head_dim)  # (batch, heads, seq, d_k)
    k = torch.randn(batch, 4, seq_len, head_dim)
    q_rot, k_rot = rope(q, k)
    print(f"RoPE: Q {q.shape} → {q_rot.shape}")


if __name__ == "__main__":
    demo()
    demo_scaling()
