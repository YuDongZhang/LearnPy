# 6. CV实战：图像分类项目

## 项目概述

**任务**：将图像分为不同类别（如 CIFAR-10 的 10 类、猫狗分类）。

应用：医疗影像诊断、自动驾驶感知、商品识别、人脸识别。

## 方法对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| 传统方法（HOG + SVM） | 快速 | 效果一般 |
| CNN 从头训练 | 效果好 | 需要大量数据 |
| 迁移学习（ImageNet 预训练） | 少量数据也有好效果 | 需要选择合适的模型 |

## 方法一：简单CNN

```python
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
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 4 * 4)
        return self.fc2(self.dropout(F.relu(self.fc1(x))))
```

## 方法二：迁移学习（ResNet微调）

```python
model = models.resnet18(weights="IMAGENET1K_V1")

# 冻结 backbone，替换分类头
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 解冻后几层微调，不同层用不同学习率
for param in model.layer4.parameters():
    param.requires_grad = True

optimizer = torch.optim.Adam([
    {"params": model.fc.parameters(), "lr": 0.01},
    {"params": model.layer4.parameters(), "lr": 0.001}
])
```

数据增强（训练时随机，测试时固定）：

```python
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

## 方法三：PyTorch Lightning

把训练逻辑封装成模块，代码更简洁：

```python
class ImageClassifier(pl.LightningModule):
    def __init__(self, num_classes=10, lr=1e-3):
        super().__init__()
        self.model = models.resnet18(weights="IMAGENET1K_V1")
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def training_step(self, batch, batch_idx):
        inputs, labels = batch
        loss = self.criterion(self.model(inputs), labels)
        self.log("train_loss", loss)
        return loss

trainer = pl.Trainer(max_epochs=10, accelerator="auto")
trainer.fit(model, train_loader)
```

## 方法四：Timm模型库

```python
import timm

timm.list_models("efficientnet*")          # 列出可用模型
model = timm.create_model("efficientnet_b0",
                          pretrained=True, num_classes=10)

# 提取特征 (num_classes=0)
model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=0)
# 输出 [1, 1280] 特征向量
```

## 完整训练脚本要点

1. 配置超参数（batch_size=64, epochs=10, lr=0.001）
2. 数据增强 + DataLoader
3. 训练循环：前向 → 损失 → 反向 → 更新，配合 StepLR 调度
4. 每轮评估，保存最优模型：`torch.save(model.state_dict(), "best_model.pth")`
5. 输出分类报告：`classification_report(labels, preds)`

## 模型部署

```python
# 保存/加载权重（推荐）
torch.save(model.state_dict(), "model_weights.pth")
model.load_state_dict(torch.load("model_weights.pth"))

# 导出 ONNX
torch.onnx.export(model, dummy_input, "model.onnx",
                  dynamic_axes={"input": {0: "batch_size"}})

# TorchScript
scripted_model = torch.jit.trace(model, dummy_input)
```

Flask API 部署：

```python
@app.route("/predict", methods=["POST"])
def predict():
    image = Image.open(request.files["file"].stream).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image_tensor)
    return jsonify({"class": CLASSES[predicted.item()]})
```

## 模型性能对比

CIFAR-10 上的大致水平：

| 模型 | 参数量 | Top-1 Acc | 推理时间 |
|------|--------|-----------|----------|
| Simple CNN | ~1M | ~70% | 快 |
| ResNet-18 | ~11M | ~85% | 中 |
| ResNet-50 | ~25M | ~88% | 慢 |
| EfficientNet-B0 | ~5M | ~87% | 中 |
| MobileNetV2 | ~3M | ~82% | 快 |

选择建议：快速原型 Simple CNN；平衡效果 ResNet-18 / EfficientNet-B0；移动端 MobileNetV2；最高精度 ResNet-50 / EfficientNet-B3。

## 项目总结

1. 数据准备：数据增强、预处理
2. 模型选择：根据场景选择合适的模型
3. 训练：迁移学习、微调
4. 评估：准确率、分类报告
5. 部署：ONNX、Flask API

下一步：目标检测 (YOLO)、语义分割 (U-Net)、人脸识别、模型量化压缩。

## 代码

讲解对应的示例代码见 `6_cv_project.py`。
