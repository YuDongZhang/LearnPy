"""
CNN 图像分类实战
==============

使用卷积神经网络 (CNN) 进行图像分类。
由于环境中未安装 PyTorch/TensorFlow，以下为示例代码展示。
"""

print("=" * 60)
print("1. CNN 简介")
print("=" * 60)

print("""
卷积神经网络 (Convolutional Neural Network, CNN):

CNN 的核心思想:
  • 局部连接: 每个神经元只连接局部区域
  • 权值共享: 同一层的神经元共享权重
  • 池化: 降低空间尺寸, 减少参数

CNN 主要组成:
  1. 卷积层 (Convolution) - 提取特征
  2. 池化层 (Pooling) - 降维
  3. 全连接层 (Fully Connected) - 分类

为什么 CNN 适合图像?
  • 保留空间结构
  • 参数少, 训练快
  • 层次化特征提取
""")

print()
print("=" * 60)
print("2. CNN 结构详解")
print("=" * 60)

print("""
2.1 卷积层

卷积操作:
  Input (5x5)  *  Kernel (3x3)  =  Output (3x3)

  [1 1 1 0 0]     [1 0 1]       [4 3 4]
  [0 1 1 1 0]  *  [0 1 0]   =   [2 4 3]
  [0 0 1 1 1]     [1 0 1]       [1 2 3]
  [0 0 1 1 0]
  [0 1 0 1 0]

参数:
  • 卷积核大小: 3x3, 5x5, 7x7
  • 步长 (Stride): 每次移动的距离
  • 填充 (Padding): 边缘补零

2.2 池化层

  • Max Pooling: 取最大值
  • Average Pooling: 取平均值
  • Global Pooling: 全局池化

2.3 全连接层

  • 将特征图展开为一维
  • 进行分类
""")

print()
print("=" * 60)
print("3. 经典 CNN 架构")
print("=" * 60)

print("""
3.1 LeNet-5 (1998)
  • 第一个 CNN
  • 用于手写数字识别
  • 结构: Conv -> Pool -> Conv -> Pool -> FC -> FC

3.2 AlexNet (2012)
  • ImageNet 竞赛突破
  • 8 层网络
  • ReLU 激活函数
  • Dropout 正则化

3.3 VGGNet (2014)
  • 统一的 3x3 卷积
  • VGG16 (16层), VGG19 (19层)
  • 简单有效

3.4 ResNet (2015)
  • 残差连接解决深层网络问题
  • 152 层网络
  • Skip Connection: y = F(x) + x

3.5 EfficientNet (2019)
  • 平衡深度、宽度、分辨率
  • 高效准确
""")

print()
print("=" * 60)
print("4. 项目: 猫狗分类")
print("=" * 60)

print("""
项目概述:
  • 任务: 二分类 (猫 vs 狗)
  • 数据集: Dogs vs Cats (Kaggle)
  • 模型: 自定义 CNN 或迁移学习

步骤:
  1. 数据准备
  2. 数据增强
  3. 构建模型
  4. 训练模型
  5. 评估模型
  6. 预测新图
""")

print()
print("=" * 60)
print("5. 数据准备")
print("=" * 60)

print('''
# 目录结构:
# data/
#   train/
#     cat.0.jpg
#     dog.0.jpg
#   validation/
#     cat.1.jpg
#     dog.1.jpg

# PyTorch 数据加载
from torchvision import datasets, transforms

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),  # 数据增强
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

train_data = datasets.ImageFolder('data/train', transform=train_transform)
val_data = datasets.ImageFolder('data/validation', transform=val_transform)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32)
''')

print()
print("=" * 60)
print("6. 构建 CNN 模型")
print("=" * 60)

print('''
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self, num_classes=2):
        super(CNN, self).__init__()

        # 卷积层
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        # 池化层
        self.pool = nn.MaxPool2d(2, 2)

        # BatchNorm
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(256)

        # 全连接层
        self.fc1 = nn.Linear(256 * 14 * 14, 512)
        self.fc2 = nn.Linear(512, num_classes)

        # Dropout
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Conv Block 1: 224 -> 112
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        # Conv Block 2: 112 -> 56
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        # Conv Block 3: 56 -> 28
        x = self.pool(torch.relu(self.bn3(self.conv3(x))))
        # Conv Block 4: 28 -> 14
        x = self.pool(torch.relu(self.bn4(self.conv4(x))))

        # 展平
        x = x.view(-1, 256 * 14 * 14)

        # 全连接
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

model = CNN(num_classes=2)
''')

