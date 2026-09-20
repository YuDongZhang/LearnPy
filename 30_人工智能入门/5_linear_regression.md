# 5. 线性回归实战：预测房价

## 项目概述

项目目标：根据房屋特征预测房价。

数据特征（波士顿房价数据集）：

- 房间数量 (RM)
- 犯罪率 (CRIM)
- 房屋年龄 (AGE)
- 距离就业中心距离 (DIS)
- 税率 (TAX)

这是机器学习的经典回归问题，综合运用数据处理和模型训练。

## 加载数据

```python
from sklearn.datasets import load_boston
import pandas as pd

boston = load_boston()
X, y = boston.data, boston.target

df = pd.DataFrame(X, columns=boston.feature_names)
df['PRICE'] = y
print(f"数据集形状: {X.shape}")
```

## 数据探索

```python
print(df.describe())                        # 基本统计
print(df.isnull().sum())                    # 缺失值检查
print(df.corr()['PRICE'].sort_values(ascending=False))  # 相关性分析
```

先看数据再建模：了解分布、缺失情况和哪些特征与目标相关。

## 数据预处理

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X = df.drop('PRICE', axis=1)
y = df['PRICE']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

## 训练多个模型

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

models = {
    '线性回归': LinearRegression(),
    '岭回归': Ridge(alpha=1.0),
    'Lasso回归': Lasso(alpha=0.1),
    '随机森林': RandomForestRegressor(n_estimators=100, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results[name] = {'RMSE': rmse, 'MAE': mae, 'R²': r2}
    print(f"{name}: RMSE={rmse:.2f}, MAE={mae:.2f}, R²={r2:.4f}")
```

模型对比是实战常用手法：一次训练多个候选模型，用同一指标选出最佳。

## 模型评估对比

```python
results_df = pd.DataFrame(results).T
results_df = results_df.sort_values('R²', ascending=False)

best_model_name = results_df['R²'].idxmax()
print(f"最佳模型: {best_model_name}")
```

## 预测新数据

```python
new_house = pd.DataFrame({
    'RM': [5],      # 5个房间
    'CRIM': [0.1],  # 低犯罪率
    'AGE': [30],    # 30年房龄
    'DIS': [4],     # 距离就业中心4km
    'TAX': [300]    # 税率
})

new_house_scaled = scaler.transform(new_house)
predicted_price = best_model.predict(new_house_scaled)[0]
print(f"预测房价: ${predicted_price * 1000:.2f}")
```

## 模型解释

```python
lr_model = models['线性回归']
importance = pd.DataFrame({
    '特征': X.columns,
    '系数': lr_model.coef_
}).sort_values('系数', key=abs, ascending=False)
```

线性回归系数的解读：

- 系数 > 0：该特征增加，房价增加
- 系数 < 0：该特征增加，房价降低
- |系数| 越大，影响越大

## 项目总结

完整流程：

1. 定义问题 — 预测房价
2. 收集数据 — 加载数据集
3. 数据探索 — 统计分析
4. 数据预处理 — 划分数据集、标准化
5. 选择模型 — 线性回归、岭回归、随机森林
6. 训练模型 — 拟合并调参
7. 评估模型 — RMSE、MAE、R²
8. 预测新数据 — 应用模型

下一步可以尝试：特征工程、超参数调优 (GridSearchCV)、模型集成 (Voting/Stacking)、深度学习、部署上线 (Flask/FastAPI)。

## 代码

讲解对应的示例代码见 `5_linear_regression.py`。
