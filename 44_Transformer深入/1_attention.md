# 1. 注意力机制从零实现

## 注意力的直觉

注意力机制回答一个问题：**对于当前token，序列中哪些token最重要？**

类比：你在读一篇文章，读到"它"这个字时，你的注意力会回到前面找"它"指代的名词。

## Scaled Dot-Product Attention

核心公式：
```
Attention(Q, K, V) = softmax(Q × K^T / √d_k) × V
```

- Q（Query）：当前token的查询向量，"我在找什么"
- K（Key）：所有token的键向量，"我有什么"
- V（Value）：所有token的值向量，"我的内容是什么"
- d_k：Key的维度，用于缩放防止数值过大

## 计算步骤

```
1. 计算注意力分数: scores = Q × K^T
2. 缩放: scores = scores / √d_k
3. Mask（可选）: 遮住未来token（因果注意力）
4. Softmax: weights = softmax(scores)
5. 加权求和: output = weights × V
```

## 因果注意力（Causal Attention）

GPT等自回归模型使用因果注意力：每个token只能看到自己和之前的token，看不到未来。

用一个上三角mask实现：
```
mask = [[0, -inf, -inf],
        [0,    0, -inf],
        [0,    0,    0]]
```

## Multi-Head Attention

将Q、K、V分成多个"头"，每个头独立计算注意力，最后拼接：

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W_O

其中 head_i = Attention(Q × W_Q_i, K × W_K_i, V × W_V_i)
```

多头的好处：不同的头可以关注不同类型的关系（语法、语义、位置等）。

## 参数量

对于hidden_size=d, num_heads=h：
- W_Q, W_K, W_V, W_O 各一个 d×d 矩阵
- 总参数：4 × d²
