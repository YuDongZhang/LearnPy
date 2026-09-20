# 1. AI概述

## 什么是人工智能

**人工智能 (AI)** 是让计算机具有人类智能的技术。

**机器学习 (ML)** 是 AI 的一个分支，让计算机从数据中学习。

**深度学习 (DL)** 是机器学习的一个分支，使用神经网络模拟人脑。

三者是包含关系：AI ⊃ ML ⊃ DL。

## AI技术图谱

```
人工智能 (Artificial Intelligence, AI)
    │
    ├── 机器学习 (Machine Learning, ML)
    │   │
    │   ├── 监督学习 (有标签数据)
    │   │   ├── 分类
    │   │   └── 回归
    │   │
    │   ├── 无监督学习 (无标签数据)
    │   │   ├── 聚类
    │   │   └── 降维
    │   │
    │   └── 强化学习 (奖励机制)
    │
    └── 深度学习 (Deep Learning, DL)
        ├── 神经网络
        ├── 卷积神经网络 (CNN)
        └── 循环神经网络 (RNN)
```

## AI发展历程

| 年份 | 里程碑 |
|------|--------|
| 1956 | AI 概念诞生 |
| 1997 | Deep Blue 战胜国际象棋冠军 |
| 2012 | AlexNet 引领深度学习革命 |
| 2016 | AlphaGo 战胜围棋冠军 |
| 2022 | ChatGPT 引发大语言模型热潮 |

## AI应用领域

| 领域 | 应用 |
|------|------|
| 计算机视觉 | 人脸识别、自动驾驶 |
| 自然语言处理 | 机器翻译、聊天机器人 |
| 推荐系统 | 抖音推荐、电商推荐 |
| 语音识别 | 语音助手、Siri |
| 生成式 AI | AI 绘画、AI 写作 |

## 常见AI库

| 库 | 用途 |
|---|---|
| NumPy | 数值计算 |
| Pandas | 数据处理 |
| Matplotlib | 数据可视化 |
| Scikit-learn | 传统机器学习 |
| TensorFlow | 深度学习 |
| PyTorch | 深度学习 |

安装方式：

```bash
# 基础数据科学栈
pip install numpy pandas matplotlib scikit-learn

# 深度学习 (二选一)
pip install tensorflow  # Google
pip install torch       # PyTorch
```

## 机器学习基本流程

```
1. 定义问题     →  明确要解决什么问题
2. 收集数据     →  获取训练所需的数据
3. 数据预处理   →  清洗、转换、特征工程
4. 选择模型     →  选择合适的算法
5. 训练模型     →  用数据训练模型
6. 评估模型     →  用测试集评估性能
7. 部署模型     →  将模型应用到实际场景
```

## 数据集划分

- 训练集 (Training Set)：70-80%，用于训练
- 验证集 (Validation Set)：10-15%，用于调参
- 测试集 (Test Set)：10-15%，用于评估

注意：测试集不应该参与训练！

## 常见评估指标

回归问题：

| 指标 | 名称 | 含义 |
|------|------|------|
| MAE | 平均绝对误差 | 预测值与真实值的绝对误差 |
| MSE | 均方误差 | 预测值与真实值误差的平方 |
| RMSE | 均方根误差 | MSE 的平方根 |
| R² | 决定系数 | 模型解释变量的程度 |

分类问题：

| 指标 | 名称 | 含义 |
|------|------|------|
| Accuracy | 准确率 | 正确预测的比例 |
| Precision | 精确率 | 预测为正例中实际正例的比例 |
| Recall | 召回率 | 实际正例中被预测正确的比例 |
| F1 Score | F1 分数 | 精确率和召回率的调和平均 |

## 第一个AI程序

```python
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

model = LinearRegression()
model.fit(X, y)

prediction = model.predict([[6]])[0]
# 模型学到 y = 2x，预测 x=6 时 y=12
```

## 学习路径建议

1. Python 基础
2. NumPy / Pandas 数据处理
3. Matplotlib 数据可视化
4. Scikit-learn 机器学习
5. 深度学习 (TensorFlow 或 PyTorch)
6. 实战项目

推荐资源：书籍《Python机器学习》《深度学习入门》；课程 Coursera、Fast.ai；实践 Kaggle 竞赛。

## 代码

讲解对应的示例代码见 `1_ai_overview.py`。
