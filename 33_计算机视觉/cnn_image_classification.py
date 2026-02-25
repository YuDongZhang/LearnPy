"""
CNN 图像分类
==========

介绍卷积神经网络 (CNN) 的原理和图像分类实现。
"""

print("=" * 60)
print("1. CNN 简介")
print("=" * 60)

print("""
卷积神经网络 (Convolutional Neural Network, CNN):

为什么需要 CNN?
  • 全连接网络参数量大
  • 难以捕捉图像的空间结构
  • CNN 通过卷积操作共享参数

CNN 的核心思想:
  • 局部连接: 每个神经元只连接局部区域
  • 权值共享: 同一层的神经元使用相同的卷积核
  • 池化: 降低分辨率, 减少计算量

CNN 主要组成:
  1. 卷积层 (Convolutional Layer)
  2. 池化层 (Pooling Layer)
  3. 全连接层 (Fully Connected Layer)
""")

print()
print("=" * 60)
print("2. 卷积操作")
print("=" * 60)

print("""
卷积操作原理:

输入图像与卷积核 (滤波器) 的点积运算:

  [I * K](i,j) = Σ Σ I(i+m, j+n) · K(m,n)

卷积核 (3x3):
  [[-1, 0, 1],
   [-2, 0, 2],
   [-1, 0, 1]]  ← Sobel 边缘检测

参数:
  • stride (步长): 卷积核移动的步长
  • padding (填充): 边缘补零
  • 感受野: 卷积核看到的区域大小

特征图 (Feature Map):
  • 输入: H × W × C
  • 输出: H' × W' × C'
""")

print()
print("=" * 60)
print("3. 池化层")
print("=" * 60)

print("""
池化 (Pooling) 操作:

最大池化 (Max Pooling):
  取区域内的最大值
  保留最显著的特征

平均池化 (Average Pooling):
  取区域内的平均值
  保留背景信息

参数:
  • pool_size: 池化窗口大小
  • stride: 步长

作用:
  ✓ 降低特征图尺寸
  ✓ 减少参数和计算量
  ✓ 防止过拟合
  ✓ 提供平移不变性
""")

print()
print("=" * 60)
print("4. 经典 CNN 架构")
print("=" * 60)

print("""
4.1 LeNet-5 (1998)

  第一个成功的 CNN
  用于手写数字识别
  结构: Conv → Pool → Conv → Pool → FC → FC

4.2 AlexNet (2012)

  ImageNet 竞赛冠军
  首次使用 ReLU 激活函数
  使用 Dropout 正则化
  8 层网络

4.3 VGGNet (2014)

  统一的 3×3 卷积
  更深的网络 (16-19 层)
  参数量大, 但结构简单

4.4 GoogLeNet (2014)

  Inception 模块
  并行多尺度卷积
  减少参数, 提高效率

4.5 ResNet (2015)

  残差连接 (Skip Connection)
  可以训练超深网络 (152层)
  解决梯度消失问题

4.6 EfficientNet (2019)

  平衡深度、宽度、分辨率
  更高的效率和精度
""")

print()
print("=" * 60)
print("5. PyTorch CNN 实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.nn.functional as F

# 5.1 简单 CNN
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()

        # 卷积层
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        # 池化层
        self.pool = nn.MaxPool2d(2, 2)

        # 全连接层
        self.fc1 = nn.Linear(64 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)

        # Dropout
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Conv -> ReLU -> Pool
        x = self.pool(F.relu(self.conv1(x)))  # 224 -> 112
        x = self.pool(F.relu(self.conv2(x)))  # 112 -> 56
        x = self.pool(F.relu(self.conv3(x)))  # 56 -> 28

        # Flatten
        x = x.view(-1, 64 * 4 * 4)

        # FC
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)

        return x


# 5.2 使用 nn.Sequential
class CNN_v2(nn.Module):
    def __init__(self, num_classes=10):
        super(CNN_v2, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
''')

print()
print("=" * 60)
print("6. 训练 CNN")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

# 6.1 数据准备
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_dataset = torchvision.datasets.CIFAR10(
    root="./data", train=True, download=True, transform=transform
)
test_dataset = torchvision.datasets.CIFAR10(
    root="./data", train=False, download=True, transform=transform
)

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=64, shuffle=True
)
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=64, shuffle=False
)

# 6.2 模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN(num_classes=10).to(device)

# 6.3 损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 6.4 训练循环
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    return running_loss / len(loader), 100. * correct / total

# 6.5 评估
def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return 100. * correct / total

# 6.6 训练
for epoch in range(10):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    test_acc = evaluate(model, test_loader, device)
    print(f"Epoch {epoch+1}: Loss={train_loss:.4f}, Train Acc={train_acc:.2f}%, Test Acc={test_acc:.2f}%")
''')

print()
print("=" * 60)
print("7. 使用预训练模型")
print("=" * 60)

