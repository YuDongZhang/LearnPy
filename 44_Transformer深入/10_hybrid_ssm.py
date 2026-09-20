"""
10. 混合架构：Mamba/SSM + 注意力 - 代码示例
SSM把历史压缩成固定大小的状态: 线性复杂度、恒定显存, 但精确检索弱;
注意力反之。混合架构 = Mamba层为主 + 少量注意力层做"锚点"
(Jamba / Nemotron 3 / Kimi Linear / HunyuanTurboS)。
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================
# 1. 注意力锚点 (自包含, 同第3章思路)
# ============================================================
class CausalAttention(nn.Module):
    """因果注意力: 全量回顾历史, 精确检索强, 但KV Cache随T线性增长"""

    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):
        B, T, C = x.shape
        Q, K, V = self.qkv(x).chunk(3, dim=-1)
        Q = Q.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        mask = torch.tril(torch.ones(T, T, device=x.device))
        scores = scores.masked_fill(mask == 0, float('-inf'))
        out = F.softmax(scores, dim=-1) @ V
        return self.proj(out.transpose(1, 2).contiguous().view(B, T, C))


# ============================================================
# 2. 选择性SSM (Mamba核心, 教学版逐token循环)
# ============================================================
class SelectiveSSM(nn.Module):
    """状态空间模型的离散递推:
        h_t = Ā ⊙ h_{t-1} + B̄·x_t    # 更新状态: 衰减旧信息, 写入新信息
        y_t = C·h_t                    # 读出
    "选择性" = Δ/B/C 由输入决定 → 模型学会决定记什么、忘什么:
        Δ大 → Ā→0 → 丢弃旧状态 (忘); Δ小 → Ā→1 → 保留历史 (记)
    状态 h 只有 (d_model × d_state) 维, 与序列长度无关 ← 恒定显存的根源。
    训练时Mamba用并行扫描+kernel融合, 这里用直观循环 (慢但好懂)。
    """

    def __init__(self, d_model, d_state=16):
        super().__init__()
        self.d_state = d_state
        # A为负值(衰减), 用log参数化保证训练中恒为负
        self.A_log = nn.Parameter(torch.log(torch.rand(d_model, d_state) * (d_state - 1) + 1))
        # Δ/B/C 全部由输入投影 → "选择性"的来源
        self.x_proj = nn.Linear(d_model, 2 * d_state, bias=False)  # B, C
        self.dt_proj = nn.Linear(d_model, d_model, bias=True)      # Δ

    def forward(self, x):
        B_, T, D = x.shape
        S = self.d_state
        A = -torch.exp(self.A_log)              # (D, S) 全为负 → 指数衰减
        delta = F.softplus(self.dt_proj(x))     # (B,T,D) 步长Δ>0
        BC = self.x_proj(x)
        Bv, Cv = BC[..., :S], BC[..., S:]       # (B,T,S) 各为

        h = torch.zeros(B_, D, S, device=x.device)  # 状态: 与T无关!
        outputs = []
        for t in range(T):
            A_bar = torch.exp(delta[:, t].unsqueeze(-1) * A)           # (B,D,S)
            B_bar = (delta[:, t].unsqueeze(-1) * Bv[:, t].unsqueeze(1)
                     * x[:, t].unsqueeze(-1))                          # (B,D,S)
            h = A_bar * h + B_bar               # 记忆更新
            outputs.append((h * Cv[:, t].unsqueeze(1)).sum(-1))        # (B,D)
        return torch.stack(outputs, dim=1)      # (B,T,D)


# ============================================================
# 3. Mamba块 (conv1d + 选择性SSM + 门控)
# ============================================================
class MambaBlock(nn.Module):
    """简化版Mamba块: in_proj → 因果conv1d → 选择性SSM ⊙ SiLU门 → out_proj
    conv1d给每个位置带上局部上下文 (Mamba-3用更好的离散化把它变成了可选项);
    门控稳定训练; D提供残差直通。
    """

    def __init__(self, d_model, d_state=16, d_expand=2):
        super().__init__()
        d_inner = d_expand * d_model
        self.d_inner = d_inner
        self.in_proj = nn.Linear(d_model, 2 * d_inner, bias=False)  # 主干 + 门
        self.conv1d = nn.Conv1d(d_inner, d_inner, kernel_size=4,
                                padding=3, groups=d_inner, bias=True)
        self.ssm = SelectiveSSM(d_inner, d_state)
        self.D = nn.Parameter(torch.ones(d_inner))                  # 残差直通
        self.out_proj = nn.Linear(d_inner, d_model, bias=False)

    def forward(self, x):
        B_, T, C = x.shape
        x_main, z = self.in_proj(x).chunk(2, dim=-1)     # (B,T,I) × 2
        # 因果卷积: 两侧pad后裁掉右侧 → 每个位置只看左边
        x_main = self.conv1d(x_main.transpose(1, 2))[..., :T].transpose(1, 2)
        x_main = F.silu(x_main)
        y = self.ssm(x_main) + x_main * self.D
        return self.out_proj(y * F.silu(z))              # 门控输出


# ============================================================
# 4. 混合堆叠: Mamba为主 + 注意力锚点
# ============================================================
class HybridStack(nn.Module):
    """Nemotron 3的思路: 88层里大部分是MoE+Mamba-2, 只在关键处插入
    少量注意力层做"全局锚点" (精确检索/远距离路由)。"""

    def __init__(self, d_model, num_heads, pattern):
        super().__init__()
        self.pattern = pattern
        self.layers = nn.ModuleList([
            MambaBlock(d_model) if p == "mamba" else CausalAttention(d_model, num_heads)
            for p in pattern
        ])

    def forward(self, x):
        for layer in self.layers:
            x = x + layer(x)  # 残差 (简化: 省略norm)
        return x


# ============================================================
# 演示
# ============================================================
def demo_mamba():
    d_model = 64
    block = MambaBlock(d_model, d_state=8)
    x = torch.randn(2, 32, d_model)
    out = block(x)
    params = sum(p.numel() for p in block.parameters())
    print(f"MambaBlock (d_model={d_model}, d_state=8):")
    print(f"  输入 {tuple(x.shape)} → 输出 {tuple(out.shape)}")
    print(f"  参数量: {params:,}")
    print(f"  状态大小: d_inner×d_state = {block.d_inner * 8} 维 ← 恒定, 不随序列长度增长")


def demo_hybrid():
    d_model, num_heads = 64, 4
    pattern = ["mamba"] * 5 + ["attn"] + ["mamba"] * 5 + ["attn"]
    model = HybridStack(d_model, num_heads, pattern)
    x = torch.randn(2, 64, d_model)
    out = model(x)
    n_attn = pattern.count("attn")
    print(f"\n混合堆叠 ({len(pattern)}层, 其中注意力锚点 {n_attn} 层):")
    print(f"  输入 {tuple(x.shape)} → 输出 {tuple(out.shape)}")
    print(f"  注意力层占 {n_attn / len(pattern):.0%} ← 远少于纯Transformer, 大部分序列建模走线性SSM")


def demo_efficiency():
    """每层状态的显存对比: 注意力KV Cache随T线性增长, Mamba状态恒定"""
    d_model, d_state, d_expand = 2048, 128, 2
    print(f"\n每层状态显存 (d_model={d_model}, d_state={d_state}):")
    print(f"  {'序列长度':>10s} {'Attention KV Cache':>20s} {'Mamba状态':>14s}")
    for T in [4096, 16384, 65536, 1048576]:
        attn = 2 * T * d_model * 2 / 1024**2               # K+V, fp16
        mamba = d_model * d_expand * d_state * 4 / 1024**2  # fp32, 与T无关
        print(f"  {T:>10d} {attn:>16.1f} MB {mamba:>11.1f} MB")
    print("  ↑ 1M token时: 注意力每层8GB × 全部层数; Mamba每层2MB")


def hybrid_overview():
    rows = [
        ("Mamba-1 (2023.12)", "选择性SSM + 硬件感知并行扫描"),
        ("Jamba (2024.3)", "首个生产级混合模型: 注意力:Mamba≈1:7"),
        ("Mamba-2 (2024.5)", "SSD对偶: 打通SSM与注意力的数学联系, 训练快2-8x"),
        ("Kimi Linear (2025)", "混合线性注意力, 长上下文推理大幅降本"),
        ("Nemotron 3 (2026)", "MoE + Mamba-2 + 注意力锚点, 1M上下文, 吞吐最高7.5x"),
        ("Mamba-3 (2026.3)", "指数梯形离散化+复数状态+MIMO, 长序列延迟仅1/7"),
    ]
    print("\n混合架构里程碑:")
    for name, desc in rows:
        print(f"  {name:20s} {desc}")


if __name__ == "__main__":
    print("=" * 60)
    print("1. Mamba块")
    print("=" * 60)
    demo_mamba()

    print("\n" + "=" * 60)
    print("2. 混合堆叠")
    print("=" * 60)
    demo_hybrid()

    print("\n" + "=" * 60)
    print("3. 显存对比")
    print("=" * 60)
    demo_efficiency()

    print("\n" + "=" * 60)
    print("4. 里程碑")
    print("=" * 60)
    hybrid_overview()
