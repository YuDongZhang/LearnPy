"""
人工智能概述与环境准备
=====================

介绍 AI 基础知识并检查开发环境。
"""

print("=" * 60)
print("1. 人工智能简介")
print("=" * 60)

print("""
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
""")

print()
print("=" * 60)
print("2. AI 开发环境检查")
print("=" * 60)

def check_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', '未知')
        print(f"  ✓ {package_name}: {version}")
        return True
    except ImportError:
        print(f"  ✗ {package_name}: 未安装")
        return False

print("检查常用 AI 库:")
packages = [
    ("NumPy", "numpy"),
    ("Pandas", "pandas"),
    ("Matplotlib", "matplotlib"),
    ("Scikit-learn", "sklearn"),
    ("TensorFlow", "tensorflow"),
    ("PyTorch", "torch"),
]

for name, import_name in packages:
    check_package(name, import_name)

print()
print("=" * 60)
print("3. 机器学习基本流程")
print("=" * 60)

print("""
机器学习项目流程:
┌─────────────────────────────────────────────────────────┐
│  1. 定义问题     →  明确要解决什么问题                   │
│  2. 收集数据     →  获取训练所需的数据                   │
│  3. 数据预处理   →  清洗、转换、特征工程                 │
│  4. 选择模型     →  选择合适的算法                      │
│  5. 训练模型     →  用数据训练模型                       │
│  6. 评估模型     →  用测试集评估性能                     │
│  7. 部署模型     →  将模型应用到实际场景                 │
└─────────────────────────────────────────────────────────┘
""")

print()
print("=" * 60)
print("4. 数据集划分")
print("=" * 60)

print("""
通常将数据划分为:
  ├── 训练集 (Training Set)   - 70-80% 用于训练
  ├── 验证集 (Validation Set) - 10-15% 用于调参
  └── 测试集 (Test Set)       - 10-15% 用于评估

注意: 测试集不应该参与训练！
""")

print()
print("=" * 60)
print("5. 常见评估指标")
print("=" * 60)

print("回归问题:")
metrics_regression = [
    ("MAE", "平均绝对误差", "预测值与真实值的绝对误差"),
    ("MSE", "均方误差", "预测值与真实值误差的平方"),
    ("RMSE", "均方根误差", "MSE 的平方根"),
    ("R²", "决定系数", "模型解释变量的程度"),
]

for metric, name, desc in metrics_regression:
    print(f"  {metric}: {name} - {desc}")

print("\n分类问题:")
metrics_classification = [
    ("Accuracy", "准确率", "正确预测的比例"),
    ("Precision", "精确率", "预测为正例中实际正例的比例"),
    ("Recall", "召回率", "实际正例中被预测正确的比例"),
    ("F1 Score", "F1 分数", "精确率和召回率的调和平均"),
]

for metric, name, desc in metrics_classification:
    print(f"  {metric}: {name} - {desc}")

print()
print("=" * 60)
print("6. 安装 AI 库")
print("=" * 60)

print("推荐安装方式:")
print("""
# 基础数据科学栈
pip install numpy pandas matplotlib scikit-learn

# 深度学习 (二选一)
pip install tensorflow  # Google
pip install torch       # Facebook (PyTorch)

# 辅助工具
pip install jupyter notebook  # 交互式编程环境
pip install seaborn           # 统计数据可视化
pip install pillow            # 图像处理
""")

print()
print("=" * 60)
print("7. 第一个 AI 程序")
print("=" * 60)

try:
    import numpy as np
    from sklearn.linear_model import LinearRegression
    
    print("使用 Scikit-learn 训练第一个模型...")
    
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 4, 6, 8, 10])
    
    model = LinearRegression()
    model.fit(X, y)
    
    prediction = model.predict([[6]])[0]
    
    print(f"训练数据: X = {X.flatten()}, y = {y}")
    print(f"模型: y = {model.coef_[0]:.1f}x + {model.intercept_:.1f}")
    print(f"预测: 当 x=6 时，y = {prediction:.1f}")
    
except ImportError as e:
    print(f"注意: {e}")
    print("请运行以下命令安装必要的库:")
    print("  pip install numpy pandas scikit-learn")
    print("\n示例代码 (安装后可正常运行):")
    print("""
# 准备数据
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# 创建并训练模型
model = LinearRegression()
model.fit(X, y)

# 预测
prediction = model.predict([[6]])[0]
print(f"预测结果: {prediction}")""")

print()
print("=" * 60)
print("8. AI 学习路径建议")
print("=" * 60)

print("""
入门推荐学习路径:

1. Python 基础 ✓
2. NumPy / Pandas 数据处理
3. Matplotlib 数据可视化
4. Scikit-learn 机器学习
5. 深度学习 (TensorFlow 或 PyTorch)
6. 实战项目

推荐资源:
  • 书籍: 《Python机器学习》、《深度学习入门》
  • 课程: Coursera、Fast.ai
  • 实践: Kaggle 竞赛
""")
