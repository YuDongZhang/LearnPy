# 5. CNN图像分类实战

## CNN简介

卷积神经网络 (Convolutional Neural Network, CNN) 的核心思想：

- **局部连接**：每个神经元只连接局部区域
- **权值共享**：同一层的神经元共享权重
- **池化**：降低空间尺寸，减少参数

CNN 主要组成：

| 层 | 作用 |
|----|------|
| 卷积层 (Convolution) | 提取特征 |
| 池化层 (Pooling) | 降维 |
| 全连接层 (Fully Connected) | 分类 |

为什么 CNN 适合图像？保留空间结构、参数少训练快、层次化特征提取（浅层学边缘纹理，深层学语义部件）。

## 卷积层

卷积操作：输入 (5x5) × 卷积核 (3x3) → 输出 (3x3)：

```
[1 1 1 0 0]     [1 0 1]       [4 3 4]
[0 1 1 1 0]  *  [0 1 0]   =   [2 4 3]
[0 0 1 1 1]     [1 0 1]       [1 2 3]
[0 0 1 1 0]
[0 1 0 1 0]
```

关键参数：

- 卷积核大小：3x3、5x5、7x7
- 步长 (Stride)：每次移动的距离
- 填充 (Padding)：边缘补零，控制输出尺寸

## 池化层

- Max Pooling：取最大值（最常用）
- Average Pooling：取平均值
- Global Pooling：全局池化

## 经典CNN架构

| 架构 | 年份 | 贡献 |
|------|------|------|
| LeNet-5 | 1998 | 第一个 CNN，手写数字识别 |
| AlexNet | 2012 | ImageNet 突破，引入 ReLU 和 Dropout |
| VGGNet | 2014 | 统一的 3x3 卷积，VGG16/19 |
| ResNet | 2015 | 残差连接 y = F(x) + x，训到 152 层 |
| EfficientNet | 2019 | 平衡深度、宽度、分辨率 |

## 项目：猫狗分类

任务：二分类（猫 vs 狗），数据集 Dogs vs Cats (Kaggle)。

步骤：数据准备 → 数据增强 → 构建模型 → 训练 → 评估 → 预测。

## 数据准备

```python
from torchvision import datasets, transforms

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),   # 数据增强
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

train_data = datasets.ImageFolder('data/train', transform=train_transform)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
```

注意：训练集做数据增强，验证集只做 Resize + Normalize。

## 构建CNN模型

```python
class CNN(nn.Module):
    def __init__(self, num_classes=2):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.bn1 = nn.BatchNorm2d(32)   # BatchNorm 稳定训练
        self.fc1 = nn.Linear(256 * 14 * 14, 512)
        self.fc2 = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # 4个卷积块: 224 -> 112 -> 56 -> 28 -> 14
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        ...
        x = x.view(-1, 256 * 14 * 14)   # 展平
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x
```

## 训练模型

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=2
)

def train_epoch(model, loader, criterion, optimizer):
    model.train()          # 训练模式
    for inputs, labels in loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

def validate(model, loader, criterion):
    model.eval()           # 评估模式
    with torch.no_grad(): # 不计算梯度
        for inputs, labels in loader:
            outputs = model(inputs)
            ...

# 训练循环 + 保存最佳模型
for epoch in range(num_epochs):
    train_loss, train_acc = train_epoch(...)
    val_loss, val_acc = validate(...)
    scheduler.step(val_loss)

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), 'best_model.pth')
```

要点：`model.train()` / `model.eval()` 切换模式，验证时 `torch.no_grad()`。

## 迁移学习

数据不多时，用预训练模型效果远好于从头训练：

```python
model = models.efficientnet_b0(pretrained=True)

# 冻结前面层
for param in model.features[:-1].parameters():
    param.requires_grad = False

# 修改分类头
num_features = model.classifier[1].in_features
model.classifier = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 2)
)
```

训练技巧：先冻结训练几轮 → 解冻微调 → 用小学习率 (如 1e-4)。

## 模型评估

```python
from sklearn.metrics import confusion_matrix, classification_report

model.load_state_dict(torch.load('best_model.pth'))
model.eval()

with torch.no_grad():
    for inputs, labels in val_loader:
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        ...

cm = confusion_matrix(all_labels, all_preds)   # 混淆矩阵
print(classification_report(all_labels, all_preds,
                            target_names=['Cat', 'Dog']))
```

## 预测新图像

```python
from PIL import Image

def predict_image(image_path, model):
    model.eval()
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)   # 加 batch 维度

    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.softmax(output, dim=1)
        pred = output.argmax(1)

    classes = ['Cat', 'Dog']
    return classes[pred.item()], prob[0][pred.item()].item()

class_name, confidence = predict_image('test.jpg', model)
print(f'预测: {class_name}, 置信度: {confidence:.2%}')
```

## 部署为Web服务

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    image_file = request.files['image']
    # 预处理 → 预测 → 返回 JSON
    return jsonify({'class': classes[pred], 'confidence': float(prob)})

# 或使用 TorchScript 优化
scripted_model = torch.jit.trace(model, example_input)
scripted_model.save('model_scripted.pt')
```

## 项目总结

完整流程：数据收集 → 数据划分 → 数据增强 → 构建模型 → 训练（GPU、早停）→ 评估（混淆矩阵、分类报告）→ 预测部署。

下一步可以尝试：目标检测 (YOLO、Faster R-CNN)、语义分割 (U-Net、DeepLab)、图像生成 (GAN、Diffusion)、模型量化部署到移动端。

## 代码

讲解对应的示例代码见 `5_cnn_image_classification.py`。
