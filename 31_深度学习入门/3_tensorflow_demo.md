# 3. TensorFlow框架示例

## TensorFlow简介

TensorFlow 是 Google 2015 年发布的深度学习框架：

- 静态计算图 (1.x) → 动态计算图 (2.x + Eager Execution)
- Keras 官方高层 API
- TensorBoard 可视化
- 生态完善，生产部署方便

```bash
pip install tensorflow
```

## 基础操作

```python
import tensorflow as tf

a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])

c = tf.add(a, b)      # 加法
d = tf.matmul(a, b)   # 矩阵乘法
```

## Keras构建模型

方法1：Sequential 顺序模型（简单场景）：

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

方法2：函数式 API（更灵活，支持多输入输出）：

```python
inputs = keras.Input(shape=(784,))
x = layers.Dense(128, activation='relu')(inputs)
x = layers.Dropout(0.2)(x)
x = layers.Dense(64, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.summary()  # 查看模型结构
```

## 编译和训练

```python
model.compile(
    optimizer='adam',                          # 优化器
    loss='sparse_categorical_crossentropy',    # 损失函数
    metrics=['accuracy']                       # 评估指标
)

history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=3),
        keras.callbacks.ModelCheckpoint('model.h5')
    ]
)

test_loss, test_acc = model.evaluate(x_test, y_test)
```

Keras 一行 fit 抵得上 PyTorch 的整个训练循环，非常适合快速原型。

## 自定义训练循环

需要更细粒度控制时，用 GradientTape：

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

## CNN示例

```python
cnn_model = keras.Sequential([
    # 卷积层
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # 全连接层
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

## RNN示例

```python
rnn_model = keras.Sequential([
    layers.Embedding(10000, 64, input_length=100),
    layers.LSTM(64, return_sequences=True),
    layers.LSTM(32),
    layers.Dense(1, activation='sigmoid')
])
```

## 数据增强

```python
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])
```

## 迁移学习

```python
base_model = keras.applications.VGG16(
    weights='imagenet', include_top=False, input_shape=(224, 224, 3)
)
base_model.trainable = False   # 冻结预训练层

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# 解冻后用小学习率微调
base_model.trainable = True
model.compile(optimizer=keras.optimizers.Adam(1e-5), loss='categorical_crossentropy')
```

## 模型保存和加载

```python
model.save('my_model.keras')            # 整个模型
model.save_weights('weights.h5')        # 只保存权重
model.save('saved_model/')              # SavedModel 格式

# 导出 TFLite (移动端部署)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
```

## 回调函数

```python
cb = [
    callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3),
    callbacks.ModelCheckpoint('best_model.keras', save_best_only=True),
    callbacks.TensorBoard(log_dir='./logs'),
]
model.fit(x, y, callbacks=cb)
```

## 完整示例：MNIST分类

```python
import tensorflow as tf
from tensorflow.keras import layers

# 1. 加载数据
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 2. 预处理
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# 3. 构建模型
model = tf.keras.Sequential([
    layers.Dense(512, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

# 4. 编译训练
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# 5. 评估
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"测试准确率: {test_acc:.2%}")
```

## 代码

讲解对应的示例代码见 `3_tensorflow_demo.py`。