print()
print("=" * 60)
print("7. 训练模型")
print("=" * 60)

print('''
import torch.optim as optim

# 损失函数
criterion = nn.CrossEntropyLoss()

# 优化器
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 学习率调度
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=2
)

# 训练函数
def train_epoch(model, loader, criterion, optimizer):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in loader:
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

# 验证函数
def validate(model, loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return running_loss / len(loader), 100. * correct / total

# 训练循环
num_epochs = 20
best_val_acc = 0.0

for epoch in range(num_epochs):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)
    val_loss, val_acc = validate(model, val_loader, criterion)

    scheduler.step(val_loss)

    print(f'Epoch {epoch+1}/{num_epochs}')
    print(f'  Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%')
    print(f'  Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%')

    # 保存最佳模型
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), 'best_model.pth')
''')

print()
print("=" * 60)
print("8. 迁移学习")
print("=" * 60)

print('''
import torchvision.models as models

# 使用预训练模型
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

# 或者使用 ResNet
model = models.resnet50(pretrained=True)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)

# 训练技巧:
# 1. 先冻结训练几轮
# 2. 然后解冻微调
# 3. 使用小的学习率
optimizer = optim.Adam(model.parameters(), lr=1e-4)
''')

print()
print("=" * 60)
print("9. 模型评估")
print("=" * 60)

print('''
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# 加载最佳模型
model.load_state_dict(torch.load('best_model.pth'))
model.eval()

# 预测
all_preds = []
all_labels = []

with torch.no_grad():
    for inputs, labels in val_loader:
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        all_preds.extend(predicted.numpy())
        all_labels.extend(labels.numpy())

# 混淆矩阵
cm = confusion_matrix(all_labels, all_preds)
print('混淆矩阵:')
print(cm)

# 分类报告
print('\\n分类报告:')
print(classification_report(all_labels, all_preds, target_names=['Cat', 'Dog']))
''')

print()
print("=" * 60)
print("10. 预测新图像")
print("=" * 60)

print('''
from PIL import Image

# 加载并预处理图像
def predict_image(image_path, model):
    model.eval()

    img = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.softmax(output, dim=1)
        pred = output.argmax(1)

    classes = ['Cat', 'Dog']
    return classes[pred.item()], prob[0][pred.item()].item()

# 预测
image_path = 'test.jpg'
class_name, confidence = predict_image(image_path, model)
print(f'预测: {class_name}, 置信度: {confidence:.2%}')
''')

print()
print("=" * 60)
print("11. 部署为 Web 服务")
print("=" * 60)

print('''
# 使用 Flask 部署
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # 获取图像
    image_file = request.files['image']
    image_bytes = image_file.read()

    # 预处理
    img = Image.open(io.BytesIO(image_bytes))
    img_tensor = transform(img).unsqueeze(0).to(device)

    # 预测
    with torch.no_grad():
        output = model(img_tensor)
        pred = output.argmax(1).item()

    return jsonify({'class': classes[pred], 'confidence': float(prob[0][pred])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# 或者使用 TorchScript 优化
model.eval()
scripted_model = torch.jit.trace(model, example_input)
scripted_model.save('model_scripted.pt')
''')

print()
print("=" * 60)
print("12. 项目总结")
print("=" * 60)

print("""
完整的 CNN 图像分类项目:

  ✓ 1. 数据收集 - 下载数据集
  ✓ 2. 数据划分 - 训练/验证/测试
  ✓ 3. 数据增强 - 增加样本多样性
  ✓ 4. 构建模型 - 自定义 CNN 或迁移学习
  ✓ 5. 训练模型 - GPU 训练, 早停
  ✓ 6. 评估模型 - 混淆矩阵, 分类报告
  ✓ 7. 预测新数据 - 部署上线

下一步可以尝试:
  • 目标检测 (YOLO, Faster R-CNN)
  • 语义分割 (U-Net, DeepLab)
  • 图像生成 (GAN, Diffusion)
  • 模型量化部署到移动端
""")
