"""
Transformer 原理详解
=================

介绍 Transformer 架构的原理和工作机制。
"""

print("=" * 60)
print("1. Transformer 简介")
print("=" * 60)

print("""
Transformer (2017, "Attention Is All You Need"):

• 完全基于注意力机制
• 摒弃了 RNN 的序列处理方式
• 可以并行计算, 大大提高训练速度
• 已成为 NLP 领域的主流架构

核心创新:
  • Self-Attention (自注意力)
  • Multi-Head Attention (多头注意力)
  • 位置编码 (Positional Encoding)

优势:
  ✓ 并行计算, 训练速度快
  ✓ 捕捉长距离依赖
  ✓ 可解释性强
  ✓ 迁移学习效果好
""")

print()
print("=" * 60)
print("2. 整体架构")
print("=" * 60)

print("""
Transformer 编码器结构:

  输入 → 嵌入 → 位置编码 → 多头注意力 → 残差&层归一化 → 前馈网络 → 输出

Transformer 解码器结构:

  输入 → 嵌入 → 位置编码 → 多头注意力(掩码) → 残差&层归一化 →
  编码器-解码器注意力 → 残差&层归一化 → 前馈网络 → 输出

关键组件:
  1. 嵌入层 (Embedding)
  2. 位置编码 (Positional Encoding)
  3. 多头注意力 (Multi-Head Attention)
  4. 残差连接 (Residual Connection)
  5. 层归一化 (Layer Normalization)
  6. 前馈网络 (Feed Forward Network)
""")

print()
print("=" * 60)
print("3. 自注意力机制")
print("=" * 60)

print("""
Self-Attention (自注意力):

核心思想: 计算序列中每个位置与其他位置的相关性

步骤:
  1. 对于每个词, 生成 Query, Key, Value 三个向量
  2. 计算 Query 与所有 Key 的相似度
  3. 使用 softmax 得到权重
  4. 加权求和得到输出

公式:
  Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V

Q (Query): 我要找什么
K (Key): 我有什么
V (Value): 我的实际内容

直观理解:
  当处理"bank"时:
  - 如果上下文有"river", "bank"指河岸
  - 如果上下文有"money", "bank"指银行
""")

print()
print("=" * 60)
print("4. 多头注意力")
print("=" * 60)

print("""
Multi-Head Attention:

并行执行多次注意力函数:
  1. 线性投影到 h 个不同的表示空间
  2. 在每个空间分别计算注意力
  3. 拼接结果并线性变换

MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O

其中:
  head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)

为什么要多头?
  • 关注不同类型的关系
  • 捕获多种语义信息
  • 例如: 语法关系、语义关系、位置关系

典型配置:
  • h = 8 (8 个头)
  • d_model = 512 (模型维度)
  • d_k = d_v = 64 (每个头的维度)
""")

print()
print("=" * 60)
print("5. 位置编码")
print("=" * 60)

print("""
Positional Encoding:

Transformer 没有循环结构, 需要显式添加位置信息

公式:
  PE_(pos, 2i) = sin(pos / 10000^(2i/d_model))
  PE_(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

特点:
  • 每个维度对应不同频率的正弦波
  • 可以表示相对位置
  • 偶数位置用 sin, 奇数位置用 cos

或者使用学习的位置嵌入:
  self.position_embedding = nn.Embedding(max_len, d_model)

为什么用正弦函数?
  • 可以表示相对位置
  • 任意位置可以通过线性变换得到
  • 外推到更长序列
""")

print()
print("=" * 60)
print("6. 残差与层归一化")
print("=" * 60)

print("""
残差连接 (Residual Connection):

  输出 = LayerNorm(x + Sublayer(x))

作用:
  • 缓解梯度消失
  • 允许梯度直接流回更早层
  • 训练更深的网络

层归一化 (Layer Normalization):

  LayerNorm(x) = γ * (x - μ) / σ + β

  μ = mean(x), σ = std(x)

与 Batch Normalization 的区别:
  • BN: 在 batch 维度归一化
  • LN: 在特征维度归一化
  • LN 更适合变长序列
""")

