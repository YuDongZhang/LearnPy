"""
6. Scaling Laws - 代码示例
演示Chinchilla Scaling Law的计算和模型选择。
"""

import math


# ============================================================
# 1. Chinchilla最优配置计算
# ============================================================
def chinchilla_optimal(params_billions: float) -> dict:
    """根据Chinchilla Law计算最优训练配置"""
    optimal_tokens = params_billions * 20  # 最优: 数据量 ≈ 20 × 参数量
    # FLOPs ≈ 6 × N × D
    flops = 6 * params_billions * 1e9 * optimal_tokens * 1e9
    # A100 GPU: ~312 TFLOPS (bf16)
    gpu_hours = flops / (312e12 * 3600)
    a100_days = gpu_hours / (24 * 8)  # 8卡集群

    return {
        "params": f"{params_billions}B",
        "optimal_tokens": f"{optimal_tokens:.0f}B",
        "flops": f"{flops:.2e}",
        "a100_8gpu_days": f"{a100_days:.0f}",
    }


def demo_chinchilla():
    """展示不同规模模型的最优训练配置"""
    print("Chinchilla最优训练配置:")
    print(f"{'参数量':>8s} | {'最优数据量':>10s} | {'FLOPs':>12s} | {'8×A100天数':>10s}")
    print("-" * 55)
    for b in [0.5, 1, 3, 7, 13, 70]:
        r = chinchilla_optimal(b)
        print(f"{r['params']:>8s} | {r['optimal_tokens']:>10s} | {r['flops']:>12s} | {r['a100_8gpu_days']:>10s}")


# ============================================================
# 2. 训练成本估算
# ============================================================
def estimate_cost(params_b: float, tokens_b: float, gpu_type: str = "A100"):
    """估算训练成本"""
    gpu_specs = {
        "A100": {"tflops": 312, "price_per_hour": 2.0},
        "H100": {"tflops": 990, "price_per_hour": 4.0},
        "4090": {"tflops": 165, "price_per_hour": 0.5},
    }
    spec = gpu_specs[gpu_type]
    flops = 6 * params_b * 1e9 * tokens_b * 1e9
    gpu_hours = flops / (spec["tflops"] * 1e12 * 3600)
    cost = gpu_hours * spec["price_per_hour"]

    return {
        "gpu_type": gpu_type,
        "gpu_hours": f"{gpu_hours:.0f}",
        "cost_usd": f"${cost:,.0f}",
    }


def demo_cost():
    """对比不同GPU的训练成本"""
    print("\n训练成本估算（7B模型，140B tokens）:")
    for gpu in ["A100", "H100", "4090"]:
        r = estimate_cost(7, 140, gpu)
        print(f"  {r['gpu_type']}: {r['gpu_hours']} GPU小时, {r['cost_usd']}")


# ============================================================
# 3. 模型选择建议
# ============================================================
def model_selection_guide():
    """根据预算和需求推荐模型"""
    scenarios = [
        {"budget": "低（消费级GPU）", "task": "简单问答", "recommend": "Qwen2.5-0.5B/1.5B + QLoRA"},
        {"budget": "中（单卡A100）", "task": "领域微调", "recommend": "Qwen2.5-7B + LoRA"},
        {"budget": "高（多卡A100）", "task": "通用能力", "recommend": "LLaMA-3-70B + QLoRA"},
        {"budget": "很高（集群）", "task": "从零预训练", "recommend": "自定义架构 + DeepSpeed"},
    ]

    print("\n模型选择指南:")
    for s in scenarios:
        print(f"  {s['budget']:20s} | {s['task']:10s} → {s['recommend']}")

    print("\n核心原则:")
    print("  - 小模型+高质量数据 > 大模型+低质量数据")
    print("  - 先用小模型验证方案，再考虑扩大规模")
    print("  - 能用API就不要自己训练")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. Chinchilla最优配置")
    print("=" * 60)
    demo_chinchilla()

    print("\n" + "=" * 60)
    print("2. 训练成本估算")
    print("=" * 60)
    demo_cost()

    print("\n" + "=" * 60)
    print("3. 模型选择指南")
    print("=" * 60)
    model_selection_guide()
