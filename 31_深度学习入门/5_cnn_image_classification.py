"""
CNN 图像分类实战
==============

使用卷积神经网络 (CNN) 做图像分类, 全部代码真实运行。

数据集: sklearn digits (8x8 手写数字, 离线可用)。
真实猫狗照片项目的写法 (ImageFolder + 迁移学习) 见第 8 节。
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

print("=" * 60)
print("1. 卷积操作的直观理解 (手算)")
print("=" * 60)

image = torch.tensor([
    [1., 1., 1., 0., 0.],
    [0., 1., 1., 1., 0.],
    [0., 0., 1., 1., 1.],
    [0., 0., 1., 1., 0.],
    [0., 1., 0., 1., 0.],
])
kernel = torch.tensor([
    [1., 0., 1.],
    [0., 1., 0.],
    [1., 0., 1.],
])

conv = nn.Conv2d(1, 1, kernel_size=3, bias=False)
with torch.no_grad():
    conv.weight.copy_(kernel.reshape(1, 1, 3, 3))
    out = conv(image.reshape(1, 1, 5, 5))

print(f"输入 5x5:\n{image.int().numpy()}")
print(f"卷积核 3x3:\n{kernel.int().numpy()}")
print(f"输出 3x3 (无填充, 5-3+1=3):\n{out.int().reshape(3, 3).numpy()}")
print("卷积 = 同一个核滑过整张图, 每次做加权求和 (权值共享)")
print("参数量只有 9 个 (3x3), 与图片大小无关 —— 这是 CNN 参数少的原因")

print()
print("=" * 60)
print("2. 池化: 降低空间尺寸")
print("=" * 60)

feature = torch.arange(1., 17.).reshape(1, 1, 4, 4)
max_pool = nn.MaxPool2d(2)
avg_pool = nn.AvgPool2d(2)
print(f"输入 4x4:\n{feature.int().reshape(4, 4).numpy()}")
print(f"MaxPool 2x2 (每块取最大):\n{max_pool(feature).int().reshape(2, 2).numpy()}")
print(f"AvgPool 2x2 (每块取平均):\n{avg_pool(feature).round().int().reshape(2, 2).numpy()}")
print("池化没有参数, 只做降维: 4x4 -> 2x2, 计算量和内存都减少")

print()
print("=" * 60)
print("3. 数据准备")
print("=" * 60)

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()
X = digits.images.astype("float32") / 16.0      # (1797, 8, 8), 像素归一化
y = digits.target.astype("int64")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_ds = TensorDataset(torch.from_numpy(X_train).unsqueeze(1), torch.from_numpy(y_train))
test_ds = TensorDataset(torch.from_numpy(X_test).unsqueeze(1), torch.from_numpy(y_test))
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=256)

print(f"训练集 {len(train_ds)} 条 / 测试集 {len(test_ds)} 条")
print(f"单张图片形状: {tuple(train_ds[0][0].shape)}  (通道=1, 8x8)")

print()
print("=" * 60)
print("4. 构建 CNN")
print("=" * 60)


class CNN(nn.Module):
    """Conv -> BN -> ReLU -> Pool 堆叠, 最后全连接分类"""

    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool = nn.MaxPool2d(2)
        self.dropout = nn.Dropout(0.25)
        self.fc1 = nn.Linear(64 * 2 * 2, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # 8x8 -> conv(padding=1) -> 8x8 -> pool -> 4x4
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        # 4x4 -> conv(padding=1) -> 4x4 -> pool -> 2x2
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = torch.flatten(x, 1)
        x = self.dropout(torch.relu(self.fc1(x)))
        return self.fc2(x)


model = CNN()
print(f"参数量: {sum(p.numel() for p in model.parameters()):,}")

print()
print("=" * 60)
print("5. 训练模型")
print("=" * 60)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)


def run_epoch(loader, train=True):
    if train:
        model.train()
    else:
        model.eval()

    total_loss = correct = total = 0
    with torch.set_grad_enabled(train):
        for inputs, labels in loader:
            if train:
                optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            if train:
                loss.backward()
                optimizer.step()

            total_loss += loss.item()
            correct += (outputs.argmax(1) == labels).sum().item()
            total += labels.size(0)
    return total_loss / len(loader), 100 * correct / total


for epoch in range(1, 11):
    train_loss, train_acc = run_epoch(train_loader, train=True)
    val_loss, val_acc = run_epoch(test_loader, train=False)
    scheduler.step(val_loss)              # 验证损失不降时自动降低学习率

    if epoch in (1, 3, 5, 10):
        print(f"  epoch {epoch:2d}: Train Loss {train_loss:.3f} Acc {train_acc:.2f}% | "
              f"Val Loss {val_loss:.3f} Acc {val_acc:.2f}%")

print()
print("=" * 60)
print("6. 模型评估 (混淆矩阵)")
print("=" * 60)

from sklearn.metrics import confusion_matrix

model.eval()
all_preds, all_labels = [], []
with torch.no_grad():
    for inputs, labels in test_loader:
        all_preds.extend(model(inputs).argmax(1).tolist())
        all_labels.extend(labels.tolist())

print("混淆矩阵 (行=真实, 列=预测):")
print(confusion_matrix(all_labels, all_preds))
print(f"\n准确率: {np.mean(np.array(all_preds) == np.array(all_labels)):.2%}")

print()
print("=" * 60)
print("7. 预测单张图片")
print("=" * 60)

idx = 0
img = torch.from_numpy(X_test[idx]).unsqueeze(0).unsqueeze(0)   # (1, 1, 8, 8)
with torch.no_grad():
    probs = torch.softmax(model(img), dim=1)[0]
pred = probs.argmax().item()
print(f"真实标签: {y_test[idx]}")
print(f"预测结果: {pred}, 置信度: {probs[pred].item():.2%}")

print()
print("=" * 60)
print("8. 真实图片项目写法 (猫狗分类)")
print("=" * 60)

print("""
处理真实照片 (如 Kaggle Dogs vs Cats) 时, 用 ImageFolder + 预训练模型:

    from torchvision import datasets, transforms, models

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),          # 数据增强
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    # 目录结构: data/train/cat/*.jpg, data/train/dog/*.jpg
    train_data = datasets.ImageFolder('data/train', transform=transform)
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

    # 迁移学习: 用 ImageNet 预训练权重, 只换掉分类头
    model = models.efficientnet_b0(weights='DEFAULT')
    for p in model.features.parameters():
        p.requires_grad = False                     # 冻结主干
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 2)

    # 微调时解冻部分层, 用小学习率 (如 1e-4)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

注意:
  - weights='DEFAULT' 是当前推荐写法 (旧版 pretrained=True 已弃用)
  - 首次运行需联网下载预训练权重
  - 部署可用 Flask/FastAPI 包一层, 加载模型做在线推理

小结: 本项目流程 = 数据准备 -> 数据增强 -> 构建模型 -> 训练(含学习率调度)
      -> 评估(混淆矩阵) -> 预测新图片 -> (可选)部署上线
""")