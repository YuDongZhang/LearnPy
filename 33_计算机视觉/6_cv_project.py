"""
CV 实战：图像分类项目
==================

使用多种方法实现图像分类项目。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("""
项目: 图像分类 (Image Classification)

任务: 将图像分为不同类别

数据集:
  • 英文: CIFAR-10, ImageNet
  • 猫狗分类: Dogs vs Cats

应用:
  • 医疗影像诊断
  • 自动驾驶感知
  • 商品识别
  • 人脸识别
""")

print()
print("=" * 60)
print("2. 方法对比")
print("=" * 60)

print("""
2.1 传统方法

  • 特征提取 + SVM
  • HOG + 分类器
  • 优点: 快速
  • 缺点: 效果一般

2.2 深度学习

  • CNN (LeNet, AlexNet)
  • 优点: 效果好
  • 缺点: 需要大量数据

2.3 迁移学习

  • 使用 ImageNet 预训练模型
  • 优点: 少量数据也能有好效果
  • 缺点: 需要选择合适的模型
""")

print()
print("=" * 60)
print("3. 方法一: 简单 CNN")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)

        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 32 -> 16
        x = self.pool(F.relu(self.conv2(x)))  # 16 -> 8
        x = self.pool(F.relu(self.conv3(x)))  # 8 -> 4

        x = x.view(-1, 128 * 4 * 4)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# 训练
model = SimpleCNN(num_classes=10)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练循环...
''')

print()
print("=" * 60)
print("4. 方法二: 使用预训练模型")
print("=" * 60)

print('''
import torch
import torchvision.models as models
import torch.nn as nn

# 加载预训练 ResNet
model = models.resnet18(weights="IMAGENET1K_V1")

# 冻结参数
for param in model.parameters():
    param.requires_grad = False

# 修改最后的全连接层
num_classes = 10
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 解冻后几层进行微调
for param in model.layer4.parameters():
    param.requires_grad = True

# 训练
optimizer = torch.optim.Adam(
    [
        {"params": model.fc.parameters(), "lr": 0.01},
        {"params": model.layer4.parameters(), "lr": 0.001}
    ]
)

# 完整训练流程
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 数据增强
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 数据集
train_data = datasets.CIFAR10(root="./data", train=True, transform=train_transform, download=True)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# 训练
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1} completed")
''')

print()
print("=" * 60)
print("5. 方法三: PyTorch Lightning")
print("=" * 60)

print('''
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torchvision.models as models

class ImageClassifier(pl.LightningModule):
    def __init__(self, num_classes=10, lr=1e-3):
        super().__init__()
        self.model = models.resnet18(weights="IMAGENET1K_V1")
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
        self.lr = lr
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        inputs, labels = batch
        outputs = self.forward(inputs)
        loss = self.criterion(outputs, labels)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.model.parameters(), lr=self.lr)

# 训练
trainer = pl.Trainer(max_epochs=10, accelerator="auto")
model = ImageClassifier(num_classes=10)
trainer.fit(model, train_loader)
''')

print()
print("=" * 60)
print("6. 方法四: Timm (更多模型)")
print("=" * 60)

print('''
import timm

# 列出可用模型
models = timm.list_models("efficientnet*")
print(models[:10])

# 加载模型
model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=10)

# 使用
output = model(torch.randn(1, 3, 224, 224))
print(output.shape)  # [1, 10]

# 获取特征
model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=0)
features = model(torch.randn(1, 3, 224, 224))
print(features.shape)  # [1, 1280]
''')

print()
print("=" * 60)
print("7. 完整项目代码")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import numpy as np
from sklearn.metrics import classification_report

# 配置
NUM_CLASSES = 10
BATCH_SIZE = 64
EPOCHS = 10
LR = 0.001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 数据增强
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 数据集
train_data = datasets.CIFAR10(root="./data", train=True, transform=train_transform, download=True)
test_data = datasets.CIFAR10(root="./data", train=False, transform=test_transform, download=True)

train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=4)

# 模型
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model = model.to(DEVICE)

# 损失和优化
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# 训练函数
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

# 评估函数
def evaluate(model, loader, device):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    accuracy = (np.array(all_preds) == np.array(all_labels)).mean()
    return accuracy, all_preds, all_labels

# 训练循环
best_acc = 0.0

for epoch in range(EPOCHS):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, DEVICE)
    test_acc, preds, labels = evaluate(model, test_loader, DEVICE)

    scheduler.step()

    print(f"Epoch {epoch+1}/{EPOCHS}: "
          f"Train Loss: {train_loss:.4f}, "
          f"Train Acc: {train_acc:.2f}%, "
          f"Test Acc: {test_acc*100:.2f}%")

    if test_acc > best_acc:
        best_acc = test_acc
        torch.save(model.state_dict(), "best_model.pth")

print(f"Best Test Accuracy: {best_acc*100:.2f}%")

# 分类报告
print("\\nClassification Report:")
print(classification_report(labels, preds))
''')

print()
print("=" * 60)
print("8. 模型部署")
print("=" * 60)

print('''
import torch

# 保存整个模型
torch.save(model, "model.pth")
loaded_model = torch.load("model.pth")

# 保存权重 (推荐)
torch.save(model.state_dict(), "model_weights.pth")
model.load_state_dict(torch.load("model_weights.pth"))

# 导出 ONNX
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)

# 导出 TorchScript
model.eval()
scripted_model = torch.jit.trace(model, dummy_input)
scripted_model.save("model.pt")
''')

print()
print("=" * 60)
print("9. Flask API 部署")
print("=" * 60)

print('''
from flask import Flask, request, jsonify
import torch
from torchvision import transforms
from PIL import Image
import io

app = Flask(__name__)

# 加载模型
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(model.fc.in_features, 10)
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# 图像预处理
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

CLASSES = ["airplane", "automobile", "bird", "cat", "deer",
           "dog", "frog", "horse", "ship", "truck"]

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    image = Image.open(file.stream).convert("RGB")

    # 预处理
    image_tensor = transform(image).unsqueeze(0)

    # 预测
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = outputs.max(1)
        prob = torch.softmax(outputs, dim=1)[0]

    result = {
        "class": CLASSES[predicted.item()],
        "confidence": prob[predicted.item()].item()
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
''')

print()
print("=" * 60)
print("10. 模型对比")
print("=" * 60)

print("""
模型性能对比 (CIFAR-10):

