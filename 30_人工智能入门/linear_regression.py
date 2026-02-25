"""
线性回归实战：预测房价
=====================

使用线性回归模型预测房价，综合运用数据处理和模型训练。
由于环境中未安装 sklearn，以下为示例代码展示。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("""
项目: 房价预测
目标: 根据房屋特征预测房价

数据特征:
  • 房间数量 (RM)
  • 犯罪率 (CRIM)
  • 房屋年龄 (AGE)
  • 距离就业中心距离 (DIS)
  • 税率 (TAX)
  
使用数据集: 波士顿房价数据集
""")

print()
print("=" * 60)
print("2. 安装必要库")
print("=" * 60)

print("""
pip install scikit-learn pandas numpy matplotlib seaborn
""")

print()
print("=" * 60)
print("3. 加载数据")
print("=" * 60)

print("""
from sklearn.datasets import load_boston
import pandas as pd
import numpy as np

# 加载数据集
boston = load_boston()
X, y = boston.data, boston.target

# 转换为 DataFrame
df = pd.DataFrame(X, columns=boston.feature_names)
df['PRICE'] = y

print(f"数据集形状: {X.shape}")
print(f"特征: {list(boston.feature_names)}")
""")

print()
print("=" * 60)
print("4. 数据探索")
print("=" * 60)

print("""
# 基本统计
print(df.describe())

# 缺失值检查
print(df.isnull().sum())

# 相关性分析
print(df.corr()['PRICE'].sort_values(ascending=False))
""")

print()
print("=" * 60)
print("5. 数据预处理")
print("=" * 60)

print("""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 特征和目标
X = df.drop('PRICE', axis=1)
y = df['PRICE']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 特征标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"训练集: {X_train.shape[0]} 样本")
print(f"测试集: {X_test.shape[0]} 样本")
""")

print()
print("=" * 60)
print("6. 训练多个模型")
print("=" * 60)

print("""
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 定义模型
models = {
    '线性回归': LinearRegression(),
    '岭回归': Ridge(alpha=1.0),
    'Lasso回归': Lasso(alpha=0.1),
    '随机森林': RandomForestRegressor(n_estimators=100, random_state=42)
}

# 训练并评估
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
""")

print()
print("=" * 60)
print("7. 模型评估对比")
print("=" * 60)

print("""
import pandas as pd

# 转为 DataFrame 方便对比
results_df = pd.DataFrame(results).T
results_df = results_df.sort_values('R²', ascending=False)

print("模型性能排名:")
print(results_df)

# 找出最佳模型
best_model_name = results_df['R²'].idxmax()
print(f"\\n最佳模型: {best_model_name}")
""")

print()
print("=" * 60)
print("8. 预测新数据")
print("=" * 60)

print("""
# 使用最佳模型预测
best_model = models[best_model_name]

# 新房数据
new_house = pd.DataFrame({
    'RM': [5],      # 5个房间
    'CRIM': [0.1],  # 低犯罪率
    'AGE': [30],    # 30年房龄
    'DIS': [4],     # 距离就业中心4km
    'TAX': [300]    # 税率
})

# 标准化并预测
new_house_scaled = scaler.transform(new_house)
predicted_price = best_model.predict(new_house_scaled)[0]

print(f"新房特征: {new_house.to_dict(records=True)}")
print(f"预测房价: ${predicted_price * 1000:.2f}")
""")

print()
print("=" * 60)
print("9. 模型解释")
print("=" * 60)

print('''
# 线性回归系数 (特征重要性)
lr_model = models['线性回归']
importance = pd.DataFrame({
    '特征': X.columns,
    '系数': lr_model.coef_
}).sort_values('系数', key=abs, ascending=False)

print("特征重要性 (按系数绝对值排序):")
print(importance.to_string(index=False))

print("""
解读:
  • 系数 > 0: 该特征增加，房价增加
  • 系数 < 0: 该特征增加，房价降低
  • |系数| 越大，影响越大
""")
''')

print()
print("=" * 60)
print("10. 项目总结")
print("=" * 60)

print("""
完整的机器学习项目流程:
  ✓ 1. 定义问题 - 预测房价
  ✓ 2. 收集数据 - 加载数据集
  ✓ 3. 数据探索 - 统计分析
  ✓ 4. 数据预处理 - 划分数据集、标准化
  ✓ 5. 选择模型 - 线性回归、岭回归、随机森林
  ✓ 6. 训练模型 - 拟合并调参
  ✓ 7. 评估模型 - RMSE、MAE、R²
  ✓ 8. 预测新数据 - 应用模型

下一步可以尝试:
  • 特征工程 - 创建新特征 (如房间数*房龄)
  • 超参数调优 - 使用 GridSearchCV
  • 模型集成 - 多个模型组合 (Voting, Stacking)
  • 深度学习 - 使用 TensorFlow/PyTorch
  • 部署上线 - 使用 Flask/FastAPI 部署模型

推荐学习路径:
  1. 机器学习基础 - Scikit-learn
  2. 深度学习 - TensorFlow 或 PyTorch
  3. 项目实战 - Kaggle 竞赛
  4. 部署上线 - 模型服务化
""")
