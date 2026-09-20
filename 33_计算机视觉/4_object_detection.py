"""
目标检测算法
==========

介绍目标检测的基本概念和主流算法。
由于环境中未安装相关库，以下为示例代码展示。
"""

print("=" * 60)
print("1. 目标检测简介")
print("=" * 60)

print("""
目标检测 (Object Detection):

任务: 在图像中定位并分类所有物体

输出:
  • 边界框 (Bounding Box): x, y, w, h
  • 类别标签: 类别 + 置信度

与图像分类的区别:
  • 图像分类: 一张图 → 一个标签
  • 目标检测: 一张图 → 多个物体 + 位置 + 类别

应用场景:
  • 自动驾驶
  • 人脸检测
  • 视频监控
  • 医学影像
  • 商品检测
""")

print()
print("=" * 60)
print("2. 目标检测发展历程")
print("=" * 60)

print("""
| 年份 | 算法 | 特点 |
|------|------|------|
| 2013 | R-CNN | CNN + 选择性搜索 |
| 2014 | Fast R-CNN | ROI Pooling |
| 2015 | Faster R-CNN | RPN 网络 |
| 2016 | SSD | 单阶段检测 |
| 2016 | YOLO v1 | 实时检测 |
| 2017 | RetinaNet | Focal Loss |
| 2018 | YOLO v3 | 多尺度检测 |
| 2020 | YOLO v5 | 工程化成熟 |
| 2022 | YOLO v8 | 最新版本 |

两阶段 vs 单阶段:
  • 两阶段 (Two-stage):
    - 先找候选区域 → 再分类
    - 精度高, 速度慢
    - 代表: R-CNN 系列

  • 单阶段 (One-stage):
    - 直接在特征图上预测
    - 精度稍低, 速度快
    - 代表: YOLO, SSD
""")

print()
print("=" * 60)
print("3. 评价指标")
print("=" * 60)

print("""
3.1 IoU (Intersection over Union)

  预测框与真实框的重叠程度

  IoU = (预测框 ∩ 真实框) / (预测框 ∪ 真实框)

  IoU >= 0.5 → 视为检测正确

3.2 AP (Average Precision)

  Precision-Recall 曲线下的面积
  衡量单个类别的检测精度

3.3 mAP (mean Average Precision)

  所有类别 AP 的平均值
  目标检测最重要的指标

3.4 FPS (Frames Per Second)

  检测速度
  实时检测需要 >= 30 FPS
""")

print()
print("=" * 60)
print("4. YOLO 原理")
print("=" * 60)

print("""
YOLO (You Only Look Once):

核心思想:
  • 将图像划分为 S×S 网格
  • 每个网格预测 B 个边界框
  • 每个边界框包含: x, y, w, h, confidence
  • 每个网格预测 C 个类别概率

YOLO v1 结构:
  • 输入: 448×448×3
  • 骨干网络: GoogLeNet
  • 输出: 7×7×30

YOLO v3:
  • 骨干: Darknet-53
  • 多尺度检测 (3个尺度)
  • 使用 FPN
  • 13×13, 26×26, 52×52

YOLO v5/v8:
  • 骨干: CSPDarknet
  • PAN 特征融合
  • 工程化成熟
  • 易于部署
""")

print()
print("=" * 60)
print("5. YOLO 使用")
print("=" * 60)

print('''
# 使用 YOLOv5

# 安装
pip install ultralytics

from ultralytics import YOLO

# 加载模型
model = YOLO("yolov8n.pt")  # nano
# model = YOLO("yolov8s.pt")  # small
# model = YOLO("yolov8m.pt")  # medium
# model = YOLO("yolov8l.pt")  # large
# model = YOLO("yolov8x.pt")  # xlarge

# 预测
results = model("image.jpg")

# 显示结果
for r in results:
    print(r.boxes)  # 边界框信息
    r.show()       # 显示图像
    r.save("result.jpg")  # 保存结果

# 批量预测
results = model(["image1.jpg", "image2.jpg"])

# 视频预测
results = model("video.mp4", save=True)

# 使用摄像头
results = model(0, save=True)  # 0 表示摄像头


# 训练自己的模型

from ultralytics import YOLO

# 加载预训练模型
model = YOLO("yolov8n.pt")

# 训练
results = model.train(
    data="coco8.yaml",    # 数据集配置
    epochs=100,           # 训练轮数
    imgsz=640,            # 图像大小
    batch=16,             # batch size
    project="runs",       # 保存路径
    name="train"          # 实验名称
)

# 验证
results = model.val()

# 导出模型
model.export(format="onnx")  # 导出为 ONNX
model.export(format="tflite")  # 导出为 TFLite
''')

print()
print("=" * 60)
print("6. Faster R-CNN 原理")
print("=" * 60)

print("""
Faster R-CNN 架构:

1. 骨干网络 (Backbone)
   • 提取图像特征
   • 常用: ResNet, VGG

2. 区域建议网络 (RPN)
   • 生成候选区域 (Proposals)
   • 分类: 前景/背景
   • 回归: 调整边界框

3. ROI Pooling
   • 将不同大小的提案
   • 映射为固定大小特征

4. 分类器
   • 类别分类
   • 边界框回归

训练:
  • 交替训练 RPN 和 Fast R-CNN
  • 端到端训练
""")

print()
print("=" * 60)
print("7. 使用 Faster R-CNN")
print("=" * 60)

