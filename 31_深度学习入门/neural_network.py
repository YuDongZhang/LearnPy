"""
神经网络基础与原理
================

介绍神经网络的核心概念和工作原理。
"""

print("=" * 60)
print("1. 神经网络概述")
print("=" * 60)

print("""
神经网络 (Neural Network) 灵感来自生物神经元:

生物神经元:
  • 树突: 接收信号
  • 细胞体: 处理信号
  • 轴突: 传递信号

人工神经网络:
  • 输入: 接收数据
  • 权重: 调整信号强度
  • 激活函数: 决定是否传递信号
  • 输出: 预测结果

人脑有约 860 亿个神经元
深度学习网络有数百万到数千亿个参数
""")

print()
print("=" * 60)
print("2. 感知机 (Perceptron)")
print("=" * 60)

print("""
最简单的神经网络: 单层感知机

     x1 ──┐
          │
     x2 ──┼──→ ● ──→ y
          │
     x3 ──┘

公式: y = f(w1*x1 + w2*x2 + w3*x3 + b)

     • w: 权重 (weight)
     • b: 偏置 (bias)
     • f: 激活函数

感知机只能处理线性可分问题
""")

print()
print("=" * 60)
print("3. 多层神经网络")
print("=" * 60)

print("""
多层感知机 (MLP):

     输入层     隐藏层     输出层
       x1 ──► h1 ──► y1
       x2 ──► h2 ──► y2
       x3 ──► h3 ──►

全连接层: 每一层都连接到下一层所有节点

前向传播:
  h1 = f(W1*x + b1)
  y = W2*h1 + b2

反向传播: 计算梯度并更新参数
""")

print()
print("=" * 60)
print("4. 激活函数")
print("=" * 60)

print("""
为什么需要激活函数?

  • 引入非线性
  • 没有激活函数 = 线性组合 = 没用
  • 让网络学习复杂模式

常见激活函数:

1. Sigmoid
   f(x) = 1 / (1 + e^-x)
   输出: (0, 1)
   问题: 梯度消失

2. Tanh
   f(x) = tanh(x)
   输出: (-1, 1)
   问题: 梯度消失

3. ReLU (最常用!)
   f(x) = max(0, x)
   优点: 计算快, 缓解梯度消失
   问题: 神经元死亡

4. Leaky ReLU
   f(x) = max(0.01x, x)
   改进: 解决 ReLU 神经元死亡问题

5. Softmax
   用于多分类, 输出概率分布
""")

print()
print("=" * 60)
print("5. 损失函数")
print("=" * 60)

print("""
损失函数: 衡量模型预测与真实值的差距

1. 均方误差 (MSE) - 回归
   L = (1/n) * Σ(y_pred - y_true)²

2. 交叉熵 (CrossEntropy) - 分类
   L = -Σ y_true * log(y_pred)

   二分类:
   L = -[y*log(p) + (1-y)*log(1-p)]

3. Hinge Loss - SVM
   L = max(0, 1 - y*pred)

选择原则:
  • 回归 → MSE
  • 二分类 → Binary CrossEntropy
  • 多分类 → CrossEntropy
""")

print()
print("=" * 60)
print("6. 反向传播算法")
print("=" * 60)

print("""
反向传播 (Backpropagation):

链式法则计算梯度:
  ∂L/∂w = ∂L/∂y * ∂y/∂z * ∂z/∂w

步骤:
  1. 前向传播: 计算输出和损失
  2. 计算输出层梯度
  3. 反向传播: 逐层计算梯度
  4. 更新参数

梯度下降:
  w = w - learning_rate * gradient
""")

print()
print("=" * 60)
print("7. 优化器")
print("=" * 60)

