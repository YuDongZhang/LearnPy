# 4. Scikit-learn机器学习示例

## Scikit-learn简介

Scikit-learn (sklearn) 是 Python 中最流行的传统机器学习库：

- 简单高效的机器学习工具
- 涵盖主流机器学习算法
- 统一的 API 设计

主要模块：

| 模块 | 用途 |
|------|------|
| datasets | 数据集 |
| linear_model | 线性模型 |
| tree | 决策树 |
| ensemble | 集成学习 |
| svm | 支持向量机 |
| neural_network | 神经网络 |
| metrics | 评估指标 |
| model_selection | 模型选择 |

安装：`pip install scikit-learn`

## 常用数据集

```python
from sklearn import datasets

iris = datasets.load_iris()            # 鸢尾花 (分类)
digits = datasets.load_digits()        # 手写数字 (分类)
diabetes = datasets.load_diabetes()    # 糖尿病 (回归)
breast_cancer = datasets.load_breast_cancer()  # 乳腺癌 (分类)

X, y = datasets.make_classification(n_samples=100)  # 生成模拟数据
```

## 统一API

sklearn 所有模型遵循同一套接口：

```python
model = SomeModel()       # 创建模型
model.fit(X_train, y_train)   # 训练
y_pred = model.predict(X_test)  # 预测
model.score(X_test, y_test)    # 评估
```

## 数据划分

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,    # 测试集比例
    random_state=42    # 随机种子
)
```

## 数据预处理

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 标准化 (均值为0，标准差为1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 测试集只 transform

# 归一化 (0-1区间)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
```

注意：测试集只能用 `transform`，不能用 `fit_transform`，否则会泄露测试集信息。

## 常用算法

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

model = LinearRegression()                     # 线性回归 (回归)
model = LogisticRegression()                   # 逻辑回归 (分类)
model = KNeighborsClassifier(n_neighbors=3)   # K近邻
model = DecisionTreeClassifier()               # 决策树
model = RandomForestClassifier(n_estimators=100)  # 随机森林
model = SVC(kernel='rbf')                      # 支持向量机
```

## 评估指标

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, mean_squared_error, r2_score
)

# 分类指标
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)   # 混淆矩阵

# 回归指标
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```

## 交叉验证

```python
from sklearn.model_selection import cross_val_score

# 5折交叉验证
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"平均准确率: {scores.mean():.2%}")
```

比单次划分更可靠：数据被分成5份，轮流做测试集。

## 超参数调优

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid=param_grid,
    cv=5,
    scoring='accuracy'
)
grid_search.fit(X_train, y_train)

print(grid_search.best_params_)     # 最佳参数
best_model = grid_search.best_estimator_
```

## 保存和加载模型

```python
import joblib

joblib.dump(model, 'model.pkl')           # 保存
loaded_model = joblib.load('model.pkl')   # 加载
```

## 完整流程示例

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 2. 划分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 3. 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 训练模型
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train_scaled, y_train)

# 5. 预测和评估
y_pred = model.predict(X_test_scaled)
print(f'准确率: {accuracy_score(y_test, y_pred):.2%}')
```

## 代码

讲解对应的示例代码见 `4_sklearn_demo.py`。
