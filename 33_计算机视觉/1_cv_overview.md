# 1. CV概述

## 什么是计算机视觉

**计算机视觉 (Computer Vision, CV)** 让计算机具有人类视觉的能力，能够"看懂"图像和视频。

CV 的核心问题：
- 图像分类：这张图片是什么？
- 目标检测：图片里有哪些物体？在哪里？
- 语义分割：每个像素属于哪个类别？
- 人脸识别：这是谁？
- 姿态估计：人的姿势是什么样的？
- 图像生成：生成逼真的图像

为什么重要：人类获取信息 80% 来自视觉；应用广泛（安防、医疗、自动驾驶）；图像/视频数据爆发式增长。

## 发展历程

| 年份 | 里程碑 |
|------|--------|
| 1966 | MIT 夏季视觉项目起步 |
| 1990s | 人脸识别、Eigenfaces |
| 2010 | ImageNet 大规模数据集 |
| 2012 | AlexNet 深度学习突破 |
| 2014 | GAN 生成对抗网络 |
| 2015 | ResNet 超越人类识别 |
| 2016 | YOLO 实时目标检测 |
| 2020s | CLIP、DALL-E 多模态 |

关键突破：AlexNet (2012, CNN) → GAN (2014) → ResNet (2015, 残差网络) → Transformer 应用于 CV (2017) → CLIP (2020, 多模态)。

## 主要任务

| 任务 | 输入 → 输出 | 代表算法 |
|------|------------|---------|
| 图像分类 | 图像 → 类别标签 | ResNet, EfficientNet |
| 目标检测 | 图像 → 多个边界框 + 类别 | YOLO, R-CNN, SSD |
| 语义分割 | 图像 → 每个像素的类别 | FCN, U-Net, DeepLab |
| 实例分割 | 图像 → 每个物体的像素 + 类别 | Mask R-CNN |
| 人脸识别 | 检测 → 对齐 → 特征提取 → 比对 | — |
| 姿态估计 | 图像 → 人体关键点 | — |
| 图像生成 | 噪声/文本 → 图像 | GAN, VAE, Diffusion |

## 应用领域

| 领域 | 应用 |
|------|------|
| 安防 | 人脸门禁、视频监控 |
| 医疗 | CT/MRI 影像分析 |
| 自动驾驶 | 车道线、障碍物检测 |
| 零售 | 商品识别、无人零售 |
| 农业 | 病虫害检测 |
| 制造业 | 缺陷检测 |
| 娱乐 | AR/VR、AI 绘画 |

热门应用：AI 绘画（DALL-E、Midjourney、Stable Diffusion）、视频生成（Sora）、自动驾驶（Tesla FSD）。

## 常用数据集

- 图像分类：MNIST（手写数字）、CIFAR-10/100、ImageNet（1000类, 140万图）、Fashion-MNIST
- 目标检测：COCO（80类, 33万图）、PASCAL VOC、KITTI（自动驾驶）
- 语义分割：Cityscapes、ADE20K
- 人脸：LFW（验证）、CelebA（属性）

## 常用库

| 库 | 用途 | 安装 |
|----|------|------|
| PyTorch + torchvision | 深度学习框架 | `pip install torch torchvision` |
| OpenCV | 图像处理、摄像头、特征检测 | `pip install opencv-python` |
| Pillow | 基础图像操作 | `pip install pillow` |
| scikit-image | 图像处理算法 | `pip install scikit-image` |
| Albumentations | 数据增强 | `pip install albumentations` |
| MMDetection / Detectron2 | 目标检测 | `pip install mmdet` |

## 评估指标

| 任务 | 指标 |
|------|------|
| 图像分类 | Accuracy、Top-5 Error、Precision/Recall/F1 |
| 目标检测 | mAP、IoU、FPS |
| 语义分割 | Pixel Accuracy、Mean IoU |
| 人脸识别 | FAR（误识率）、FRR（拒识率）、TAR |

```
IoU = A ∩ B / A ∪ B          # 预测框与真实框的重叠程度
mAP = 各类别 AP 的平均值      # AP: PR 曲线下面积
```

## 第一个CV程序

```python
import cv2

img = cv2.imread("image.jpg")     # 读取
print(img.shape)                  # (height, width, channels)
cv2.imshow("Image", img)          # 显示
cv2.imwrite("output.jpg", img)    # 保存
```

## 深度学习CV流程

```
数据准备(收集/标注/增强) → Dataset/DataLoader 加载
→ 模型选择(ResNet/YOLO/U-Net) → 训练(损失/优化器/调度)
→ 评估(测试集/错误分析) → 部署(ONNX/TorchScript/服务化)
```

## 学习路径建议

1. 基础：图像处理 (OpenCV)、NumPy 图像操作、数据集使用
2. 深度学习：CNN 原理、图像分类
3. 进阶：目标检测 (YOLO)、语义分割、人脸识别
4. 高级：GAN、Diffusion Models、Transformer (ViT)

实战项目：猫狗分类、口罩检测、车道线检测、AI 头像生成。

## 代码

讲解对应的示例代码见 `1_cv_overview.py`。