print("""
优化器: 决定如何更新参数

1. SGD (随机梯度下降)
   w = w - lr * gradient
   缺点: 收敛慢, 容易陷入局部最优

2. Momentum
   v = momentum * v - lr * gradient
   w = w + v
   优点: 加速收敛

3. AdaGrad
   自适应调整学习率
   缺点: 学习率越来越小

4. RMSprop
   使用指数加权平均
   优点: 适合非平稳目标

5. Adam (最常用!)
   结合 Momentum 和 RMSprop
   优点: 收敛快, 稳定
   默认参数: lr=0.001, beta1=0.9, beta2=0.999
""")

print()
print("=" * 60)
print("8. 正则化")
print("=" * 60)

print("""
防止过拟合的技术:

1. L1 正则化
   L = Loss + λ * |w|
   → 产生稀疏权重 (特征选择)

2. L2 正则化 (Weight Decay)
   L = Loss + λ * w²
   → 权重衰减, 防止过大

3. Dropout
   训练时随机"关闭"部分神经元
   防止依赖单个神经元

4. Early Stopping
   验证集性能下降时停止训练

5. Data Augmentation
   数据增强, 增加样本多样性
""")

print()
print("=" * 60)
print("9. 超参数")
print("=" * 60)

print("""
重要超参数:

1. 学习率 (Learning Rate)
   • 最重要!
   • 太大: 不收敛
   •太小: 收敛太慢
   • 常用: 0.001, 0.0001
   • 技巧: 学习率衰减

2. 批量大小 (Batch Size)
   • 常用: 32, 64, 128, 256
   • 小批量: 泛化好, 噪声大
   • 大批量: 收敛快, 内存要求高

3. 网络层数
   • 太浅: 欠拟合
   • 太深: 梯度消失/爆炸

4. 隐藏层神经元数量
   • 根据任务复杂度调整
   • 一般 64, 128, 256, 512...

5. 训练轮数 (Epochs)
   • 太多: 过拟合
   • 技巧: 早停 (Early Stopping)
""")

print()
print("=" * 60)
print("10. 梯度问题")
print("=" * 60)

print("""
10.1 梯度消失 (Vanishing Gradient)

  • 原因: 链式乘法导致梯度指数衰减
  • 影响: 前面层无法学习
  • 解决: ReLU 激活, BatchNorm, 残差连接

10.2 梯度爆炸 (Exploding Gradient)

  • 原因: 梯度指数增长
  • 影响: 训练不稳定
  • 解决: 梯度裁剪 (Gradient Clipping)

10.3 批归一化 (Batch Normalization)

  • 归一化每层输入
  • 加速训练, 稳定梯度
  • 公式: y = (x - μ) / σ * γ + β

10.4 残差连接 (Residual Connection)

  • 跳跃连接: y = F(x) + x
  • 解决深层网络训练问题
  • ResNet 核心思想
""")

print()
print("=" * 60)
print("11. 训练技巧")
print("=" * 60)

print("""
实战技巧:

1. 数据预处理
   • 归一化/标准化
   • 处理缺失值
   • 特征工程

2. 权重初始化
   • Xavier 初始化
   • He 初始化

3. 学习率调度
   • Step LR
   • Cosine Annealing
   • Reduce on Plateau

4. 调试
   • 先用小数据集验证代码
   • 检查梯度流
   • 使用 TensorBoard 可视化

5. Ensemble
   • 多个模型投票
   • 提升稳定性
""")

print()
print("=" * 60)
print("12. 代码示例: 从零实现神经网络")
print("=" * 60)

print("""
import numpy as np

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, X):
        self.activations = [X]
        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            a = self.relu(z) if i < len(self.weights) - 1 else self.sigmoid(z)
            self.activations.append(a)
        return self.activations[-1]

    def backward(self, X, y, learning_rate):
        m = X.shape[0]
        delta = self.activations[-1] - y

        for i in range(len(self.weights) - 1, -1, -1):
            dw = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * (self.activations[i] > 0)

# 使用示例
nn = NeuralNetwork([4, 8, 8, 1])
X = np.random.randn(100, 4)
y = np.random.randint(0, 2, (100, 1))

for epoch in range(1000):
    output = nn.forward(X)
    nn.backward(X, y, 0.01)
""")
