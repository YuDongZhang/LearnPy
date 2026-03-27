"""
3. Transformer Block - 代码示例
实现完整的Decoder Block：Pre-RMSNorm + Causal Attention + SwiGLU FFN。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class RMSNorm(nn.Module):
    """RMSNorm（LLaMA使用）"""
    def __init__(self, d_model: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x):
        rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
        return x / rms * self.weight


class CausalAttention(nn.Module):
    """因果多头注意力"""
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_QKV = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):
        B, T, C = x.shape
        qkv = self.W_QKV(x).chunk(3, dim=-1)
        Q, K, V = [t.view(B, T, self.num_heads, self.d_k).transpose(1, 2) for t in qkv]

        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        mask = torch.tril(torch.ones(T, T, device=x.device))
        scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        out = (attn @ V).transpose(1, 2).contiguous().view(B, T, C)
        return self.W_O(out)


class SwiGLU(nn.Module):
    """SwiGLU FFN（LLaMA使用）"""
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.w_gate = nn.Linear(d_model, d_ff, bias=False)
        self.w_up = nn.Linear(d_model, d_ff, bias=False)
        self.w_down = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))


class TransformerBlock(nn.Module):
    """完整的Decoder Block"""
    def __init__(self, d_model: int, num_heads: int, d_ff: int):
        super().__init__()
        self.norm1 = RMSNorm(d_model)
        self.attn = CausalAttention(d_model, num_heads)
        self.norm2 = RMSNorm(d_model)
        self.ffn = SwiGLU(d_model, d_ff)

    def forward(self, x):
        # Pre-Norm + 残差
        x = x + self.attn(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x


# ============================================================
# 演示
# ============================================================
if __name__ == "__main__":
    d_model, num_heads, d_ff = 128, 4, 512
    block = TransformerBlock(d_model, num_heads, d_ff)

    x = torch.randn(2, 20, d_model)
    out = block(x)

    params = sum(p.numel() for p in block.parameters())
    print(f"Transformer Block:")
    print(f"  输入: {x.shape} → 输出: {out.shape}")
    print(f"  d_model={d_model}, heads={num_heads}, d_ff={d_ff}")
    print(f"  参数量: {params:,}")
    print(f"\n组件参数:")
    for name, module in block.named_children():
        p = sum(p.numel() for p in module.parameters())
        print(f"  {name}: {p:,}")
