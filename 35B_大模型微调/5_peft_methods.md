# 5. 其他PEFT方法

## PEFT概述

PEFT（Parameter-Efficient Fine-Tuning）是参数高效微调方法的统称。除了LoRA，还有多种方法，各有适用场景。

## P-Tuning v2

### 原理
在模型每一层的注意力机制前加入可训练的前缀向量（Prefix），冻结原模型参数。

```
原始: Attention(Q, K, V)
P-Tuning v2: Attention([Prefix_K; K], [Prefix_V; V], Q)
```

### 特点
- 每层都加前缀，效果比P-Tuning v1好很多
- 参数量约占原模型1%
- 对NLU任务（分类、抽取）效果好
- ChatGLM系列推荐使用

### 关键参数
| 参数 | 说明 | 常用值 |
|------|------|--------|
| num_virtual_tokens | 虚拟token数量 | 10-128 |
| encoder_hidden_size | 编码器隐藏层大小 | 128-256 |

## Prefix Tuning

### 原理
在输入序列前加可训练的前缀向量，只训练前缀参数。

### 与P-Tuning v2的区别
- Prefix Tuning只在输入层加前缀
- P-Tuning v2在每一层都加
- P-Tuning v2效果通常更好

## Adapter

### 原理
在Transformer的每一层中插入小型适配网络（Adapter Layer）：

```
原始层输出 → Adapter(下投影 → 激活 → 上投影) → 残差连接
```

### 特点
- 参数量约1-5%
- 推理时有额外计算开销（不像LoRA可以合并）
- 早期PEFT方法，现在用得较少

## IA3

### 原理
通过学习三个缩放向量来调整注意力层的Key、Value和FFN层的输出。

### 特点
- 参数量极小（比LoRA还少）
- 效果略逊于LoRA
- 适合参数预算极低的场景

## 方法对比

| 方法 | 参数量 | 效果 | 推理开销 | 适用场景 |
|------|--------|------|---------|---------|
| LoRA | ~0.1% | 很好 | 可合并无开销 | 通用，最推荐 |
| QLoRA | ~0.1% | 很好 | 可合并无开销 | 显存受限 |
| P-Tuning v2 | ~1% | 好 | 有少量开销 | NLU任务、ChatGLM |
| Prefix Tuning | ~1% | 中等 | 有少量开销 | 生成任务 |
| Adapter | 1-5% | 好 | 有开销 | 多任务切换 |
| IA3 | <0.1% | 中等 | 可合并 | 极低预算 |

## 如何选择

```
显存充足 + 追求最佳效果 → 全量微调
通用场景 → LoRA（首选）
显存紧张 → QLoRA
ChatGLM系列 → P-Tuning v2
需要极小参数 → IA3
```

大多数情况下，LoRA/QLoRA是最佳选择。
