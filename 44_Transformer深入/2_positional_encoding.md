# 2. 位置编码

## 为什么需要位置编码

Attention本身是置换不变的——打乱输入顺序，输出不变。但语言是有顺序的，"狗咬人"和"人咬狗"意思完全不同。位置编码给每个token注入位置信息。

## 绝对位置编码（Sinusoidal）

原始Transformer使用正弦/余弦函数：
```
PE(pos, 2i)   = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

特点：
- 不需要学习，直接计算
- 理论上可以外推到更长序列
- 实际外推效果一般

## 可学习位置编码

GPT-2/BERT使用可学习的位置嵌入：
```python
position_embedding = nn.Embedding(max_seq_len, d_model)
```

特点：
- 效果好
- 不能外推（超过训练长度就不行）

## 旋转位置编码（RoPE）

LLaMA、Qwen等主流LLM使用RoPE：

核心思想：通过旋转矩阵将位置信息编码到Q和K中，使得注意力分数只依赖于相对位置。

```
q_rotated = rotate(q, pos_q)
k_rotated = rotate(k, pos_k)
score = q_rotated · k_rotated  # 只依赖 pos_q - pos_k
```

优势：
- 天然支持相对位置
- 外推性好
- 当前最主流的方案

## ALiBi

不修改Q/K，直接在注意力分数上加位置偏置：
```
score = Q·K^T - m × |i-j|
```
m是每个头不同的斜率。简单高效，外推性好。

## 位置编码对比

| 方法 | 类型 | 外推性 | 使用模型 |
|------|------|--------|---------|
| Sinusoidal | 绝对 | 一般 | 原始Transformer |
| Learned | 绝对 | 差 | GPT-2, BERT |
| RoPE | 相对 | 好 | LLaMA, Qwen, Mistral |
| ALiBi | 相对 | 好 | BLOOM, MPT |
