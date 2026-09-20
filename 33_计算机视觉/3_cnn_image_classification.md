# 3. CNN图像分类

## 为什么需要CNN

- 全连接网络参数量大，难以捕捉图像的空间结构
- CNN 通过卷积操作共享参数，大幅减少参数量

CNN 的核心思想：
- **局部连接**：每个神经元只连接局部区域
- **权值共享**：同一层的神经元使用相同的卷积核
- **池化**：降低分辨率，减少计算量

主要组成：卷积层、池化层、全连接层。

## 卷积操作

输入图像与卷积核（滤波器）做滑动点积：

```
[I * K](i,j) = Σ Σ I(i+m, j+n) · K(m,n)
```

例如 Sobel 边缘检测核：

```
[[-1, 0, 1],
 [-2, 0, 2],
 [-1, 0, 1]]
```

关键参数：
- **stride（步长）**：卷积核每次移动的距离
- **padding（填充）**：边缘补零，控制输出尺寸
- **感受野**：卷积核看到的区域大小

## 池化层

| 类型 | 做法 | 特点 |
|------|------|------|
| 最大池化 | 取区域内最大值 | 保留最显著的特征 |
| 平均池化 | 取区域内平均值 | 保留背景信息 |

作用：降低特征图尺寸、减少参数和计算量、防止过拟合、提供平移不变性。

## 经典CNN架构

| 模型 | 年份 | 贡献 |
|------|------|------|
| LeNet-5 | 1998 | 第一个成功的 CNN，手写数字识别 |
| AlexNet | 2012 | ImageNet 冠军，首次使用 ReLU 和 Dropout |
| VGGNet | 2014 | 统一的 3×3 卷积，16-19 层 |
| GoogLeNet | 2014 | Inception 模块，并行多尺度卷积 |
| ResNet | 2015 | 残差连接，可训练 152 层超深网络 |
| EfficientNet | 2019 | 平衡深度、宽度、分辨率 |

## PyTorch实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # Conv -> ReLU -> Pool
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 4 * 4)            # Flatten
        x = self.dropout(F.relu(self.fc1(x)))
        return self.fc2(x)
```

## 训练流程

```python
# 数据: CIFAR-10
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 每轮: 前向 -> 计算损失 -> 反向 -> 更新参数
# 评估时: model.eval() + torch.no_grad()
```

典型超参数：batch_size=64，lr=0.001，配合学习率调度（如 StepLR）。

## 使用预训练模型

```python
import torchvision.models as models
import torch.nn as nn

resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# 特征提取: 冻结 backbone，只训练分类头
for param in resnet.parameters():
    param.requires_grad = False
resnet.fc = nn.Linear(resnet.fc.in_features, num_classes)

# 微调: 解冻部分层
for param in resnet.layer4.parameters():
    param.requires_grad = True
```

常用预训练模型：ResNet、VGG、EfficientNet、MobileNet（移动端）。

## 迁移学习技巧

何时使用：数据量少、计算资源有限、任务与预训练任务相似。

| 策略 | 做法 | 适用 |
|------|------|------|
| 特征提取 | 冻结 backbone，只训练分类头 | 数据很少 |
| 微调 | 解冻部分层，较低学习率 (1e-4) | 数据适中 |
| 从头训练 | 解冻所有层，较高学习率 | 数据充足 |

## 训练技巧

- 数据增强：RandomResizedCrop、RandomHorizontalFlip、ColorJitter（训练时），测试只做 Resize + CenterCrop
- 学习率调度：`optim.lr_scheduler.StepLR`
- Dropout 防止过拟合
- 可视化：损失曲线、预测结果、卷积核

## 代码

讲解对应的示例代码见 `3_cnn_image_classification.py`。
