"""
PyTorch 框架示例
==============

PyTorch 是 Facebook 开发的深度学习框架。
由于环境中未安装 PyTorch，以下为示例代码展示。
"""

print("=" * 60)
print("1. PyTorch 简介")
print("=" * 60)

print("""
PyTorch 特点:
  • 2016年 Facebook 发布
  • 动态计算图 (Debug 方便)
  • Pythonic 设计 (像写 Python 一样写 DL)
  • 研究首选 (论文复现容易)
  • GPU 加速支持
  • 越来越多人使用

安装:
  pip install torch torchvision torchaudio

验证:
  import torch
  print(torch.__version__)

GPU 版本 (需要 CUDA):
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
""")

print()
print("=" * 60)
print("2. PyTorch 基础")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim

# 创建张量
x = torch.tensor([1, 2, 3])
y = torch.randn(3, 4)  # 3x4 随机矩阵
z = torch.zeros(2, 3)  # 2x3 零矩阵

# 张量操作
a = torch.add(x, x)
b = torch.matmul(x, y.t())

# 移到 GPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    x = x.to(device)

# 自动求导
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
z = y.sum()
z.backward()
print(x.grad)  # 梯度: [2, 4, 6]
''')

print()
print("=" * 60)
print("3. 构建神经网络")
print("=" * 60)

print('''
import torch.nn as nn

# 方法1: 继承 nn.Module
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = x.view(-1, 784)  # 展平
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

model = Net()
print(model)

# 方法2: 使用 nn.Sequential
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 10)
)

# 查看参数
for param in model.parameters():
    print(param.shape)
''')

print()
print("=" * 60)
print("4. 数据加载")
print("=" * 60)

print('''
from torch.utils.data import DataLoader, TensorDataset

# 方式1: 使用 TensorDataset
X = torch.randn(1000, 784)
y = torch.randint(0, 10, (1000,))
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 方式2: 使用 torchvision 数据集
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = datasets.MNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.MNIST(
    root='./data',
    train=False,
    transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
''')

print()
print("=" * 60)
print("5. 训练循环")
print("=" * 60)

print('''
# 损失函数
criterion = nn.CrossEntropyLoss()

# 优化器
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练循环
for epoch in range(10):
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader):
        # 前向传播
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 100 == 99:
            print(f'[{epoch + 1}, {i + 1}] loss: {running_loss / 100:.3f}')
            running_loss = 0.0

print('Training finished!')
''')

print()
print("=" * 60)
print("6. CNN 卷积神经网络")
print("=" * 60)

print('''
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # 卷积层
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)

        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Conv -> ReLU -> Pool
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))

        # 展平
        x = x.view(-1, 64 * 7 * 7)

        # 全连接
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

model = CNN()
print(model)
''')

print()
print("=" * 60)
print("7. RNN/LSTM")
print("=" * 60)

print('''
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)

        lstm_out, (hidden, cell) = self.lstm(embedded)

        # 使用最后一个隐藏状态
        output = self.fc(hidden[-1])
        return torch.sigmoid(output)

# 或使用 GRU
class GRUClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        embedded = self.embedding(x)
        _, hidden = self.gru(embedded)
        output = self.fc(hidden[-1])
        return torch.sigmoid(output)
''')

print()
print("=" * 60)
print("8. GPU 训练")
print("=" * 60)

print('''
# 检查 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# 移动模型和数据到 GPU
model = CNN().to(device)

# 训练循环中使用
for inputs, labels in train_loader:
    inputs, labels = inputs.to(device), labels.to(device)

    outputs = model(inputs)
    loss = criterion(outputs, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# 多 GPU 训练
model = nn.DataParallel(model)
''')

print()
print("=" * 60)
print("9. 模型保存和加载")
print("=" * 60)

print('''
# 保存整个模型
torch.save(model, 'model.pth')

# 保存模型权重 (推荐)
torch.save(model.state_dict(), 'model_weights.pth')

# 加载模型
model = CNN()
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()

# 加载到 GPU
model.load_state_dict(torch.load('model_weights.pth', map_location='cuda:0'))

# 保存和加载优化器状态
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pth')

# 加载 checkpoint
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
''')

print()
print("=" * 60)
print("10. 迁移学习")
print("=" * 60)

print('''
import torchvision.models as models

# 使用预训练模型 (ResNet)
model = models.resnet18(pretrained=True)

# 冻结参数
for param in model.parameters():
    param.requires_grad = False

# 修改最后的全连接层
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 10)  # 10 分类

# 解冻后微调
for param in model.layer4.parameters():
    param.requires_grad = True

# 使用不同的优化器只更新新层
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# 其他预训练模型
vgg16 = models.vgg16(pretrained=True)
efficientnet = models.efficientnet_b0(pretrained=True)
''')

print()
print("=" * 60)
print("11. 完整示例: MNIST 分类")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 1. 数据加载
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST('./data', train=False, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# 2. 定义模型
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = torch.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return x

model = Net()

# 3. 训练
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
    print(f'Epoch {epoch+1} completed')

# 4. 测试
model.eval()
correct = 0
with torch.no_grad():
    for data, target in test_loader:
        output = model(data)
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()

print(f'准确率: {100*correct/len(test_data):.2f}%')
''')

print()
print("=" * 60)
print("12. PyTorch Lightning 简化训练")
print("=" * 60)

print('''
# PyTorch Lightning 高级封装
import pytorch_lightning as pl

class LitModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.functional.cross_entropy(y_hat, y)
        return loss

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=0.001)

# 训练
trainer = pl.Trainer(max_epochs=10)
model = LitModel()
trainer.fit(model, train_loader)
''')
