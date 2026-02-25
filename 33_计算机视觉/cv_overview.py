"""
计算机视觉概述
============

介绍计算机视觉的基本概念、发展历程和应用领域。
"""

print("=" * 60)
print("1. 计算机视觉简介")
print("=" * 60)

print("""
计算机视觉 (Computer Vision, CV):

让计算机具有人类视觉的能力，能够"看懂"图像和视频。

CV 的核心问题:
  • 图像分类: 这张图片是什么?
  • 目标检测: 图片里有哪些物体? 在哪里?
  • 语义分割: 每个像素属于哪个类别?
  • 人脸识别: 这是谁?
  • 姿态估计: 人的姿势是什么样的?
  • 图像生成: 生成逼真的图像

为什么重要?
  • 人类获取信息 80% 来自视觉
  • 应用广泛: 安防、医疗、自动驾驶
  • 大数据时代，图像/视频爆发式增长
""")

print()
print("=" * 60)
print("2. 发展历程")
print("=" * 60)

print("""
| 年份 | 里程碑 |
|------|--------|
| 1966 | MIT 夏季视觉项目起步 |
| 1970s | 边缘检测、特征提取 |
| 1990s | 人脸识别、Eigenfaces |
| 2010 | ImageNet 大规模数据集 |
| 2012 | AlexNet 深度学习突破 |
| 2014 | GAN 生成对抗网络 |
| 2015 | ResNet 超越人类识别 |
| 2016 | YOLO 实时目标检测 |
| 2020s | CLIP、DALL-E 多模态 |

关键突破:
  • 2012: AlexNet (CNN) ImageNet 竞赛
  • 2014: GAN (生成对抗网络)
  • 2015: ResNet (残差网络)
  • 2017: Transformer 应用于 CV
  • 2020: CLIP (多模态)
""")

print()
print("=" * 60)
print("3. 主要任务")
print("=" * 60)

print("""
3.1 图像分类 (Image Classification)

  输入: 一张图像
  输出: 类别标签

  示例: 猫/狗/汽车/飞机

3.2 目标检测 (Object Detection)

  输入: 一张图像
  输出: 多个边界框 + 类别

  算法: YOLO, R-CNN, SSD

3.3 语义分割 (Semantic Segmentation)

  输入: 一张图像
  输出: 每个像素的类别

  算法: FCN, U-Net, DeepLab

3.4 实例分割 (Instance Segmentation)

  输入: 一张图像
  输出: 每个物体的像素 + 类别

  算法: Mask R-CNN

3.5 人脸识别 (Face Recognition)

  人脸检测 → 人脸对齐 → 特征提取 → 比对

3.6 姿态估计 (Pose Estimation)

  检测人体关键点: 头、肩、肘、膝等

3.7 图像生成 (Image Generation)

  GAN, VAE, Diffusion Models
""")

print()
print("=" * 60)
print("4. 应用领域")
print("=" * 60)

print("""
| 领域 | 应用 |
|------|------|
| 安防 | 人脸门禁、视频监控 |
| 医疗 | CT/MRI 影像分析 |
| 自动驾驶 | 车道线、障碍物检测 |
| 零售 | 商品识别、无人零售 |
| 农业 | 病虫害检测 |
| 制造业 | 缺陷检测 |
| 娱乐 | AR/VR、AI 绘画 |

热门应用:
  • AI 绘画: DALL-E, Midjourney, Stable Diffusion
  • 换脸: DeepFaceLab
  • 视频生成: Sora
  • 自动驾驶: Tesla FSD
""")

print()
print("=" * 60)
print("5. 常用数据集")
print("=" * 60)

print("""
5.1 图像分类数据集

  • MNIST: 手写数字 (10类, 7万图)
  • CIFAR-10/100: 小图像 (10/100类)
  • ImageNet: 大规模 (1000类, 140万图)
  • Fashion-MNIST: 服装分类

5.2 目标检测数据集

  • COCO: 80类, 33万图像
  • PASCAL VOC: 20类
  • KITTI: 自动驾驶场景

5.3 语义分割数据集

  • Cityscapes: 城市场景
  • ADE20K: 室内外场景

5.4 人脸数据集

  • LFW: 人脸验证
  • CelebA: 人脸属性
""")

print()
print("=" * 60)
print("6. 常用库")
print("=" * 60)

print("""
6.1 深度学习框架

  PyTorch:
    pip install torch torchvision

  TensorFlow:
    pip install tensorflow

6.2 计算机视觉库

  OpenCV:
    pip install opencv-python

    功能: 图像处理、摄像头、特征检测

  Pillow (PIL):
    pip install pillow

    功能: 基础图像操作

  scikit-image:
    pip install scikit-image

    功能: 图像处理算法

6.3 目标检测库

  MMDetection:
    pip install mmdet

  Detectron2:
    pip install detectron2

6.4 数据增强

  Albumentations:
    pip install albumentations
""")

print()
print("=" * 60)
print("7. 评估指标")
print("=" * 60)

print("""
7.1 图像分类

  • Accuracy (准确率)
  • Top-5 Error Rate
  • Precision/Recall/F1

7.2 目标检测

  • mAP (mean Average Precision)
  • IoU (Intersection over Union)
  • FPS (帧率)

  IoU = A ∩ B / A ∪ B

  AP: PR 曲线下面积
  mAP: 各类 AP 的平均值

7.3 语义分割

  • Pixel Accuracy
  • Mean IoU
  • Mean Accuracy

7.4 人脸识别

  • FAR (False Accept Rate)
  • FRR (False Reject Rate)
  • TAR (True Accept Rate)
""")

