"""
4. KV Cache - 代码示例
演示KV Cache的原理和加速效果。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import time


class AttentionWithKVCache(nn.Module):
    """带KV Cache的因果注意力"""
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, kv_cache=None):
        B, T, C = x.shape
        Q = self.W_Q(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_K(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_V(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)

        # 使用KV Cache
        if kv_cache is not None:
            K = torch.cat([kv_cache[0], K], dim=2)
            V = torch.cat([kv_cache[1], V], dim=2)
        new_cache = (K, V)

        # Attention
        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        seq_len = K.size(2)
        mask = torch.tril(torch.ones(T, seq_len, device=x.device))
        if T == 1:  # 生成阶段，只有最后一行
            mask = torch.ones(1, seq_len, device=x.device)
        scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        out = (attn @ V).transpose(1, 2).contiguous().view(B, T, C)
        return self.W_O(out), new_cache


# ============================================================
# 对比有无KV Cache的速度
# ============================================================
def demo_kv_cache():
    d_model, num_heads = 128, 4
    attn = AttentionWithKVCache(d_model, num_heads)
    attn.eval()

    gen_len = 50

    # 方式1: 无KV Cache（每次重新计算全部）
    start = time.time()
    tokens = torch.randn(1, 1, d_model)
    for i in range(gen_len):
        full_input = torch.randn(1, i + 1, d_model)
        with torch.no_grad():
            out, _ = attn(full_input)
    time_no_cache = time.time() - start

    # 方式2: 有KV Cache（只计算新token）
    start = time.time()
    first_token = torch.randn(1, 1, d_model)
    with torch.no_grad():
        out, cache = attn(first_token)
    for i in range(gen_len - 1):
        new_token = torch.randn(1, 1, d_model)
        with torch.no_grad():
            out, cache = attn(new_token, kv_cache=cache)
    time_with_cache = time.time() - start

    print(f"生成 {gen_len} tokens:")
    print(f"  无KV Cache: {time_no_cache:.4f}s")
    print(f"  有KV Cache: {time_with_cache:.4f}s")
    print(f"  加速比: {time_no_cache / time_with_cache:.1f}x")
    print(f"  KV Cache大小: K={cache[0].shape}, V={cache[1].shape}")


def demo_cache_memory():
    """估算KV Cache显存"""
    configs = [
        ("7B (32层, 32头, d=128)", 32, 32, 128),
        ("13B (40层, 40头, d=128)", 40, 40, 128),
        ("70B (80层, 64头, d=128)", 80, 64, 128),
    ]
    seq_len = 4096
    print(f"\nKV Cache显存估算 (seq_len={seq_len}, fp16):")
    for name, layers, heads, d_k in configs:
        # 2(K+V) × layers × heads × d_k × seq_len × 2bytes
        mem = 2 * layers * heads * d_k * seq_len * 2
        print(f"  {name}: {mem / 1024**3:.2f} GB")


if __name__ == "__main__":
    print("=" * 60)
    print("KV Cache速度对比")
    print("=" * 60)
    demo_kv_cache()

    demo_cache_memory()
