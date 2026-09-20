# 3. RNN/LSTM文本分类

## 为什么需要RNN

- 传统神经网络：输入输出相互独立
- RNN（循环神经网络）：能够处理序列数据，记住之前的信息

核心结构：每个时间步处理一个输入，隐藏状态在时间步之间传递：

```
h_t = f(W * h_{t-1} + U * x_t)
```

RNN 的问题：梯度消失/爆炸、长期依赖问题（难以记住远距离信息）。

## LSTM原理

LSTM（长短期记忆网络）引入门控机制：

| 门 | 作用 |
|----|------|
| 遗忘门 f_t | 决定丢弃什么旧信息 |
| 输入门 i_t | 决定存储什么新信息 |
| 输出门 o_t | 决定输出什么信息 |

```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)    # 遗忘门
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)    # 输入门
C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C) # 候选值
C_t = f_t * C_{t-1} + i_t * C̃_t        # 更新细胞状态
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)    # 输出门
h_t = o_t * tanh(C_t)                   # 输出
```

**GRU**（门控循环单元）是 LSTM 的简化版：更新门合并遗忘门和输入门，重置门决定忽略多少过去信息。参数更少，训练更快。

## 文本分类流程

```
1. 文本预处理 → 2. 词嵌入 → 3. RNN/LSTM 编码 → 4. 全连接层 → 5. Softmax 输出
```

常见任务：情感分析（正面/负面）、主题分类（科技/体育/娱乐）、垃圾邮件检测。

## PyTorch实现

```python
import torch
import torch.nn as nn

class TextLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(TextLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim,
                            batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 双向

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # 双向 LSTM: 拼接最后隐藏状态
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        return self.fc(hidden)
```

RNN/GRU 版本只需替换 `nn.RNN` / `nn.GRU`。

## 数据准备

文本要先转成索引序列并 padding 对齐：

```python
def build_vocab(texts, min_freq=2):
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for word, count in count_words(texts).items():
        if count >= min_freq:
            vocab[word] = len(vocab)
    return vocab

# 文本 → 索引，不足 max_len 用 <PAD> 补齐
indices = [vocab.get(token, vocab["<UNK>"]) for token in tokens]
indices += [vocab["<PAD>"]] * (max_len - len(indices))
```

## 训练要点

- 损失函数：`nn.CrossEntropyLoss()`
- 优化器：Adam (lr=0.001)
- 梯度裁剪：`torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)`，防止梯度爆炸
- 评估：classification_report + 混淆矩阵

## 使用预训练词向量

```python
import gensim.downloader as api

word_vectors = api.load("glove-wiki-gigaword-100")

# 用预训练向量初始化 embedding
pretrained_vectors = torch.randn(VOCAB_SIZE, 100)
for word, idx in vocab.items():
    if word in word_vectors:
        pretrained_vectors[idx] = torch.tensor(word_vectors[word])

embedding = nn.Embedding.from_pretrained(pretrained_vectors, freeze=False)
```

## 注意力机制

让模型聚焦重要词，而不是只看最后一个隐藏状态：

```python
class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1)

    def forward(self, lstm_output):
        # (batch, seq_len, hidden_dim)
        weights = torch.softmax(self.attention(lstm_output), dim=1)
        context = torch.sum(weights * lstm_output, dim=1)  # 加权求和
        return context
```

## RNN/LSTM总结

| 方面 | 说明 |
|------|------|
| 优点 | 处理变长序列、捕捉时序依赖 |
| 缺点 | 训练慢（难以并行）、长序列效果下降 |
| 改进 | LSTM/GRU 解决梯度问题、双向增强上下文、注意力聚焦重点 |

现代方法：大多数任务已被 Transformer 和 BERT 等预训练模型超越（见下一节）。

## 代码

讲解对应的示例代码见 `3_rnn_text_classification.py`。
