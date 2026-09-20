# 9. 高效注意力

## 问题：二次复杂度

标准注意力要物化 T×T 打分矩阵：

```
计算: O(T² × d)      T翻倍 → 计算4倍
显存: T×T 打分矩阵    seq=8192时 ≈ 1GB (fp32)
```

长上下文两大方向：**少算**（稀疏/窗口）和 **少存**（MLA，见第7章）。

## 滑动窗口注意力（SWA）

语言的大部分依赖是局部的 → 每个token只看最近window个：

```
可见mask = 因果 ∩ 最近window个（带状）

全注意力: T×T 次打分
SWA:     T×window 次打分；KV Cache滑窗淘汰旧token → 恒定显存
```

- Mistral引入（window=4096），Gemma分层混用（底层小窗口抓局部，顶层全注意力抓全局）

## Flash Attention：IO-aware

不动数学，只动实现。关键观察：注意力慢在显存读写（HBM），不在计算。

三个技巧：

1. **分块**：Q/K/V切块计算，从不物化完整T×T矩阵
2. **在线softmax**：softmax可分块增量计算
3. **驻留SRAM**：块算完不写回HBM

在线softmax（每读入一块K/V）：

```
m_new = max(m, block_max)            # 更新running max
l     = l × e^(m-m_new) + Σp         # 修正历史累积
out   = out × e^(m-m_new) + p·V      # 同上
```

因果场景还能整块跳过上三角。FA2/FA3在GPU上比naive快数倍且省显存——
收益主要在IO（少读写HBM），FLOP数并不变，"IO-aware"由此得名。

### 实际使用：一行SDPA

```python
out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
```

PyTorch 2.0+自动选后端（FlashAttention / memory-efficient / math）。
生产代码直接用它，不要手写注意力。

## 稀疏注意力：少算的极限

| 技术 | 思路 | 代表 |
|------|------|------|
| NSA原生稀疏 | 学习的块级Top-K + 窗口 | DeepSeek-V3 |
| DSA稀疏注意力 | 轻量indexer选关键token | DeepSeek-V3.2-Exp（API降价50%+） |
| 序列维度压缩 | 沿序列压缩KV | DeepSeek-V4（1M上下文） |

## 混合架构：换骨架

Mamba/SSM把历史压成**固定大小的状态**，线性复杂度、恒定显存：

- 纯SSM：检索能力弱——"快照"记不住"第几行第几个字"这类精确细节
- 混合：SSM层为主 + 少量注意力层做"锚点"（Nemotron 3、Kimi Linear、HunyuanTurboS）

Mamba-3（2026.3）：端到端延迟仅Transformer的1/7，混合版本在检索任务上超过纯Transformer。

## 总结

| 方向 | 技术 | 收益 |
|------|------|------|
| 少存 | GQA / MLA | KV Cache缩小4~80倍 |
| 少算 | SWA / 稀疏注意力 | 计算量接近线性 |
| IO | Flash Attention | 数倍加速（不省FLOP） |
| 换骨架 | SSM混合架构 | 推理吞吐数倍 |

## 代码

`9_efficient_attention.py`：SWA实现与可见性图、在线softmax分块版（与naive验证一致）、SDPA接口、稀疏/混合架构概览。
