"""
1. 注意力机制从零实现
用纯PyTorch实现Scaled Dot-Product Attention和Multi-Head Attention。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# ============================================================
# 1. Scaled Dot-Product Attention
# ============================================================
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: (batch, seq_len, d_k)
    mask: (seq_len, seq_len) 因果mask
    """
    d_k = Q.size(-1)
    # 计算注意力分数
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    # 应用mask（因果注意力）
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    # Softmax
    weights = F.softmax(scores, dim=-1)
    # 加权求和
    output = torch.matmul(weights, V)
    return output, weights


def demo_attention():
    """演示基础注意力"""
    batch, seq_len, d_k = 1, 4, 8
    Q = torch.randn(batch, seq_len, d_k)
    K = torch.randn(batch, seq_len, d_k)
    V = torch.randn(batch, seq_len, d_k)

    # 因果mask：下三角为1
    mask = torch.tril(torch.ones(seq_len, seq_len))

    output, weights = scaled_dot_product_attention(Q, K, V, mask)
    print(f"输入形状: Q={Q.shape}, K={K.shape}, V={V.shape}")
    print(f"输出形状: {output.shape}")
    print(f"注意力权重:\n{weights[0].detach()}")


# ============================================================
# 2. Multi-Head Attention
# ============================================================
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch, seq_len, _ = x.shape

        # 线性投影
        Q = self.W_Q(x)  # (batch, seq, d_model)
        K = self.W_K(x)
        V = self.W_V(x)

        # 拆分多头: (batch, seq, d_model) → (batch, heads, seq, d_k)
        Q = Q.view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        # 注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        weights = F.softmax(scores, dim=-1)
        attn_output = torch.matmul(weights, V)

        # 合并多头: (batch, heads, seq, d_k) → (batch, seq, d_model)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch, seq_len, self.d_model)

        # 输出投影
        return self.W_O(attn_output)


def demo_multi_head():
    """演示多头注意力"""
    d_model, num_heads = 64, 4
    mha = MultiHeadAttention(d_model, num_heads)

    x = torch.randn(2, 10, d_model)  # batch=2, seq=10
    mask = torch.tril(torch.ones(10, 10)).unsqueeze(0).unsqueeze(0)

    output = mha(x, mask)
    params = sum(p.numel() for p in mha.parameters())
    print(f"\nMulti-Head Attention:")
    print(f"  输入: {x.shape} → 输出: {output.shape}")
    print(f"  heads={num_heads}, d_k={d_model//num_heads}")
    print(f"  参数量: {params:,}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. Scaled Dot-Product Attention")
    print("=" * 60)
    demo_attention()

    print("\n" + "=" * 60)
    print("2. Multi-Head Attention")
    print("=" * 60)
    demo_multi_head()