print()
print("=" * 60)
print("7. 前馈网络")
print("=" * 60)

print("""
Feed Forward Network (FFN):

位置-wise (对每个位置分别处理):
  FFN(x) = max(0, xW_1 + b_1) W_2 + b_2

典型配置:
  • 两层全连接
  • 中间层维度通常是输入的 4 倍
  • 激活函数: ReLU / GELU

作用:
  • 提供非线性变换
  • 增加模型容量
  • 对每个位置独立处理

代码实现:
  nn.Sequential(
      nn.Linear(d_model, d_ff),
      nn.ReLU(),
      nn.Linear(d_ff, d_model)
  )
""")

print()
print("=" * 60)
print("8. 编码器 vs 解码器")
print("=" * 60)

print("""
编码器 (Encoder):

  • N = 6 层
  • 每层: Multi-Head Attention + FFN
  • 残差连接 + 层归一化
  • 输入序列全部同时处理

解码器 (Decoder):

  • N = 6 层
  • 每层:
    1. Masked Multi-Head Attention (掩码)
    2. Encoder-Decoder Attention
    3. FFN
  • 自回归生成 (逐步预测)

掩码 (Masking):
  • Padding Mask: 忽略 padding
  • Look-ahead Mask: 看不到未来位置
""")

print()
print("=" * 60)
print("9. 训练技巧")
print("=" * 60)

print("""
9.1 标签平滑 (Label Smoothing)

  • 防止模型过度自信
  • 平滑系数: 0.1
  • 真实标签概率: 1 - ε
  • 其他标签: ε / (vocab_size - 1)

9.2 梯度裁剪 (Gradient Clipping)

  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

9.3 学习率调度

  使用 Warm-up:
  lr = d_model^(-0.5) * min(step^(-0.5), step * warmup_steps^(-1.5))

9.4 优化器

  Adam with β1=0.9, β2=0.98, ε=10^(-9)

9.5 正则化

  • Dropout: 0.1
  • 在每个子层输出前应用
""")

print()
print("=" * 60)
print("10. 经典 Transformer 模型")
print("=" * 60)

print("""
10.1 BERT (Bidirectional Encoder Representations)

  • 只使用编码器
  • 双向注意力
  • 预训练: Masked LM + Next Sentence Prediction
  • 适合: 分类、序列标注、问答

10.2 GPT (Generative Pre-training)

  • 只使用解码器
  • 单向注意力 (从左到右)
  • 预训练: Language Modeling
  • 适合: 文本生成

10.3 T5 (Text-to-Text Transfer Transformer)

  • 编码器-解码器结构
  • 统一框架: 所有任务转为 text-to-text
  • 适合: 翻译、摘要、问答

10.4 BART (Bidirectional and Auto-Regressive)

  • 编码器-解码器
  • 降噪自编码器
  • 适合: 文本生成
""")

print()
print("=" * 60)
print("11. 代码实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() *
                            -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_k = d_model // num_heads
        self.num_heads = num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch_size = x.size(0)

        Q = self.W_q(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn = torch.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        output = torch.matmul(attn, V)
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        return self.W_o(output)

class TransformerLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        attn_output = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        ffn_output = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_output))
        return x
''')

print()
print("=" * 60)
print("12. Transformer vs RNN")
print("=" * 60)

print("""
Transformer vs RNN/LSTM:

| 方面        | Transformer      | RNN/LSTM        |
|-------------|-----------------|-----------------|
| 并行计算    | ✓ 完全并行      | ✗ 序列依赖      |
| 长距离依赖  | ✓ O(1)          | ✗ O(n)          |
| 计算复杂度  | O(n²·d)         | O(n·d²)         |
| 内存        | O(n²)           | O(n·d)          |
| 训练速度    | 快               | 慢               |
| 可解释性    | 强 (注意力权重) | 弱               |

适用场景:

Transformer 适合:
  • 需要捕捉长距离依赖
  • 大规模数据
  • 需要并行训练
  • 分类、翻译、生成

RNN 适合:
  • 资源受限
  • 实时流数据
  • 小规模数据
""")
