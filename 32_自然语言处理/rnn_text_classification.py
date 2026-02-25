"""
RNN/LSTM 文本分类
==============

使用循环神经网络 (RNN/LSTM) 进行文本分类。
由于环境中未安装 PyTorch/TensorFlow，以下为示例代码展示。
"""

print("=" * 60)
print("1. RNN 简介")
print("=" * 60)

print("""
循环神经网络 (Recurrent Neural Network, RNN):

为什么需要 RNN?
  • 传统神经网络: 输入输出独立
  • RNN: 能够处理序列数据
  • 记住之前的信息

RNN 结构:
  • 每个时间步处理一个输入
  • 隐藏状态在时间步之间传递
  • 公式: h_t = f(W * h_{t-1} + U * x_t)

RNN 的问题:
  • 梯度消失/爆炸
  • 长期依赖问题
  • 难以记住远距离信息
""")

print()
print("=" * 60)
print("2. LSTM 原理")
print("=" * 60)

print("""
长短期记忆网络 (Long Short-Term Memory, LSTM):

LSTM 引入门控机制:
  • 遗忘门: 决定丢弃什么信息
  • 输入门: 决定存储什么信息
  • 输出门: 决定输出什么信息

公式:
  f_t = σ(W_f * [h_{t-1}, x_t] + b_f)   # 遗忘门
  i_t = σ(W_i * [h_{t-1}, x_t] + b_i)   # 输入门
  C̃_t = tanh(W_C * [h_{t-1}, x_t] + b_C)  # 候选值
  C_t = f_t * C_{t-1} + i_t * C̃_t       # 更新细胞状态
  o_t = σ(W_o * [h_{t-1}, x_t] + b_o)   # 输出门
  h_t = o_t * tanh(C_t)                  # 输出

GRU (Gated Recurrent Unit):
  • 更新门: 合并遗忘门和输入门
  • 重置门: 决定忽略多少过去的信息
  • 参数量更少, 训练更快
""")

print()
print("=" * 60)
print("3. 文本分类任务")
print("=" * 60)

print("""
文本分类: 将文本分为不同类别

示例:
  • 情感分析: 正面 / 负面
  • 主题分类: 科技 / 体育 / 娱乐
  • 垃圾邮件检测: 垃圾 / 正常

流程:
  1. 文本预处理
  2. 词嵌入 (Word Embedding)
  3. RNN/LSTM 编码
  4. 全连接层分类
  5. Softmax 输出
""")

