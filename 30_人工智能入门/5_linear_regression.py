"""
线性回归实战：预测房价
=====================

使用真实的加州房价数据集，综合运用数据处理和模型训练。

注: 老教材常用的 load_boston 已在 sklearn 1.2 中移除 (伦理争议),
官方推荐 fetch_california_housing 作为替代数据集。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("""
项目: 房价预测 (回归问题)
目标: 根据房屋特征预测社区房价中位数

使用数据集: 加州房价 (California Housing)
  • 20640 个社区样本, 8 个特征
  • 目标值单位: 10万美元
  • 首次运行会自动下载数据 (~400KB), 之后使用本地缓存
""")

print()
print("=" * 60)
print("2. 加载数据")
print("=" * 60)

from sklearn.datasets import fetch_california_housing
import numpy as np
import pandas as pd

housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target, name="PRICE")  # 单位: 10万美元

print(f"数据集形状: {X.shape}")
print(f"特征: {list(X.columns)}")

print()
print("=" * 60)
print("3. 数据探索")
print("=" * 60)

print("基本统计 (前5个特征):")
print(X.describe().T[["mean", "std", "min", "max"]].head().to_string())

n_missing = X.isnull().sum().sum() + y.isnull().sum()
print(f"\n缺失值总数: {n_missing}")

df = X.copy()
df["PRICE"] = y
print("\n与房价的相关性 (降序):")
print(df.corr()["PRICE"].sort_values(ascending=False).to_string())

print("""
解读: MedInc (社区收入中位数) 与房价相关性最高 (~0.69),
符合直觉 —— 收入高的社区房价也更贵。
""")

print()
print("=" * 60)
print("4. 数据预处理")
print("=" * 60)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 训练集: fit + transform
X_test_scaled = scaler.transform(X_test)        # 测试集: 只 transform (防止信息泄露)

print(f"训练集: {X_train.shape[0]} 样本")
print(f"测试集: {X_test.shape[0]} 样本")

print()
print("=" * 60)
print("5. 训练多个模型")
print("=" * 60)

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

models = {
    "线性回归": LinearRegression(),
    "岭回归": Ridge(alpha=1.0),
    "Lasso回归": Lasso(alpha=0.1),
    "随机森林": RandomForestRegressor(n_estimators=100, random_state=42),
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results[name] = {"RMSE": rmse, "MAE": mae, "R²": r2}
    print(f"{name}: RMSE={rmse:.3f}, MAE={mae:.3f}, R²={r2:.4f}")

print("""
指标解读 (房价单位: 10万美元):
  • RMSE/MAE 越小越好 —— 预测误差
  • R² 越接近 1 越好 —— 模型解释力
""")

print()
print("=" * 60)
print("6. 模型评估对比")
print("=" * 60)

results_df = pd.DataFrame(results).T.sort_values("R²", ascending=False)
print("模型性能排名:")
print(results_df.to_string())

best_model_name = results_df["R²"].idxmax()
best_model = models[best_model_name]
print(f"\n最佳模型: {best_model_name}")

print()
print("=" * 60)
print("7. 预测新数据")
print("=" * 60)

# 构造一套"典型房子": 用训练集的中位数作为基准, 再调高社区收入
new_house = X_train.median().to_frame().T
new_house["MedInc"] = 6.0  # 收入中位数 6 万美元 (高于整体中位数)

new_house_scaled = scaler.transform(new_house)
predicted_price = best_model.predict(new_house_scaled)[0]

print(f"新房特征: {new_house.round(3).to_dict('records')[0]}")
print(f"预测房价: ${predicted_price * 100000:,.0f}")

# 对比: 低收入社区
new_house_low = new_house.copy()
new_house_low["MedInc"] = 2.0
pred_low = best_model.predict(scaler.transform(new_house_low))[0]
print(f"若社区收入只有 2 万美元: ${pred_low * 100000:,.0f}")

print()
print("=" * 60)
print("8. 模型解释 (特征重要性)")
print("=" * 60)

# 线性回归系数: 特征已标准化, 系数绝对值可直接比较影响力
lr_model = models["线性回归"]
importance = pd.DataFrame({
    "特征": X.columns,
    "系数": lr_model.coef_,
}).sort_values("系数", key=abs, ascending=False)

print("线性回归系数 (按绝对值排序):")
print(importance.to_string(index=False))

# 随机森林的特征重要性
rf_model = models["随机森林"]
rf_importance = pd.Series(
    rf_model.feature_importances_, index=X.columns
).sort_values(ascending=False)
print("\n随机森林特征重要性 (前5):")
print(rf_importance.head().to_string())

print("""
解读:
  • 系数 > 0: 该特征增加, 房价增加
  • 系数 < 0: 该特征增加, 房价降低
  • |系数| 越大, 影响越大
  • 两种方法都指向 MedInc (社区收入) 是最重要特征
""")

print()
print("=" * 60)
print("9. 项目总结")
print("=" * 60)

print("""
完整的机器学习项目流程:
  ✓ 1. 定义问题 - 预测房价
  ✓ 2. 收集数据 - 加载加州房价数据集
  ✓ 3. 数据探索 - 统计分析、相关性
  ✓ 4. 数据预处理 - 划分数据集、标准化
  ✓ 5. 选择模型 - 线性回归、岭回归、随机森林
  ✓ 6. 训练模型 - 拟合多个候选模型
  ✓ 7. 评估模型 - RMSE、MAE、R²
  ✓ 8. 预测新数据 - 应用最佳模型
  ✓ 9. 模型解释 - 特征重要性分析

下一步可以尝试:
  • 特征工程 - 创建新特征 (如房间数*房龄)
  • 超参数调优 - 使用 GridSearchCV
  • 模型集成 - 多个模型组合 (Voting, Stacking)
  • 深度学习 - 使用 TensorFlow/PyTorch
  • 部署上线 - 使用 Flask/FastAPI 部署模型
""")
