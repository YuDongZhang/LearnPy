# 4. PyTorch框架示例

## PyTorch简介

PyTorch 是 Facebook 2016 年发布的深度学习框架：

- 动态计算图，Debug 方便
- Pythonic 设计，像写 Python 一样写深度学习
- 研究首选，论文复现容易
- GPU 加速支持

```bash
pip install torch torchvision torchaudio

# GPU 版本 (需要 CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 张量基础

```python
import torch

x = torch.tensor([1, 2, 3])
y = torch.randn(3, 4)    # 3x4 随机矩阵
z = torch.zeros(2, 3)

# 移到 GPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    x = x.to(device)
```

## 自动求导

PyTorch 的核心：autograd 自动计算梯度。

```python
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
z = y.sum()
z.backward()
print(x.grad)  # 梯度: [2, 4, 6]
```

## 构建神经网络

方法1：继承 nn.Module（标准方式）：

```python
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = x.view(-1, 784)        # 展平
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

model = Net()
```

方法2：nn.Sequential（简单堆叠）：

```python
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 10)
)
```

## 数据加载

```python
from torch.utils.data import DataLoader, TensorDataset

# 方式1: TensorDataset
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 方式2: torchvision 数据集
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = datasets.MNIST(root='./data', train=True,
                              download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
```

## 训练循环

PyTorch 训练的固定套路：

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    for inputs, labels in train_loader:
        outputs = model(inputs)          # 前向传播
        loss = criterion(outputs, labels)

        optimizer.zero_grad()            # 清零梯度
        loss.backward()                  # 反向传播
        optimizer.step()                 # 更新参数
```

## CNN示例

```python
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))  # Conv -> ReLU -> Pool
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)                 # 展平
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
```

## RNN/LSTM示例

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        embedded = self.embedding(x)              # (batch, seq_len, embed_dim)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        output = self.fc(hidden[-1])              # 最后一个隐藏状态
        return torch.sigmoid(output)
```

## GPU训练

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CNN().to(device)

for inputs, labels in train_loader:
    inputs, labels = inputs.to(device), labels.to(device)
    ...

# 多 GPU
model = nn.DataParallel(model)
```

## 模型保存和加载

```python
torch.save(model, 'model.pth')                     # 保存整个模型
torch.save(model.state_dict(), 'model_weights.pth') # 只保存权重（推荐）

model = CNN()
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()

# checkpoint：包含训练状态，可断点续训
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
```

## 迁移学习

```python
import torchvision.models as models

model = models.resnet18(pretrained=True)

# 冻结参数
for param in model.parameters():
    param.requires_grad = False

# 替换最后的全连接层
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 10)

# 解冻部分层微调
for param in model.layer4.parameters():
    param.requires_grad = True
```

## 完整示例：MNIST分类

```python
# 1. 数据
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# 2. 模型
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 3. 训练
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

# 4. 测试
model.eval()
correct = 0
with torch.no_grad():
    for data, target in test_loader:
        output = model(data)
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()

print(f'准确率: {100*correct/len(test_data):.2f}%')
```

## PyTorch Lightning

高级封装，省去手写训练循环：

```python
import pytorch_lightning as pl

class LitModel(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.functional.cross_entropy(y_hat, y)
        return loss

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=0.001)

trainer = pl.Trainer(max_epochs=10)
trainer.fit(LitModel(), train_loader)
```

## 代码

讲解对应的示例代码见 `4_pytorch_demo.py`。
