# 4. Transformer原理

## 简介

Transformer 出自 2017 年论文《Attention Is All You Need》：

- 完全基于注意力机制，摒弃 RNN 的序列处理方式
- 可以并行计算，大大提高训练速度
- 已成为 NLP 领域的主流架构

核心创新：Self-Attention（自注意力）、Multi-Head Attention（多头注意力）、Positional Encoding（位置编码）。

## 整体架构

```
编码器: 输入 → 嵌入 → 位置编码 → 多头注意力 → 残差&层归一化 → 前馈网络 → 输出

解码器: 输入 → 嵌入 → 位置编码 → 多头注意力(掩码) → 残差&层归一化
        → 编码器-解码器注意力 → 残差&层归一化 → 前馈网络 → 输出
```

关键组件：嵌入层、位置编码、多头注意力、残差连接、层归一化、前馈网络。

## 自注意力机制

核心思想：计算序列中每个位置与其他位置的相关性。

步骤：
1. 对每个词生成 Query、Key、Value 三个向量
2. 计算 Query 与所有 Key 的相似度
3. softmax 得到权重
4. 加权求和得到输出

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
```

直观理解 Q/K/V：
- Q (Query)：我要找什么
- K (Key)：我有什么
- V (Value)：我的实际内容

例如处理 "bank" 时：上下文有 "river" 则指河岸，有 "money" 则指银行。

## 多头注意力

并行执行多次注意力：线性投影到 h 个不同子空间，分别计算注意力，拼接后再线性变换。

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

为什么要多头？关注不同类型的关系（语法、语义、位置）。

典型配置：h=8 个头，d_model=512，d_k=d_v=64。

## 位置编码

Transformer 没有循环结构，需要显式添加位置信息：

```
PE_(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE_(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

- 每个维度对应不同频率的正弦波
- 可以表示相对位置，能外推到更长序列

也可以使用可学习的位置嵌入：`nn.Embedding(max_len, d_model)`。

## 残差与层归一化

```
输出 = LayerNorm(x + Sublayer(x))
```

- 残差连接：缓解梯度消失，允许训练更深的网络
- 层归一化：`LayerNorm(x) = γ · (x - μ)/σ + β`

LN vs BN：BN 在 batch 维度归一化，LN 在特征维度归一化。LN 更适合变长序列。

## 前馈网络

对每个位置独立处理的两层全连接：

```
FFN(x) = max(0, xW_1 + b_1) W_2 + b_2
```

中间层维度通常是输入的 4 倍，激活函数 ReLU/GELU，作用是提供非线性、增加模型容量。

## 编码器 vs 解码器

| 组件 | 编码器 | 解码器 |
|------|--------|--------|
| 层数 | N=6 | N=6 |
| 注意力 | 双向（全部同时处理） | Masked（自回归逐步生成） |
| 额外结构 | 无 | Encoder-Decoder Attention |

两种掩码：
- Padding Mask：忽略 padding
- Look-ahead Mask：看不到未来位置

## 训练技巧

- 标签平滑（ε=0.1）：防止模型过度自信
- 梯度裁剪：`clip_grad_norm_(params, max_norm=1.0)`
- Warm-up 学习率调度
- Adam 优化器（β2=0.98）
- Dropout 0.1

## 经典Transformer模型

| 模型 | 结构 | 预训练任务 | 适合 |
|------|------|-----------|------|
| BERT | 仅编码器 | Masked LM + NSP | 分类、序列标注、问答 |
| GPT | 仅解码器 | 语言模型 | 文本生成 |
| T5 | 编码器-解码器 | Text-to-Text | 翻译、摘要、问答 |
| BART | 编码器-解码器 | 降噪自编码器 | 文本生成 |

## Transformer vs RNN

| 方面 | Transformer | RNN/LSTM |
|------|-------------|----------|
| 并行计算 | ✓ 完全并行 | ✗ 序列依赖 |
| 长距离依赖 | ✓ O(1) | ✗ O(n) |
| 计算复杂度 | O(n²·d) | O(n·d²) |
| 训练速度 | 快 | 慢 |
| 可解释性 | 强（注意力权重） | 弱 |

Transformer 适合大规模数据和长距离依赖；RNN 适合资源受限、实时流数据、小规模数据。

## 代码

讲解对应的示例代码见 `4_transformer_intro.py`。
