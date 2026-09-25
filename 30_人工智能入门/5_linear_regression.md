# 5. 线性回归实战：预测房价

## 项目概述

项目目标：根据房屋特征预测社区房价中位数。

使用数据集：加州房价 (California Housing)：

- 20640 个社区样本，8 个特征
- 特征包括：收入中位数 (MedInc)、房龄 (HouseAge)、平均房间数 (AveRooms)、经纬度等
- 目标值单位：10万美元

> 注：老教材常用的 `load_boston`（波士顿房价）已在 sklearn 1.2 中移除（伦理争议），官方推荐 `fetch_california_housing` 作为替代。首次运行会自动下载数据（约400KB），之后使用本地缓存。

这是机器学习的经典回归问题，综合运用数据处理和模型训练。

## 加载数据

```python
from sklearn.datasets import fetch_california_housing
import numpy as np
import pandas as pd

housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target, name='PRICE')  # 单位: 10万美元
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
# 构造一套"典型房子": 用训练集中位数作为基准, 再调高社区收入
new_house = X_train.median().to_frame().T
new_house['MedInc'] = 6.0  # 收入中位数 6 万美元 (高于整体中位数)

new_house_scaled = scaler.transform(new_house)
predicted_price = best_model.predict(new_house_scaled)[0]
print(f"预测房价: ${predicted_price * 100000:,.0f}")
```

还可以做对比实验：把 MedInc 调低到 2.0，预测房价明显下降，验证了收入是决定房价的关键因素。

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

实际运行中，MedInc（社区收入）在回归系数和随机森林重要性中都是第一关键特征；纬度/经度系数为负，说明加州北部房价相对较低。

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
