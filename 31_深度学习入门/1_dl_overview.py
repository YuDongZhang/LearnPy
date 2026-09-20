"""
深度学习概述与环境准备
====================

深度学习 (Deep Learning) 是机器学习的一个重要分支，
使用多层神经网络来学习数据的表征。
"""

print("=" * 60)
print("1. 深度学习简介")
print("=" * 60)

print("""
深度学习 vs 传统机器学习:

传统机器学习:
  • 需要人工提取特征
  • 数据量小的时候效果好
  • 可解释性较好
  • 算法: SVM, 决策树, 线性回归等

深度学习:
  • 自动学习特征
  • 需要大量数据
  • 可解释性较差
  • 适合图像、语音、文本等复杂数据

深度学习的特点:
  ✓ 端到端学习
  ✓ 特征自动提取
  ✓ 大数据驱动
  ✓ 强大的表示能力
""")

print()
print("=" * 60)
print("2. 深度学习发展历程")
print("=" * 60)

print("""
1943: 感知机 (Perceptron) - 最早的神经网络
1958: Rosenblatt 提出感知机算法
1969: Minsky 指出感知机的局限性
1986: Backpropagation 算法提出
1998: LeNet-5 手写数字识别
2012: AlexNet ImageNet 竞赛突破
2014: GAN 生成对抗网络
2015: ResNet 解决深层网络训练问题
2016: AlphaGo 战胜李世石
2017: Transformer 架构提出
2020: GPT-3 大语言模型
""")

print()
print("=" * 60)
print("3. 神经网络类型")
print("=" * 60)

print("""
按网络结构分类:

1. 前馈神经网络 (FNN)
   • 全连接神经网络 (DNN)
   • 卷积神经网络 (CNN)

2. 循环神经网络 (RNN)
   • LSTM
   • GRU

3. Transformer
   • Attention 机制
   • BERT, GPT 等

按任务分类:

• 回归任务: 房价预测, 温度预测
• 分类任务: 图像分类, 文本分类
• 生成任务: 文本生成, 图像生成
• 强化学习: 游戏, 机器人
""")

print()
print("=" * 60)
print("4. 常见深度学习框架")
print("=" * 60)

print("""
主流深度学习框架:

1. TensorFlow (Google)
   • 2015年发布
   • Keras 高层API
   • TensorBoard 可视化
   • 生态完善

2. PyTorch (Facebook)
   • 2016年发布
   • 动态计算图
   • Pythonic 设计
   • 研究首选

3. JAX (Google)
   • 2018年发布
   • 函数式编程
   • 高性能

4. MindSpore (华为)
   • 2020年发布
   • 端云协同

推荐: 初学者从 PyTorch 或 TensorFlow Keras 开始
""")

print()
print("=" * 60)
print("5. 安装深度学习环境")
print("=" * 60)

print("""
# PyTorch (推荐)
pip install torch torchvision torchaudio

# TensorFlow
pip install tensorflow

# 验证安装
python -c "import torch; print(torch.__version__)"
python -c "import tensorflow as tf; print(tf.__version__)"

# GPU 版本 PyTorch (需要 CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
""")

print()
print("=" * 60)
print("6. GPU 环境检查")
print("=" * 60)

print("""
# 检查 CUDA 是否可用
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU数量: {torch.cuda.device_count()}")
""")

print()
print("=" * 60)
print("7. 深度学习核心概念")
print("=" * 60)

print("""
7.1 神经网络基本结构

输入层 → 隐藏层 → 输出层

全连接层: y = f(Wx + b)

7.2 激活函数

• Sigmoid: σ(x) = 1/(1+e^-x)  (0-1)
• Tanh: tanh(x)              (-1 to 1)
• ReLU: max(0, x)             (常用!)
• Leaky ReLU: max(0.01x, x)
• Softmax: 用于多分类

7.3 损失函数

• MSE: 均方误差 (回归)
• CrossEntropy: 交叉熵 (分类)
• BCE: 二元交叉熵 (二分类)

7.4 优化器

• SGD: 随机梯度下降
• Adam: 自适应学习率 (常用!)
• AdamW: 带权重衰减的 Adam
• RMSprop: 自适应学习率
""")

print()
print("=" * 60)
print("8. 训练流程")
print("=" * 60)

print("""
深度学习训练步骤:

1. 数据准备
   • 数据加载
   • 数据增强
   • 批量处理

2. 模型构建
   • 定义网络结构
   • 初始化参数

3. 训练循环
   for epoch in range(num_epochs):
       for batch in dataloader:
           # 前向传播
           outputs = model(inputs)
           loss = criterion(outputs, labels)

           # 反向传播
           optimizer.zero_grad()
           loss.backward()
           optimizer.step()

4. 模型评估
   • 验证集评估
   • 超参数调整

5. 模型保存/部署
   • 保存权重
   • 导出模型
""")

print()
print("=" * 60)
print("9. 第一个深度学习程序")
print("=" * 60)

print("""
# PyTorch 示例: 简单神经网络

import torch
import torch.nn as nn

# 定义模型
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(-1, 784)  # 展平
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 创建模型
model = SimpleNet()

# 定义损失和优化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练 (伪代码)
for epoch in range(10):
    for images, labels in dataloader:
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
""")

print()
print("=" * 60)
print("10. 深度学习学习路径")
print("=" * 60)

print("""
推荐学习路线:

阶段1: 基础
  • 神经网络原理
  • PyTorch/TensorFlow 入门
  • 简单项目实战

阶段2: 计算机视觉
  • CNN 原理
  • 图像分类 (ResNet, VGG)
  • 目标检测 (YOLO, Faster R-CNN)
  • 图像分割 (U-Net)

阶段3: 自然语言处理
  • RNN, LSTM, GRU
  • Transformer 原理
  • BERT, GPT
  • 文本分类, 机器翻译

阶段4: 进阶
  • GAN 生成对抗网络
  • 强化学习
  • 模型部署
  • 分布式训练

实战项目推荐:
  • MNIST/CIFAR 图像分类
  • IMDB 情感分析
  • 风格迁移
  • 人脸识别
  • 目标检测
""")

print()
print("=" * 60)
print("11. 资源推荐")
print("=" * 60)

print("""
书籍:
  • 《深度学习入门》- 斋藤康毅
  • 《Python深度学习》- François Chollet
  • 《动手学深度学习》- 李沐
  • 《神经网络与深度学习》- 邱锡鹏

在线课程:
  • Fast.ai - 实战导向
  • Coursera Deep Learning Specialization
  • 斯坦福 CS231n (计算机视觉)
  • 斯坦福 CS224n (NLP)

项目实践:
  • Kaggle 竞赛
  • GitHub 开源项目
  • 论文复现
""")
