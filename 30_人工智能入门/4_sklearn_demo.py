"""
Scikit-learn 机器学习示例
========================

以鸢尾花数据集为例，演示传统机器学习的完整流程：
加载数据 → 划分 → 标准化 → 训练 → 评估 → 交叉验证 → 调参 → 保存模型。
"""

print("=" * 60)
print("1. Scikit-learn 简介")
print("=" * 60)

print("""
Scikit-learn (sklearn)
  • 简单高效的机器学习工具
  • 涵盖主流机器学习算法
  • 统一的 API: fit / predict / score
""")

print()
print("=" * 60)
print("2. 加载数据集 (鸢尾花)")
print("=" * 60)

from sklearn.datasets import load_iris

iris = load_iris()
X, y = iris.data, iris.target

print(f"数据形状: {X.shape}  (150条样本, 4个特征)")
print(f"类别: {[str(name) for name in iris.target_names]}")
print(f"特征: {list(iris.feature_names)}")
print(f"前3条数据:\n{X[:3]}")

print()
print("=" * 60)
print("3. 划分训练集和测试集")
print("=" * 60)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"训练集: {X_train.shape[0]} 条")
print(f"测试集: {X_test.shape[0]} 条")

print()
print("=" * 60)
print("4. 数据标准化")
print("=" * 60)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 训练集: fit + transform
X_test_scaled = scaler.transform(X_test)        # 测试集: 只 transform (防止信息泄露)

print(f"标准化前 (花萼长度) 均值: {X_train[:, 0].mean():.2f}")
print(f"标准化后 (花萼长度) 均值: {X_train_scaled[:, 0].mean():.2f}")

print()
print("=" * 60)
print("5. 多算法对比训练")
print("=" * 60)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

models = {
    "逻辑回归": LogisticRegression(max_iter=1000),
    "K近邻 (k=3)": KNeighborsClassifier(n_neighbors=3),
    "决策树": DecisionTreeClassifier(random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=42),
    "支持向量机": SVC(kernel="rbf"),
}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)          # 训练
    acc = model.score(X_test_scaled, y_test)    # 评估 (返回准确率)
    print(f"{name}: 准确率 {acc:.2%}")

print()
print("=" * 60)
print("6. 评估指标 (以随机森林为例)")
print("=" * 60)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

print(f"准确率: {accuracy_score(y_test, y_pred):.2%}")
print(f"\n混淆矩阵 (行=真实, 列=预测):\n{confusion_matrix(y_test, y_pred)}")
print(f"\n分类报告:\n{classification_report(y_test, y_pred, target_names=iris.target_names, zero_division=0)}")

print()
print("=" * 60)
print("7. 交叉验证")
print("=" * 60)

from sklearn.model_selection import cross_val_score

# 5折交叉验证: 数据分5份, 轮流做测试集 (树模型不需要标准化, 直接用原始 X)
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(f"各折准确率: {scores}")
print(f"平均准确率: {scores.mean():.2%} (+/- {scores.std():.4f})")

print()
print("=" * 60)
print("8. 超参数调优 (网格搜索)")
print("=" * 60)

from sklearn.model_selection import GridSearchCV

param_grid = {
    "n_estimators": [10, 50, 100],
    "max_depth": [None, 3, 5],
}
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring="accuracy",
)
grid_search.fit(X_train_scaled, y_train)

print(f"测试的参数组合数: {len(grid_search.cv_results_['params'])}")
print(f"最佳参数: {grid_search.best_params_}")
print(f"交叉验证最佳分数: {grid_search.best_score_:.2%}")
print(f"最佳模型在测试集上: {grid_search.best_estimator_.score(X_test_scaled, y_test):.2%}")

print()
print("=" * 60)
print("9. 保存和加载模型")
print("=" * 60)

import os
import tempfile

import joblib

with tempfile.TemporaryDirectory() as tmp_dir:  # 用临时目录, 不留垃圾文件
    model_path = os.path.join(tmp_dir, "model.pkl")
    joblib.dump(model, model_path)              # 保存
    loaded_model = joblib.load(model_path)      # 加载
    acc = loaded_model.score(X_test_scaled, y_test)
    print(f"保存到: {model_path}")
    print(f"重新加载后测试集准确率: {acc:.2%} (与保存前一致)")

print()
print("=" * 60)
print("10. 完整流程总结")
print("=" * 60)

print("""
机器学习标准流程:
  1. 加载数据   load_iris()
  2. 划分数据   train_test_split()
  3. 标准化     StandardScaler (训练集 fit_transform, 测试集只 transform)
  4. 训练模型   model.fit(X_train, y_train)
  5. 预测评估   model.predict / model.score / accuracy_score
  6. 交叉验证   cross_val_score
  7. 超参调优   GridSearchCV
  8. 保存部署   joblib.dump
""")