print()
print("=" * 60)
print("4. PyTorch 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn

class TextRNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(TextRNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        # x: (batch_size, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)

        output, hidden = self.rnn(embedded)
        # output: (batch, seq_len, hidden_dim)
        # hidden: (1, batch, hidden_dim)

        # 使用最后一个隐藏状态
        last_hidden = hidden.squeeze(0)
        logits = self.fc(last_hidden)
        return logits

# LSTM 版本
class TextLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(TextLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 for bidirectional

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # 双向 LSTM: 拼接最后隐藏状态
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        logits = self.fc(hidden)
        return logits

# GRU 版本
class TextGRU(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(TextGRU, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        _, hidden = self.gru(embedded)
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        return self.fc(hidden)
''')

print()
print("=" * 60)
print("5. 数据准备")
print("=" * 60)

print('''
from torch.utils.data import Dataset, DataLoader
import torch

class TextDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len=128):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # 文本转索引
        tokens = text.split()[:self.max_len]
        indices = [self.vocab.get(token, self.vocab["<UNK>"]) for token in tokens]

        # Padding
        if len(indices) < self.max_len:
            indices += [self.vocab["<PAD>"]] * (self.max_len - len(indices))

        return torch.tensor(indices), torch.tensor(label)

# 构建词表
def build_vocab(texts, min_freq=2):
    word_count = {}
    for text in texts:
        for word in text.split():
            word_count[word] = word_count.get(word, 0) + 1

    vocab = {"<PAD>": 0, "<UNK>": 1}
    for word, count in word_count.items():
        if count >= min_freq:
            vocab[word] = len(vocab)

    return vocab

# 使用示例
texts = ["I love this movie", "This is a bad movie", "Great film"]
labels = [1, 0, 1]  # 1: 正面, 0: 负面

vocab = build_vocab(texts)
dataset = TextDataset(texts, labels, vocab)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
''')

print()
print("=" * 60)
print("6. 训练流程")
print("=" * 60)

print('''
import torch.optim as optim

# 超参数
VOCAB_SIZE = 10000
EMBED_DIM = 128
HIDDEN_DIM = 128
NUM_CLASSES = 2
LEARNING_RATE = 0.001

# 模型
model = TextLSTM(VOCAB_SIZE, EMBED_DIM, HIDDEN_DIM, NUM_CLASSES)

# 损失和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# 训练
def train_epoch(model, dataloader, criterion, optimizer):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for texts, labels in dataloader:
        texts = texts.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(texts)
        loss = criterion(outputs, labels)

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    return total_loss / len(dataloader), 100. * correct / total

# 训练循环
for epoch in range(10):
    loss, acc = train_epoch(model, dataloader, criterion, optimizer)
    print(f"Epoch {epoch+1}: Loss={loss:.4f}, Acc={acc:.2f}%")
''')

print()
print("=" * 60)
print("7. 使用预训练词向量")
print("=" * 60)

print('''
import gensim.downloader as api

# 加载预训练词向量
print("Loading pre-trained vectors...")
word_vectors = api.load("glove-wiki-gigaword-100")

# 使用预训练向量初始化 embedding
pretrained_vectors = torch.randn(VOCAB_SIZE, 100)
for word, idx in vocab.items():
    if word in word_vectors:
        pretrained_vectors[idx] = torch.tensor(word_vectors[word])

# 冻结或微调
embedding = nn.Embedding.from_pretrained(pretrained_vectors, freeze=False)

# 或者使用 nn.Embedding 初始化
embedding = nn.Embedding(VOCAB_SIZE, 100)
embedding.weight.data.copy_(pretrained_vectors)
''')

print()
print("=" * 60)
print("8. 注意力机制")
print("=" * 60)

print('''
class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1)

    def forward(self, lstm_output):
        # lstm_output: (batch, seq_len, hidden_dim)
        attention_weights = torch.softmax(self.attention(lstm_output), dim=1)
        # 加权求和
        context = torch.sum(attention_weights * lstm_output, dim=1)
        return context

class TextLSTMWithAttention(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(TextLSTMWithAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.attention = Attention(hidden_dim)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        context = self.attention(lstm_out)
        return self.fc(context)
''')

print()
print("=" * 60)
print("9. 双向 LSTM")
print("=" * 60)

print('''
class BiLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes, num_layers=2):
        super(BiLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=0.3
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)

        # 双向: 拼接最后两层隐藏状态
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.fc(hidden)

# Mask 机制 (忽略 padding)
class MaskedLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(MaskedLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x, mask=None):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)

        if mask is not None:
            # 使用 mask 忽略 padding 的影响
            hidden = hidden * mask.unsqueeze(-1)

        return self.fc(hidden.squeeze(0))
''')

print()
print("=" * 60)
print("10. 实战: 情感分析")
print("=" * 60)

print('''
# 完整情感分析示例

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# 1. 数据
train_data = [
    ("I love this product", 1),
    ("This is amazing", 1),
    ("Great experience", 1),
    ("Terrible quality", 0),
    ("Very bad", 0),
    ("Not recommended", 0),
]

# 2. 简单词表
word2idx = {"<PAD>": 0, "<UNK>": 1}
for text, _ in train_data:
    for word in text.lower().split():
        if word not in word2idx:
            word2idx[word] = len(word2idx)

# 3. 数据集
class SentimentDataset(Dataset):
    def __init__(self, data, word2idx, max_len=20):
        self.data = data
        self.word2idx = word2idx
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text, label = self.data[idx]
        indices = [self.word2idx.get(w, 1) for w in text.lower().split()[:self.max_len]]
        indices += [0] * (self.max_len - len(indices))
        return torch.tensor(indices), torch.tensor(label)

# 4. 模型
class SimpleLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super(SimpleLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 2)

    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, _) = self.lstm(embedded)
        return self.fc(hidden.squeeze(0))

# 5. 训练
dataset = SentimentDataset(train_data, word2idx)
loader = DataLoader(dataset, batch_size=2)

model = SimpleLSTM(len(word2idx), 64, 64)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

for epoch in range(50):
    for texts, labels in loader:
        outputs = model(texts)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# 6. 预测
def predict(text):
    indices = [word2idx.get(w, 1) for w in text.lower().split()[:20]]
    indices += [0] * (20 - len(indices))
    tensor = torch.tensor([indices])
    output = model(tensor)
    pred = output.argmax(1).item()
    return "Positive" if pred == 1 else "Negative"

print(predict("I really love this"))
print(predict("This is terrible"))
''')

print()
print("=" * 60)
print("11. 模型评估")
print("=" * 60)

print('''
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

def evaluate(model, dataloader):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for texts, labels in dataloader:
            outputs = model(texts)
            preds = outputs.argmax(1).numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.numpy())

    print("分类报告:")
    print(classification_report(all_labels, all_preds))

    print("混淆矩阵:")
    print(confusion_matrix(all_labels, all_preds))

    # 计算各项指标
    accuracy = (np.array(all_preds) == np.array(all_labels)).mean()
    return accuracy
''')

print()
print("=" * 60)
print("12. RNN/LSTM 总结")
print("=" * 60)

print("""
RNN/LSTM 文本分类要点:

✓ 优点:
  • 能够处理变长序列
  • 捕捉时序依赖
  • 适合文本、语音等序列数据

✗ 缺点:
  • 训练慢 (难以并行)
  • 梯度消失问题
  • 长序列效果下降

✓ 改进:
  • LSTM/GRU 解决梯度问题
  • 双向 LSTM 增强上下文
  • 注意力机制聚焦重点
  • 预训练词向量提升效果

🔄 现代方法:
  • Transformer (后续章节)
  • BERT 等预训练模型
  • 大多数任务已被 Transformer 超越
""")
