# 1. 深度学习概述

## 深度学习 vs 传统机器学习

| 对比项 | 传统机器学习 | 深度学习 |
|--------|-------------|---------|
| 特征提取 | 人工提取 | 自动学习 |
| 数据量 | 小数据即可 | 需要大量数据 |
| 可解释性 | 较好 | 较差 |
| 适用场景 | 结构化数据 | 图像、语音、文本等复杂数据 |
| 代表算法 | SVM、决策树、线性回归 | CNN、RNN、Transformer |

深度学习的特点：端到端学习、特征自动提取、大数据驱动、强大的表示能力。

## 发展历程

| 年份 | 里程碑 |
|------|--------|
| 1943 | 感知机 (Perceptron) - 最早的神经网络 |
| 1958 | Rosenblatt 提出感知机算法 |
| 1986 | Backpropagation 算法提出 |
| 1998 | LeNet-5 手写数字识别 |
| 2012 | AlexNet ImageNet 竞赛突破 |
| 2014 | GAN 生成对抗网络 |
| 2015 | ResNet 解决深层网络训练问题 |
| 2016 | AlphaGo 战胜李世石 |
| 2017 | Transformer 架构提出 |
| 2020 | GPT-3 大语言模型 |

## 神经网络类型

按网络结构分类：

1. 前馈神经网络 (FNN)：全连接神经网络 (DNN)、卷积神经网络 (CNN)
2. 循环神经网络 (RNN)：LSTM、GRU
3. Transformer：Attention 机制，BERT、GPT 等

按任务分类：

| 任务 | 例子 |
|------|------|
| 回归 | 房价预测、温度预测 |
| 分类 | 图像分类、文本分类 |
| 生成 | 文本生成、图像生成 |
| 强化学习 | 游戏、机器人 |

## 深度学习框架

| 框架 | 开发方 | 特点 |
|------|--------|------|
| TensorFlow | Google (2015) | Keras 高层API、TensorBoard、生态完善 |
| PyTorch | Facebook (2016) | 动态计算图、Pythonic、研究首选 |
| JAX | Google (2018) | 函数式编程、高性能 |
| MindSpore | 华为 (2020) | 端云协同 |

推荐：初学者从 PyTorch 或 TensorFlow Keras 开始。

## 环境安装

```bash
# PyTorch (推荐)
pip install torch torchvision torchaudio

# TensorFlow
pip install tensorflow

# GPU 版本 PyTorch (需要 CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

GPU 检查：

```python
import torch
print(torch.cuda.is_available())       # CUDA 是否可用
print(torch.cuda.get_device_name(0))    # GPU 型号
```

## 核心概念

**网络结构**：输入层 → 隐藏层 → 输出层，全连接层 `y = f(Wx + b)`

**激活函数**：

- Sigmoid：σ(x) = 1/(1+e^-x)，输出 (0, 1)
- Tanh：输出 (-1, 1)
- ReLU：max(0, x)，最常用
- Softmax：用于多分类

**损失函数**：MSE（回归）、CrossEntropy（分类）、BCE（二分类）

**优化器**：SGD、Adam（常用）、AdamW、RMSprop

## 训练流程

```
1. 数据准备     → 加载、增强、批量处理
2. 模型构建     → 定义网络结构、初始化参数
3. 训练循环     → 前向传播 → 计算损失 → 反向传播 → 更新参数
4. 模型评估     → 验证集评估、超参数调整
5. 模型保存/部署 → 保存权重、导出模型
```

训练循环伪代码：

```python
for epoch in range(num_epochs):
    for batch in dataloader:
        outputs = model(inputs)        # 前向传播
        loss = criterion(outputs, labels)

        optimizer.zero_grad()          # 清零梯度
        loss.backward()                # 反向传播
        optimizer.step()               # 更新参数
```

## 学习路径

- 阶段1 基础：神经网络原理、框架入门、简单项目
- 阶段2 计算机视觉：CNN、图像分类、目标检测、分割
- 阶段3 NLP：RNN/LSTM、Transformer、BERT/GPT
- 阶段4 进阶：GAN、强化学习、部署、分布式训练

实战项目推荐：MNIST/CIFAR 图像分类、IMDB 情感分析、风格迁移、人脸识别、目标检测。

资源推荐：《深度学习入门》(斋藤康毅)、《Python深度学习》、《动手学深度学习》(李沐)；Fast.ai、Coursera、CS231n、CS224n；Kaggle 竞赛。

## 代码

讲解对应的示例代码见 `1_dl_overview.py`。
