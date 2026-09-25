"""
TensorFlow 框架示例
=================

TensorFlow 是 Google 开发的深度学习框架, 本文件所有代码真实运行。

数据集使用 sklearn 自带的 digits (8x8 手写数字, 离线可用, 1797 条),
避免首次运行时下载 MNIST; 切换到 MNIST 的方法见文末第 9 节。
"""

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # 屏蔽 TF 冗余日志

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print("=" * 60)
print(f"1. 环境: TensorFlow {tf.__version__} (Keras {keras.__version__})")
print("=" * 60)

a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
print(f"a =\n{a.numpy()}")
print(f"a + b =\n{tf.add(a, b).numpy()}")
print(f"a @ b =\n{tf.matmul(a, b).numpy()}")

print()
print("=" * 60)
print("2. 自动求导 (GradientTape)")
print("=" * 60)

x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2                      # y = x², 导数 2x
print(f"y = x², x = {x.numpy()}")
print(f"dy/dx = {tape.gradient(y, x).numpy()}  (理论值 2x = 6.0)")

print()
print("=" * 60)
print("3. 加载数据 (sklearn digits, 离线)")
print("=" * 60)

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()
X = digits.data.astype("float32") / 16.0     # 像素 0-16 归一化到 0-1
y = digits.target

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"数据形状: {X.shape}  (1797 张 8x8 图片, 摊平成 64 维)")
print(f"类别: 0-9 共 10 类 | 训练集 {x_train.shape[0]} / 测试集 {x_test.shape[0]}")

print()
print("=" * 60)
print("4. Keras Sequential 构建模型")
print("=" * 60)

model = keras.Sequential([
    keras.Input(shape=(64,)),          # Keras 3 推荐用 Input 层声明输入
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
model.summary()

print()
print("=" * 60)
print("5. 编译与训练")
print("=" * 60)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=0,
)

for epoch, (loss, acc, val_acc) in enumerate(
    zip(history.history["loss"], history.history["accuracy"], history.history["val_accuracy"]), 1
):
    print(f"  epoch {epoch:2d}: loss={loss:.4f}, acc={acc:.2%}, val_acc={val_acc:.2%}")

print()
print("=" * 60)
print("6. 评估与预测")
print("=" * 60)

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"测试集准确率: {test_acc:.2%}")

preds = model.predict(x_test[:5], verbose=0)
print(f"前5张图预测: {np.argmax(preds, axis=1).tolist()}")
print(f"前5张图真实: {y_test[:5].tolist()}")

print()
print("=" * 60)
print("7. 函数式 API (等价写法, 更灵活)")
print("=" * 60)

inputs = keras.Input(shape=(64,))
h = layers.Dense(64, activation="relu")(inputs)
outputs = layers.Dense(10, activation="softmax")(h)
model2 = keras.Model(inputs=inputs, outputs=outputs)
print(f"函数式模型参数量: {model2.count_params():,}")
print(f"Sequential 模型参数量: {model.count_params():,}")
print("函数式 API 支持多输入/多输出和分支结构, 复杂模型更常用")

print()
print("=" * 60)
print("8. 模型保存与加载")
print("=" * 60)

import tempfile

with tempfile.TemporaryDirectory() as tmp_dir:     # 用临时目录, 不留垃圾文件
    path = os.path.join(tmp_dir, "model.keras")
    model.save(path)                               # 保存结构 + 权重
    loaded = keras.models.load_model(path)
    acc = loaded.evaluate(x_test, y_test, verbose=0)[1]
    print(f"保存到: {path}")
    print(f"重新加载后测试集准确率: {acc:.2%} (与保存前一致)")

print()
print("=" * 60)
print("9. 切换到 MNIST")
print("=" * 60)

print("""
只需替换第 3 节的数据加载:

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
    x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

再把模型输入从 (64,) 改成 (784,), 其余代码完全不变。
注意: 首次运行需联网下载约 11MB 数据。

其他常用能力:
  - layers.Conv2D / MaxPooling2D: CNN 图像处理
  - layers.Embedding / LSTM / GRU: 序列与文本处理
  - callbacks.EarlyStopping / ModelCheckpoint: 早停与保存最佳模型
  - model.save 到 .keras 格式 / TFLite 导出用于移动端部署
""")