"""
6. 主流LLM架构对比 - 代码示例
对比不同架构的参数量和计算量。
"""

import torch
import torch.nn as nn


def count_params(d_model, num_layers, d_ff, vocab_size, num_heads, num_kv_heads=None):
    """估算LLM参数量"""
    if num_kv_heads is None:
        num_kv_heads = num_heads

    # 每层参数
    attn_params = d_model * d_model * (1 + num_kv_heads/num_heads * 2 + 1)  # Q + KV + O
    ffn_params = d_model * d_ff * 3  # gate + up + down (SwiGLU)
    norm_params = d_model * 2  # 两个RMSNorm
    layer_params = attn_params + ffn_params + norm_params

    # 总参数
    embedding = vocab_size * d_model
    total = embedding + num_layers * layer_params + d_model  # + final norm
    return total


def compare_architectures():
    """对比主流LLM架构"""
    models = [
        ("LLaMA-2 7B", 4096, 32, 11008, 32000, 32, 32),
        ("LLaMA-2 13B", 5120, 40, 13824, 32000, 40, 40),
        ("LLaMA-2 70B", 8192, 80, 28672, 32000, 64, 8),   # GQA: 8 KV heads
        ("LLaMA-3 8B", 4096, 32, 14336, 128256, 32, 8),    # GQA
        ("Qwen2.5 7B", 3584, 28, 18944, 152064, 28, 4),    # GQA
        ("Mistral 7B", 4096, 32, 14336, 32000, 32, 8),     # GQA + 滑动窗口
        ("Phi-3 3.8B", 3072, 32, 8192, 32064, 32, 32),
    ]

    print(f"{'模型':20s} {'参数量':>12s} {'d_model':>8s} {'layers':>7s} {'heads':>6s} {'KV heads':>9s}")
    print("-" * 70)
    for name, d, layers, d_ff, vocab, heads, kv_heads in models:
        params = count_params(d, layers, d_ff, vocab, heads, kv_heads)
        print(f"{name:20s} {params/1e9:>10.1f}B {d:>8d} {layers:>7d} {heads:>6d} {kv_heads:>9d}")


def compare_kv_cache():
    """对比MHA vs GQA的KV Cache大小"""
    seq_len = 4096
    batch = 1

    configs = [
        ("MHA (32 KV heads)", 32, 32, 128),
        ("GQA (8 KV heads)", 32, 8, 128),
        ("GQA (4 KV heads)", 32, 4, 128),
        ("MQA (1 KV head)", 32, 1, 128),
    ]

    print(f"\nKV Cache对比 (32层, seq={seq_len}, fp16):")
    for name, layers, kv_heads, d_k in configs:
        mem = 2 * layers * kv_heads * d_k * seq_len * 2  # 2(K+V) * 2bytes
        print(f"  {name:25s}: {mem/1024**2:.0f} MB")


def show_modern_llm_recipe():
    """现代LLM的标准配方"""
    print("\n现代LLM标准配方 (2024+):")
    recipe = {
        "架构": "Decoder-only",
        "注意力": "GQA (Grouped Query Attention)",
        "位置编码": "RoPE",
        "归一化": "Pre-RMSNorm",
        "FFN": "SwiGLU",
        "激活函数": "SiLU",
        "词表大小": "32K-150K (BPE)",
        "训练数据": "1-15T tokens",
        "上下文长度": "8K-128K",
    }
    for k, v in recipe.items():
        print(f"  {k:12s}: {v}")


if __name__ == "__main__":
    print("=" * 70)
    print("主流LLM架构参数对比")
    print("=" * 70)
    compare_architectures()
    compare_kv_cache()
    show_modern_llm_recipe()