print()
print("=" * 60)
print("8. 第一个 CV 程序")
print("=" * 60)

print('''
# 使用 OpenCV 读取和显示图像

import cv2

# 读取图像
img = cv2.imread("image.jpg")

# 获取图像信息
print(f"Shape: {img.shape}")
print(f"Size: {img.size}")
print(f"Dtype: {img.dtype}")

# 显示图像
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存图像
cv2.imwrite("output.jpg", img)


# 使用 PIL
from PIL import Image

img = Image.open("image.jpg")
print(img.size, img.mode)

# 转换为数组
import numpy as np
arr = np.array(img)


# 使用 torchvision 加载数据
import torchvision.datasets as datasets

train_dataset = datasets.CIFAR10(
    root="./data",
    train=True,
    download=True
)
''')

print()
print("=" * 60)
print("9. 深度学习 CV 流程")
print("=" * 60)

print("""
9.1 数据准备

  • 收集数据
  • 标注数据
  • 数据清洗
  • 数据增强

9.2 数据加载

  • Dataset: 封装数据和标签
  • DataLoader: 批量加载

9.3 模型选择

  • 图像分类: ResNet, EfficientNet
  • 目标检测: YOLO, Faster R-CNN
  • 语义分割: DeepLabV3, U-Net

9.4 训练

  • 定义损失函数
  • 选择优化器
  • 设置学习率
  • 训练循环

9.5 评估

  • 在测试集上评估
  • 分析错误案例

9.6 部署

  • 模型导出 (ONNX, TorchScript)
  • 推理优化
  • 服务化
""")

print()
print("=" * 60)
print("10. 学习路径")
print("=" * 60)

print("""
推荐学习路线:

阶段1: 基础
  • 图像处理 (OpenCV)
  • NumPy 图像操作
  • 数据集使用

阶段2: 深度学习
  • CNN 原理
  • PyTorch/TensorFlow
  • 图像分类

阶段3: 进阶
  • 目标检测 (YOLO)
  • 语义分割
  • 人脸识别

阶段4: 高级
  • GAN 生成对抗网络
  • Diffusion Models
  • Transformer (ViT)

实战项目:
  • 猫狗分类
  • 口罩检测
  • 车道线检测
  • AI 头像生成
""")

print()
print("=" * 60)
print("11. PyTorch Vision 基础")
print("=" * 60)

print('''
import torch
import torchvision
import torchvision.transforms as transforms

# 数据转换
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 加载数据集
train_dataset = torchvision.datasets.CIFAR10(
    root="./data",
    train=True,
    transform=transform,
    download=True
)

test_dataset = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    transform=transform,
    download=True
)

# DataLoader
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4
)

# 查看数据
for images, labels in train_loader:
    print(images.shape)  # [64, 3, 224, 224]
    print(labels.shape)  # [64]
    break
''')

print()
print("=" * 60)
print("12. 预训练模型")
print("=" * 60)

print('''
import torchvision.models as models

# 加载预训练模型
resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

# 使用模型进行特征提取
import torch.nn as nn

# 冻结参数
for param in resnet.parameters():
    param.requires_grad = False

# 修改最后的分类层
num_classes = 10
resnet.fc = nn.Linear(resnet.fc.in_features, num_classes)

# 常用预训练模型
# 分类
models.resnet18(weights="IMAGENET1K_V1")
models.vgg16(weights="IMAGENET1K_V1")
models.efficientnet_b0(weights="IMAGENET1K_V1")
models.mobilenet_v2(weights="IMAGENET1K_V1")

# 语义分割
models.segmentation.deeplabv3_resnet50(weights="DEFAULT")

# 目标检测
# 需要使用其他库 (torchvision, mmdetection)
''')

print()
print("=" * 60)
print("13. 数据增强")
print("=" * 60)

print('''
import torchvision.transforms as transforms

# 训练时的数据增强
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# 测试时只做基础转换
test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# 使用 Albumentations (更强大的增强)
import albumentations as A

transform = A.Compose([
    A.RandomBrightnessContrast(p=0.5),
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
''')

print()
print("=" * 60)
print("14. 图像处理基础")
print("=" * 60)

print("""
14.1 基本概念

  • 像素: 图像的基本单元
  • 通道: R, G, B (彩色) / 灰度
  • 分辨率: 宽 × 高

14.2 常见操作

  • 缩放: resize
  • 裁剪: crop
  • 旋转: rotate
  • 翻转: flip
  • 亮度/对比度调整

14.3 滤波器

  • 均值滤波: 平滑
  • 高斯滤波: 去噪
  • 边缘检测: Canny, Sobel
  • 锐化

14.4 形态学操作

  • 腐蚀: 去除小的噪点
  • 膨胀: 扩大区域
  • 开运算: 先腐蚀后膨胀
  • 闭运算: 先膨胀后腐蚀
""")

print()
print("=" * 60)
print("15. CV 总结")
print("=" * 60)

print("""
计算机视觉要点:

✓ 核心任务:
  • 分类、检测、分割、生成

✓ 深度学习方法:
  • CNN (卷积神经网络)
  • Transformer (ViT)
  • GAN (生成对抗网络)

✓ 常用工具:
  • PyTorch / TensorFlow
  • OpenCV
  • MMDetection

✓ 学习建议:
  • 先掌握基础概念
  • 多动手实践
  • 关注前沿论文

✓ 发展趋势:
  • 多模态 (CLIP, GPT-4V)
  • 大模型 (SAM, DINOv2)
  • 生成模型 (Stable Diffusion)
""")
