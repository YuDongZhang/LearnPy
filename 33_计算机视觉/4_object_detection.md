# 4. 目标检测

## 任务定义

目标检测：在图像中**定位并分类所有物体**。

- 图像分类：一张图 → 一个标签
- 目标检测：一张图 → 多个物体 + 位置（边界框 x, y, w, h）+ 类别 + 置信度

应用：自动驾驶、人脸检测、视频监控、医学影像、商品检测。

## 发展历程

| 年份 | 算法 | 特点 |
|------|------|------|
| 2013 | R-CNN | CNN + 选择性搜索 |
| 2015 | Faster R-CNN | RPN 网络 |
| 2016 | SSD | 单阶段检测 |
| 2016 | YOLO v1 | 实时检测 |
| 2017 | RetinaNet | Focal Loss |
| 2020 | YOLO v5 | 工程化成熟 |
| 2022 | YOLO v8 | 最新版本 |

**两阶段 vs 单阶段**：

| 类型 | 流程 | 精度/速度 | 代表 |
|------|------|----------|------|
| 两阶段 | 先找候选区域 → 再分类 | 精度高，速度慢 | R-CNN 系列 |
| 单阶段 | 直接在特征图上预测 | 精度稍低，速度快 | YOLO, SSD |

## 评价指标

```
IoU = (预测框 ∩ 真实框) / (预测框 ∪ 真实框)   # IoU >= 0.5 视为检测正确
AP  = PR 曲线下面积                            # 单类别精度
mAP = 所有类别 AP 的平均值                      # 最重要的指标
FPS = 每秒帧数                                 # 实时检测需要 >= 30
```

## YOLO原理

YOLO (You Only Look Once) 核心思想：
1. 将图像划分为 S×S 网格
2. 每个网格预测 B 个边界框 (x, y, w, h, confidence)
3. 每个网格预测 C 个类别概率

版本演进：
- **YOLO v3**：Darknet-53 骨干，FPN 多尺度检测（13×13, 26×26, 52×52）
- **YOLO v5/v8**：CSPDarknet 骨干，PAN 特征融合，工程化成熟、易于部署

## YOLO使用

```python
# pip install ultralytics
from ultralytics import YOLO

model = YOLO("yolov8n.pt")   # n/s/m/l/x 从小到大

results = model("image.jpg")
for r in results:
    print(r.boxes)
    r.save("result.jpg")

# 视频和摄像头
results = model("video.mp4", save=True)
results = model(0, save=True)
```

训练自己的模型：

```python
model = YOLO("yolov8n.pt")
model.train(data="coco8.yaml", epochs=100, imgsz=640, batch=16)
model.export(format="onnx")   # 导出 ONNX
```

## Faster R-CNN原理

四个组件：
1. **骨干网络**（Backbone）：提取特征（ResNet、VGG）
2. **RPN**（区域建议网络）：生成候选区域，分类前景/背景 + 回归边界框
3. **ROI Pooling**：把不同大小的提案映射为固定大小特征
4. **分类器**：类别分类 + 边界框回归

```python
from torchvision.models.detection import fasterrcnn_resnet50_fpn

model = fasterrcnn_resnet50_fpn(weights="DEFAULT")
model.eval()

with torch.no_grad():
    predictions = model(image_tensor)

boxes = predictions[0]["boxes"].numpy()
scores = predictions[0]["scores"].numpy()
mask = scores > 0.5            # 过滤低置信度
```

## SSD原理

SSD (Single Shot MultiBox Detector)：
- 单阶段检测，使用多尺度特征图（38×38, 19×19, ...）
- 每个位置设置默认框（Default Boxes / Anchors）

与 YOLO v1 的区别：YOLO 只在最后一层预测，SSD 多层预测，**小物体效果更好**。

## 自定义训练

数据标注：工具 LabelImg、CVAT；格式 COCO / YOLO / VOC。

```python
class ObjectDetectionDataset(Dataset):
    def __getitem__(self, idx):
        img = Image.open(img_path).convert("RGB")
        # 解析 XML 标注得到 boxes 和 labels
        target = {"boxes": boxes, "labels": labels}
        return img, target

# DataLoader 需要自定义 collate_fn
train_loader = DataLoader(train_dataset, batch_size=2,
                          collate_fn=lambda x: tuple(zip(*x)))

# 训练: loss_dict 包含多项损失, 求和后反向传播
loss_dict = model(images, targets)
losses = sum(loss for loss in loss_dict.values())
```

## 总结

| 算法 | 特点 | 适用 |
|------|------|------|
| YOLO | 速度快 | 实时检测 |
| Faster R-CNN | 精度高 | 离线分析 |
| SSD | 平衡 | 通用 |

训练技巧：数据增强、预训练权重、多尺度训练、难例挖掘。部署：ONNX、TensorRT、TFLite。

## 代码

讲解对应的示例代码见 `4_object_detection.py`。