print('''
import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image

# 加载预训练模型
model = fasterrcnn_resnet50_fpn(weights="DEFAULT")
model.eval()

# 加载图像
image = Image.open("image.jpg")
image_tensor = F.to_tensor(image).unsqueeze(0)

# 预测
with torch.no_grad():
    predictions = model(image_tensor)

# 解析结果
boxes = predictions[0]["boxes"].numpy()
labels = predictions[0]["labels"].numpy()
scores = predictions[0]["scores"].numpy()

# 过滤低置信度
threshold = 0.5
mask = scores > threshold
boxes = boxes[mask]
labels = labels[mask]
scores = scores[mask]

# COCO 数据集类别
COCO_CLASSES = [
    "__background__", "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "N/A", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "N/A",
    "backpack", "umbrella", "N/A", "N/A", "handbag", "tie", "suitcase",
    "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "N/A", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
    "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "couch", "potted plant", "bed", "N/A",
    "dining table", "N/A", "N/A", "toilet", "N/A", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster",
    "sink", "refrigerator", "N/A", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush"
]

# 显示结果
for box, label, score in zip(boxes, labels, scores):
    class_name = COCO_CLASSES[label]
    print(f"{class_name}: {score:.2f}")
''')

print()
print("=" * 60)
print("8. SSD 原理")
print("=" * 60)

print("""
SSD (Single Shot MultiBox Detector):

核心思想:
  • 单阶段检测
  • 多尺度特征图
  • 默认框 (Default Boxes / Anchors)

架构:
  • 骨干网络: VGG / ResNet
  • 特征层: 多尺度 (38×38, 19×19, ...)
  • 分类器: 每个位置预测类别

优势:
  • 速度快 (比 YOLO 稍慢)
  • 精度高
  • 多尺度检测

相比 YOLO:
  • YOLO: 最后一层预测
  • SSD: 多层预测, 小物体更好
""")

print()
print("=" * 60)
print("9. 目标检测实战")
print("=" * 60)

print('''
# 完整的目标检测流程

import torch
from torchvision import transforms
from torchvision.models.detection import retinanet_resnet50_fpn
from PIL import Image
import cv2
import numpy as np

# 1. 加载模型
model = retinanet_resnet50_fpn(weights="DEFAULT")
model.eval()

# 2. 图像预处理
transform = transforms.Compose([
    transforms.ToTensor()
])

# 3. 加载和预处理图像
image = Image.open("image.jpg")
image_tensor = transform(image).unsqueeze(0)

# 4. 预测
with torch.no_grad():
    predictions = model(image_tensor)

# 5. 解析结果
def plot_boxes(image, boxes, labels, scores, threshold=0.5):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for box, label, score in zip(boxes, labels, scores):
        if score < threshold:
            continue

        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        text = f"{label}: {score:.2f}"
        cv2.putText(img, text, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img

# 绘制结果
boxes = predictions[0]["boxes"].numpy()
labels = predictions[0]["labels"].numpy()
scores = predictions[0]["scores"].numpy()

result_img = plot_boxes(image, boxes, labels, scores)
cv2.imwrite("result.jpg", result_img)
''')

print()
print("=" * 60)
print("10. 自定义目标检测训练")
print("=" * 60)

print('''
# 使用 PyTorch 训练目标检测模型

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_fpn
from torchvision.models.detection import faster_rcnn
from PIL import Image
import xml.etree.ElementTree as ET
import os

# 自定义数据集
class ObjectDetectionDataset(Dataset):
    def __init__(self, img_dir, ann_dir, transforms=None):
        self.img_dir = img_dir
        self.ann_dir = ann_dir
        self.transforms = transforms
        self.imgs = list(sorted(os.listdir(img_dir)))

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.imgs[idx])
        ann_path = os.path.join(self.ann_dir, self.imgs[idx].replace(".jpg", ".xml"))

        # 读取图像
        img = Image.open(img_path).convert("RGB")

        # 解析 XML 标注
        tree = ET.parse(ann_path)
        root = tree.getroot()

        boxes = []
        labels = []

        for obj in root.findall("object"):
            name = obj.find("name").text
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(1)  # 假设只有一类

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels

        if self.transforms:
            img = self.transforms(img)

        return img, target


# 数据增强
def get_transform():
    return transforms.Compose([
        transforms.ToTensor(),
    ])


# 创建数据加载器
train_dataset = ObjectDetectionDataset("train/images", "train/annotations", get_transform())
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))


# 加载模型
model = fasterrcnn_mobilenet_v3_large_fpn(weights="DEFAULT")

# 修改类别数
num_classes = 2  # 背景 + 1 类
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = nn.Linear(in_features, num_classes)


# 训练
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.001, momentum=0.9, weight_decay=0.0005)

for epoch in range(10):
    model.train()
    for images, targets in train_loader:
        images = [img for img in images]
        targets = [{k: v for k, v in t.items()} for t in targets]

        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}: Loss={losses.item():.4f}")
''')

print()
print("=" * 60)
print("11. 目标检测总结")
print("=" * 60)

print("""
目标检测要点:

✓ 主要算法:
  • YOLO: 速度快, 适合实时
  • Faster R-CNN: 精度高
  • SSD: 平衡

✓ YOLO 版本选择:
  • v5: 成熟稳定
  • v8: 最新最强
  • v8n: 最快, 精度较低

✓ 数据标注:
  • 常用工具: LabelImg, CVAT
  • 格式: COCO, YOLO, VOC

✓ 训练技巧:
  • 数据增强
  • 预训练权重
  • 多尺度训练
  • 难例挖掘

✓ 部署:
  • ONNX
  • TensorRT
  • TFLite
""")
