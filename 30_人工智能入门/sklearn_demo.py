"""
Scikit-learn 机器学习示例
========================

Scikit-learn 是 Python 中最流行的传统机器学习库。
由于环境中未安装 sklearn，以下为示例代码展示。
"""

print("=" * 60)
print("1. Scikit-learn 简介")
print("=" * 60)

print("""
Scikit-learn (sklearn)
  • 简单高效的机器学习工具
  • 涵盖主流机器学习算法
  • 统一的 API 设计
  
主要模块:
  • datasets    - 数据集
  • linear_model - 线性模型
  • tree       - 决策树
  • ensemble   - 集成学习
  • svm        - 支持向量机
  • neural_network - 神经网络
  • metrics    - 评估指标
  • model_selection - 模型选择
""")

print()
print("=" * 60)
print("2. 安装 sklearn")
print("=" * 60)

print("""
pip install scikit-learn
""")

print()
print("=" * 60)
print("3. 常用数据集")
print("=" * 60)

print("""
from sklearn import datasets

# 鸢尾花数据集 (分类)
iris = datasets.load_iris()

# 手写数字数据集 (分类)
digits = datasets.load_digits()

# 糖尿病数据集 (回归)
diabetes = datasets.load_diabetes()

# 乳腺癌数据集 (分类)
breast_cancer = datasets.load_breast_cancer()

# 生成模拟数据
X, y = datasets.make_classification(n_samples=100)
""")

print()
print("=" * 60)
print("4. 数据划分")
print("=" * 60)

print("""
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,    # 测试集比例
    random_state=42    # 随机种子
)
""")

print()
print("=" * 60)
print("5. 数据预处理")
print("=" * 60)

print("""
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 标准化 (均值为0，标准差为1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 归一化 (0-1区间)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
""")

print()
print("=" * 60)
print("6. 常用算法示例")
print("=" * 60)

print("""
# 线性回归 (回归)
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 逻辑回归 (分类)
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# K近邻 (分类/回归)
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=3)

# 决策树 (分类/回归)
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()

# 随机森林 (集成学习)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)

# 支持向量机
from sklearn.svm import SVC
model = SVC(kernel='rbf')
""")

print()
print("=" * 60)
print("7. 模型训练和预测")
print("=" * 60)

print("""
# 训练模型
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 预测概率 (分类)
y_proba = model.predict_proba(X_test)

# 评估模型
accuracy = model.score(X_test, y_test)
""")

print()
print("=" * 60)
print("8. 评估指标")
print("=" * 60)

print("""
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_squared_error,
    r2_score
)

# 分类指标
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# 混淆矩阵
cm = confusion_matrix(y_test, y_pred)

# 回归指标
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
""")

print()
print("=" * 60)
print("9. 交叉验证")
print("=" * 60)

print("""
from sklearn.model_selection import cross_val_score

# 5折交叉验证
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"各折准确率: {scores}")
print(f"平均准确率: {scores.mean():.2%}")
print(f"标准差: {scores.std():.4f}")
""")

print()
print("=" * 60)
print("10. 超参数调优")
print("=" * 60)

print("""
from sklearn.model_selection import GridSearchCV

# 定义参数网格
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'learning_rate': [0.01, 0.1, 0.2]
}

# 网格搜索
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid=param_grid,
    cv=5,
    scoring='accuracy'
)

grid_search.fit(X_train, y_train)

print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳分数: {grid_search.best_score_:.2%}")

# 使用最佳模型
best_model = grid_search.best_estimator_
""")

print()
print("=" * 60)
print("11. 保存和加载模型")
print("=" * 60)

print("""
import joblib

# 保存模型
joblib.dump(model, 'model.pkl')

# 加载模型
loaded_model = joblib.load('model.pkl')

# 使用
y_pred = loaded_model.predict(X_test)
""")

print()
print("=" * 60)
print("12. 完整示例流程")
print("=" * 60)

print("""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 2. 划分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 训练模型
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train_scaled, y_train)

# 5. 预测
y_pred = model.predict(X_test_scaled)

# 6. 评估
accuracy = accuracy_score(y_test, y_pred)
print(f'准确率: {accuracy:.2%}')
print(classification_report(y_test, y_pred))
""")
