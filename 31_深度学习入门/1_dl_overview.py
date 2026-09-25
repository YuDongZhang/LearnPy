"""
深度学习概述与环境准备
====================

深度学习 (Deep Learning) 是机器学习的重要分支，
使用多层神经网络来学习数据的表征。

本文件所有代码真实可运行，包括：环境验证、激活函数、
损失函数、第一个训练循环、第一个神经网络前向传播。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("1. 深度学习简介")
print("=" * 60)

print("""
深度学习 vs 传统机器学习:

传统机器学习:
  - 需要人工提取特征
  - 数据量小的时候效果好
  - 可解释性较好

深度学习:
  - 自动学习特征 (端到端)
  - 需要大量数据
  - 适合图像、语音、文本等复杂数据
""")

print()
print("=" * 60)
print("2. 环境验证 (真实运行)")
print("=" * 60)

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
else:
    print("(CPU 版 torch, 无 GPU 属正常, 本教学代码均可运行)")

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # 屏蔽 TF 日志
import tensorflow as tf

print(f"TensorFlow 版本: {tf.__version__} (Keras {tf.keras.__version__})")

# 两个框架各自做一次张量运算
t_torch = torch.rand(3, 4) @ torch.rand(4, 2)
t_tf = tf.matmul(tf.random.normal((3, 4)), tf.random.normal((4, 2)))
print(f"torch 矩阵乘法输出形状: {tuple(t_torch.shape)}")
print(f"tensorflow 矩阵乘法输出形状: {tuple(t_tf.shape)}")

print()
print("=" * 60)
print("3. 激活函数 (真实计算)")
print("=" * 60)

x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
print(f"输入:     {x.tolist()}")
print(f"Sigmoid:  {[round(v, 4) for v in torch.sigmoid(x).tolist()]}")
print(f"Tanh:     {[round(v, 4) for v in torch.tanh(x).tolist()]}")
print(f"ReLU:     {F.relu(x).tolist()}")

logits = torch.tensor([[1.0, 2.0, 3.0]])
probs = F.softmax(logits, dim=-1)
print(f"\nSoftmax (多分类输出): logits={logits.tolist()} -> 概率={[round(v, 4) for v in probs.squeeze().tolist()]}")
print("解读: ReLU 最常用 (正数原样通过, 负数置 0); Softmax 把分数变成和为 1 的概率")

print()
print("=" * 60)
print("4. 损失函数 (真实计算)")
print("=" * 60)

# 回归: MSE 均方误差
pred = torch.tensor([2.5, 0.0, 2.0])
target = torch.tensor([3.0, 0.0, 2.0])
print(f"MSE  (回归): {F.mse_loss(pred, target).item():.4f}  (预测[2.5,0,2] vs 真实[3,0,2])")

# 分类: 交叉熵
ce = F.cross_entropy(logits, torch.tensor([2]))
print(f"CrossEntropy (分类): {ce.item():.4f}  (真实类别=2, logits[2]=3 最大, 损失小)")
print("解读: 预测越接近真实值/正确类别, 损失越小; 训练的目标就是让损失下降")

print()
print("=" * 60)
print("5. 第一个训练程序: 拟合 y = 2x + 1")
print("=" * 60)

# 用结构化数据 (真实规律 y=2x+1), 观察损失下降、参数逼近目标值
torch.manual_seed(42)
X = torch.linspace(-1, 1, 32).reshape(-1, 1)  # 32 个样本
y_true = 2 * X + 1                             # 真实规律

model = nn.Linear(1, 1)                        # 一个神经元的线性模型
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

print("训练循环: 前向传播 -> 计算损失 -> 反向传播 -> 更新参数")
for epoch in range(1, 201):
    y_pred = model(X)              # 前向传播
    loss = criterion(y_pred, y_true)  # 计算损失

    optimizer.zero_grad()          # 清零梯度
    loss.backward()                # 反向传播
    optimizer.step()               # 更新参数

    if epoch in (1, 10, 50, 100, 200):
        print(f"  epoch {epoch:3d}: loss = {loss.item():.4f}")

w = model.weight.item()
b = model.bias.item()
print(f"\n学到的参数: w = {w:.3f} (目标 2.0), b = {b:.3f} (目标 1.0)")
print("解读: 损失从 0.57 一路降到接近 0, 参数自动逼近真实规律 —— 这就是训练")

print()
print("=" * 60)
print("6. 第一个神经网络: 前向传播")
print("=" * 60)


class SimpleNet(nn.Module):
    """手写数字网络: 784 -> 256 -> 10"""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(-1, 784)          # 展平 (batch, 1, 28, 28) -> (batch, 784)
        x = self.relu(self.fc1(x))
        return self.fc2(x)


model = SimpleNet()
n_params = sum(p.numel() for p in model.parameters())

fake_images = torch.randn(32, 1, 28, 28)  # 模拟一个 batch: 32张28x28灰度图
with torch.no_grad():                     # 推理不需要梯度
    out = model(fake_images)

print(f"输入形状: {tuple(fake_images.shape)}  (32 张 28x28 图片)")
print(f"输出形状: {tuple(out.shape)}  (每张图 10 个类别的得分)")
print(f"参数量: {n_params:,}  (fc1: {784*256+256:,}, fc2: {256*10+10:,})")

print()
print("=" * 60)
print("7. 训练流程总结与学习路径")
print("=" * 60)

print("""
深度学习训练步骤:
  1. 数据准备   -> 加载、增强、批量处理 (DataLoader)
  2. 模型构建   -> 定义网络结构 (nn.Module)
  3. 训练循环   -> 前向传播 -> 损失 -> 反向传播 -> 更新参数
  4. 模型评估   -> 验证集评估、超参数调整
  5. 模型保存   -> torch.save / 保存权重

学习路径:
  阶段1 基础:    神经网络原理、PyTorch/TF 入门
  阶段2 CV:     CNN、图像分类、目标检测
  阶段3 NLP:    RNN/LSTM、Transformer、BERT/GPT
  阶段4 进阶:    GAN、强化学习、模型部署、分布式训练

资源推荐:
  - 《深度学习入门》(斋藤康毅) / 《动手学深度学习》(李沐)
  - Fast.ai / 斯坦福 CS231n / CS224n
  - Kaggle 竞赛实践
""")