print('''
import torch
import torchvision.models as models
import torch.nn as nn

# 7.1 加载预训练模型
resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# 7.2 特征提取 (Frozen)
for param in resnet.parameters():
    param.requires_grad = False

# 修改最后的全连接层
num_classes = 10
resnet.fc = nn.Linear(resnet.fc.in_features, num_classes)

# 7.3 微调 (Fine-tuning)
# 解冻部分层
for param in resnet.layer4.parameters():
    param.requires_grad = True

# 7.4 使用模型
model = resnet
output = model(torch.randn(1, 3, 224, 224))
print(output.shape)  # [1, 10]


# 7.5 VGG16
vgg = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
vgg.classifier[-1] = nn.Linear(4096, num_classes)

# 7.6 MobileNet (轻量级)
mobilenet = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
mobilenet.classifier[-1] = nn.Linear(1280, num_classes)

# 7.7 EfficientNet
efficientnet = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
efficientnet.classifier[-1] = nn.Linear(1280, num_classes)
''')

print()
print("=" * 60)
print("8. 完整训练脚本")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision.datasets as datasets

# 超参数
BATCH_SIZE = 64
EPOCHS = 20
LR = 0.001
NUM_CLASSES = 10

# 数据增强
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# 数据集
train_data = datasets.CIFAR10(root="./data", train=True, transform=train_transform, download=True)
test_data = datasets.CIFAR10(root="./data", train=False, transform=test_transform, download=True)

train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=4)

# 模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model = model.to(device)

# 损失和优化
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# 训练
for epoch in range(EPOCHS):
    model.train()
    train_loss = 0
    train_correct = 0
    train_total = 0

    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        _, predicted = outputs.max(1)
        train_total += targets.size(0)
        train_correct += predicted.eq(targets).sum().item()

        if (batch_idx + 1) % 100 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}], Step [{batch_idx+1}/{len(train_loader)}]")

    scheduler.step()

    # 评估
    model.eval()
    test_correct = 0
    test_total = 0

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            test_total += targets.size(0)
            test_correct += predicted.eq(targets).sum().item()

    print(f"Epoch {epoch+1}: Train Acc={100.*train_correct/train_total:.2f}%, Test Acc={100.*test_correct/test_total:.2f}%")

# 保存模型
torch.save(model.state_dict(), "model.pth")
''')

print()
print("=" * 60)
print("9. 迁移学习技巧")
print("=" * 60)

print("""
9.1 何时使用迁移学习?

  ✓ 数据量少
  ✓ 计算资源有限
  ✓ 任务与预训练任务相似

9.2 迁移学习策略

  特征提取:
    • 冻结 backbone
    • 只训练分类头
    • 适用于数据很少

  微调:
    • 解冻部分层
    • 较低的学习率
    • 适用于数据适中

  从头训练:
    • 解冻所有层
    • 较高学习率
    • 适用于数据充足

9.3 学习率设置

  特征提取: lr = 0.001 ~ 0.01
  微调: lr = 0.0001 ~ 0.001
  分类层: 可以使用 10 倍学习率
""")

print()
print("=" * 60)
print("10. 可视化")
print("=" * 60)

print('''
import matplotlib.pyplot as plt

# 10.1 可视化损失曲线
plt.figure(figsize=(10, 5))
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Val Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.title("Training Progress")
plt.savefig("loss.png")

# 10.2 可视化预测结果
def visualize_predictions(images, labels, predictions, class_names):
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    for i, ax in enumerate(axes.flat):
        img = images[i]
        # 反归一化
        img = img * 0.5 + 0.5
        ax.imshow(img)

        true_label = class_names[labels[i]]
        pred_label = class_names[predictions[i]]
        color = "green" if labels[i] == predictions[i] else "red"
        ax.set_title(f"T: {true_label}\\nP: {pred_label}", color=color)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig("predictions.png")

# 10.3 可视化卷积核
def visualize_filters(model, layer_name):
    filters = model.state_dict()[layer_name]
    # 假设 filters shape: [64, 3, 3, 3]
    fig, axes = plt.subplots(8, 8, figsize=(12, 12))
    for i, ax in enumerate(axes.flat):
        filter = filters[i].cpu().numpy()
        filter = (filter - filter.min()) / (filter.max() - filter.min())
        ax.imshow(filter.transpose(1, 2, 0))
        ax.axis("off")
    plt.savefig("filters.png")
''')

print()
print("=" * 60)
print("11. CNN 总结")
print("=" * 60)

print("""
CNN 图像分类要点:

✓ 核心组件:
  • 卷积层: 提取特征
  • 池化层: 降维
  • 全连接层: 分类

✓ 经典架构:
  • LeNet → AlexNet → VGG → ResNet
  • 趋势: 越来越深、越来越高效

✓ 训练技巧:
  • 数据增强
  • 预训练 + 微调
  • 学习率调度
  • Dropout

✓ 常用模型:
  • ResNet (平衡效果好)
  • EfficientNet (效率高)
  • MobileNet (移动端)

✓ PyTorch 工具:
  • torchvision.models
  • torchvision.transforms
  • torch.optim
""")
