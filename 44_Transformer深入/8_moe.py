"""
8. MoE 混合专家 (Mixture of Experts) - 代码示例
DeepSeek-V3 (256选8+1共享) / Qwen3 / gpt-oss / Nemotron 3 都采用MoE,
2026年初的新架构里7成以上是某种形式的MoE —— dense模型已成少数派。
核心思想: 总参数量很大 (表达能力强), 但每个token只激活一小部分专家 (计算便宜)。
在Transformer里, MoE替换的是每个Block的FFN, 注意力部分不变。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================
# 1. 单个专家 = 一个小FFN
# ============================================================
class SwiGLU(nn.Module):
    """同第3章的SwiGLU FFN"""

    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w_gate = nn.Linear(d_model, d_ff, bias=False)
        self.w_up = nn.Linear(d_model, d_ff, bias=False)
        self.w_down = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))


# ============================================================
# 2. MoE层 (DeepSeekMoE风格: 细粒度专家 + Top-K路由 + 共享专家)
# ============================================================
class MoEFFN(nn.Module):
    """MoE替换Transformer Block里的FFN:
    - gate (router): 为每个token打分, 选Top-K个路由专家
    - 细粒度专家: 专家多而小 (DeepSeek-V3: 256选8), 专业化程度更高
    - 共享专家: 每个token必经, 学"通用知识",
      避免公共模式在每个路由专家里重复学一遍
    - 负载均衡: 经典方案是辅助loss (见下方函数);
      DeepSeek-V3改为免loss的bias动态调整, 避免辅助loss干扰主梯度
    """

    def __init__(self, d_model, d_ff, num_experts=8, top_k=2, num_shared=1):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

        self.gate = nn.Linear(d_model, num_experts, bias=False)
        self.experts = nn.ModuleList([SwiGLU(d_model, d_ff) for _ in range(num_experts)])
        self.shared_experts = nn.ModuleList([SwiGLU(d_model, d_ff) for _ in range(num_shared)])

    def forward(self, x):
        B, T, C = x.shape
        x_flat = x.view(-1, C)  # (N, C): 每个token独立路由

        # 路由: 打分 → Top-K → 在选中的K个里softmax
        logits = self.gate(x_flat)                                  # (N, E)
        weights, indices = torch.topk(logits, self.top_k, dim=-1)   # (N, k)
        weights = F.softmax(weights, dim=-1)

        # 逐专家计算: 每个专家只处理分给自己的token
        # (教学用直观实现; 生产实现按专家分组后用grouped GEMM一次算完)
        out = torch.zeros_like(x_flat)
        for e in range(self.num_experts):
            mask = indices == e                          # (N, k): 谁把专家e选进了Top-K
            token_idx, slot = mask.nonzero(as_tuple=True)
            if token_idx.numel() == 0:
                continue
            y = self.experts[e](x_flat[token_idx])       # 只算被选中的token
            w = weights[token_idx, slot].unsqueeze(-1)   # 对应槽位的路由权重
            out.index_add_(0, token_idx, y * w)          # 加权累加回原位置

        # 共享专家: 所有token必经, 不参与路由
        shared = sum(expert(x_flat) for expert in self.shared_experts)
        return (out + shared).view(B, T, C), logits


# ============================================================
# 3. 负载均衡辅助loss
# ============================================================
def load_balancing_loss(logits, indices):
    """Switch Transformer式辅助loss: E × Σ f_i·P_i
    f_i: 专家i被选中的频率; P_i: router给专家i的平均概率
    路由均匀时 ≈ 1, 坍缩到少数专家时显著变大 → 加进总loss一起优化。
    """
    N, E = logits.shape
    k = indices.shape[1]
    probs = F.softmax(logits, dim=-1)                          # (N, E)
    f = F.one_hot(indices, E).sum(dim=(0, 1)).float() / (N * k)  # 各专家被选频率
    P = probs.mean(dim=0)                                      # 各专家平均路由概率
    return E * (f * P).sum()


# ============================================================
# 演示
# ============================================================
def demo_moe():
    d_model, d_ff = 128, 256
    moe = MoEFFN(d_model, d_ff, num_experts=8, top_k=2, num_shared=1)

    x = torch.randn(2, 10, d_model)
    out, logits = moe(x)

    print(f"MoE层 (8路由专家选2 + 1共享):")
    print(f"  输入 {tuple(x.shape)} → 输出 {tuple(out.shape)}")

    # 路由分布: 20个token × top2 = 40次分发
    indices = torch.topk(logits, 2, dim=-1).indices
    counts = torch.bincount(indices.flatten(), minlength=8)
    print(f"  各专家承接token数: {counts.tolist()} (共{counts.sum().item()}次分发)")

    # 关键数字: 总参数 vs 每token激活参数
    total = sum(p.numel() for p in moe.parameters())
    expert_p = sum(p.numel() for p in moe.experts[0].parameters())
    shared_p = sum(p.numel() for p in moe.shared_experts[0].parameters())
    gate_p = sum(p.numel() for p in moe.gate.parameters())
    active = gate_p + 2 * expert_p + shared_p  # gate + 2路由专家 + 1共享
    print(f"  总参数: {total:,}")
    print(f"  每token激活: {active:,} ({active / total:.1%})  ← MoE的意义所在")


def demo_load_balancing():
    """没有均衡约束时, router容易坍缩: 少数专家被选爆, 其余闲置"""
    N, E, k = 100, 8, 2

    logits_uniform = torch.randn(N, E)
    idx_u = torch.topk(logits_uniform, k, dim=-1).indices

    logits_skew = torch.randn(N, E)
    logits_skew[:, :2] += 10  # 人为让router偏向专家0和1
    idx_s = torch.topk(logits_skew, k, dim=-1).indices

    print(f"负载均衡辅助loss (均匀≈1, 越大越不均衡):")
    print(f"  均匀路由: {load_balancing_loss(logits_uniform, idx_u).item():.3f}")
    print(f"  坍缩路由: {load_balancing_loss(logits_skew, idx_s).item():.3f}")


def compare_dense_vs_moe():
    """真实模型对比: 总参数 (容量) vs 激活参数 (每个token的计算/显存)"""
    models = [
        ("Llama-3 70B (dense)", 70, 70),
        ("Mixtral 8x7B", 47, 13),
        ("Qwen3-235B-A22B", 235, 22),
        ("gpt-oss-120b", 117, 5),
        ("DeepSeek-V3", 671, 37),
    ]
    print(f"{'模型':22s} {'总参数(B)':>9s} {'激活(B)':>8s} {'激活比':>7s}")
    print("-" * 50)
    for name, total, active in models:
        print(f"{name:22s} {total:>9d} {active:>8d} {active / total:>6.0%}")


if __name__ == "__main__":
    print("=" * 60)
    print("1. MoE层与路由")
    print("=" * 60)
    demo_moe()

    print("\n" + "=" * 60)
    print("2. 负载均衡")
    print("=" * 60)
    demo_load_balancing()

    print("\n" + "=" * 60)
    print("3. Dense vs MoE 真实模型对比")
    print("=" * 60)
    compare_dense_vs_moe()
