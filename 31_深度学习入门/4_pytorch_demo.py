"""
PyTorch 框架示例
==============

PyTorch 是 Facebook 开发的深度学习框架, 本文件所有代码真实运行。

数据集使用 sklearn 自带的 digits (8x8 手写数字, 离线可用),
避免首次运行时下载 MNIST。
"""

import os
import tempfile

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

print("=" * 60)
print(f"1. 环境: PyTorch {torch.__version__}")
print("=" * 60)
print(f"CUDA available: {torch.cuda.is_available()}  (CPU 版, 本示例在 CPU 上运行)")

x = torch.tensor([1, 2, 3])
print(f"张量: {x.tolist()}, dtype={x.dtype}, shape={tuple(x.shape)}")
print(f"随机矩阵 (3x4):\n{torch.randn(3, 4).round(decimals=2).numpy()}")

print()
print("=" * 60)
print("2. 自动求导 (autograd)")
print("=" * 60)

t = torch.tensor(3.0, requires_grad=True)
y = t ** 2                       # y = t², 导数 2t
y.backward()
print(f"y = x², x = {t.item()}")
print(f"dy/dx = {t.grad.item()}  (理论值 2x = 6.0)")

print()
print("=" * 60)
print("3. 定义网络 (nn.Module)")
print("=" * 60)


class Net(nn.Module):
    """64 -> 128 -> 10"""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)


model = Net()
print(model)
print(f"参数量: {sum(p.numel() for p in model.parameters()):,}")

print()
print("=" * 60)
print("4. 数据加载 (DataLoader)")
print("=" * 60)

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()
X = digits.data.astype("float32") / 16.0
y = digits.target.astype("int64")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train_ds = TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train))
test_ds = TensorDataset(torch.from_numpy(X_test), torch.from_numpy(y_test))
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=256)

print(f"训练集 {len(train_ds)} 条 / 测试集 {len(test_ds)} 条")
print(f"训练集 batch 数: {len(train_loader)} (batch_size=64)")

print()
print("=" * 60)
print("5. 训练循环")
print("=" * 60)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(1, 11):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        outputs = model(inputs)            # 前向传播
        loss = criterion(outputs, labels)

        optimizer.zero_grad()              # 清零梯度
        loss.backward()                    # 反向传播
        optimizer.step()                   # 更新参数

        running_loss += loss.item()

    if epoch in (1, 3, 5, 10):
        print(f"  epoch {epoch:2d}: 平均 loss = {running_loss / len(train_loader):.4f}")

print()
print("=" * 60)
print("6. 评估")
print("=" * 60)

model.eval()
correct = total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        preds = model(inputs).argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
print(f"测试集准确率: {correct / total:.2%}")

print()
print("=" * 60)
print("7. CNN (8x8 图片)")
print("=" * 60)


class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(32 * 2 * 2, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))   # 8x8 -> 4x4
        x = self.pool(torch.relu(self.conv2(x)))   # 4x4 -> 2x2
        x = torch.flatten(x, 1)
        return self.fc(x)


cnn = CNN()
with torch.no_grad():
    sample = torch.randn(4, 1, 8, 8)
    print(f"  输入:       {tuple(sample.shape)}")
    sample = torch.relu(cnn.conv1(sample))
    print(f"  经过 conv1: {tuple(sample.shape)}")
    sample = cnn.pool(sample)
    print(f"  经过 pool:  {tuple(sample.shape)}")
    sample = torch.relu(cnn.conv2(sample))
    print(f"  经过 conv2: {tuple(sample.shape)}")
    sample = cnn.pool(sample)
    print(f"  经过 pool:  {tuple(sample.shape)}")
    sample = torch.flatten(sample, 1)
    print(f"  展平后:     {tuple(sample.shape)}")
print(f"CNN 参数量: {sum(p.numel() for p in cnn.parameters()):,}")

print()
print("=" * 60)
print("8. 保存与加载")
print("=" * 60)

model.eval()
with tempfile.TemporaryDirectory() as tmp_dir:      # 用临时目录, 不留垃圾文件
    path = os.path.join(tmp_dir, "model.pth")
    torch.save(model.state_dict(), path)            # 推荐: 只保存权重

    reloaded = Net()
    reloaded.load_state_dict(torch.load(path))
    reloaded.eval()

    probe = torch.from_numpy(X_test[:5])
    with torch.no_grad():
        same = torch.allclose(model(probe), reloaded(probe))
    print(f"保存到: {path}")
    print(f"重新加载后输出与原模型一致: {same}")

print()
print("=" * 60)
print("9. 扩展阅读")
print("=" * 60)

print("""
  - torchvision.datasets.MNIST / ImageFolder: 真实图片数据管道
  - torchvision.models: 预训练模型 (resnet18 等), 做迁移学习
  - torch.optim.lr_scheduler: 学习率调度 (CosineAnnealing 等)
  - PyTorch Lightning: 进一步封装训练循环, 需 pip install pytorch-lightning
""")