| 模型           | 参数量   | Top-1 Acc | 推理时间 |
|---------------|----------|------------|----------|
| Simple CNN    | ~1M      | ~70%       | 快       |
| ResNet-18     | ~11M     | ~85%       | 中       |
| ResNet-50     | ~25M     | ~88%       | 慢       |
| EfficientNet-B0 | ~5M    | ~87%       | 中       |
| MobileNetV2   | ~3M      | ~82%       | 快       |

选择建议:
  • 快速原型: Simple CNN
  • 平衡效果: ResNet-18, EfficientNet-B0
  • 移动端: MobileNetV2
  • 最高精度: ResNet-50, EfficientNet-B3
""")

print()
print("=" * 60)
print("11. 项目总结")
print("=" * 60)

print("""
图像分类项目要点:

✓ 1. 数据准备 - 数据增强、预处理
✓ 2. 模型选择 - 根据场景选择合适的模型
✓ 3. 训练 - 迁移学习、微调
✓ 4. 评估 - 准确率、分类报告
✓ 5. 部署 - ONNX、Flask API

下一步可以尝试:
  • 目标检测 (YOLO)
  • 语义分割 (U-Net)
  • 人脸识别
  • 模型量化压缩

推荐资源:
  • PyTorch 官方教程
  • Fast.ai 课程
  • Kaggle 竞赛
""")
