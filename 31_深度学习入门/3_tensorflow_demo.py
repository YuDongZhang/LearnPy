"""
TensorFlow 框架示例
=================

TensorFlow 是 Google 开发的深度学习框架。
由于环境中未安装 TensorFlow，以下为示例代码展示。
"""

print("=" * 60)
print("1. TensorFlow 简介")
print("=" * 60)

print("""
TensorFlow 特点:
  • 2015年 Google 发布
  • 静态计算图 (TensorFlow 1.x)
  • 动态计算图 (TensorFlow 2.x + Eager Execution)
  • Keras 官方高层 API
  • TensorBoard 可视化
  • 生态完善, 生产部署方便

安装:
  pip install tensorflow

验证:
  import tensorflow as tf
  print(tf.__version__)
""")

print()
print("=" * 60)
print("2. TensorFlow 2.x 基础")
print("=" * 60)

print('''
import tensorflow as tf

# 开启 Eager Execution (默认开启)
tf.config.run_functions_eagerly(True)

# 基础操作
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])

c = tf.add(a, b)      # 加法
d = tf.matmul(a, b)   # 矩阵乘法

print(a)
print(c)
''')

print()
print("=" * 60)
print("3. 使用 Keras 构建模型")
print("=" * 60)

print('''
from tensorflow import keras
from tensorflow.keras import layers

# 方法1: Sequential 顺序模型
model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# 方法2: 函数式 API (更灵活)
inputs = keras.Input(shape=(784,))
x = layers.Dense(128, activation='relu')(inputs)
x = layers.Dropout(0.2)(x)
x = layers.Dense(64, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=inputs, outputs=outputs)

# 查看模型结构
model.summary()
''')

print()
print("=" * 60)
print("4. 编译和训练模型")
print("=" * 60)

print('''
# 编译模型
model.compile(
    optimizer='adam',                    # 优化器
    loss='sparse_categorical_crossentropy',  # 损失函数
    metrics=['accuracy']                 # 评估指标
)

# 训练模型
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

# 评估模型
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"测试准确率: {test_acc:.2%}")
''')

print()
print("=" * 60)
print("5. 自定义训练循环")
print("=" * 60)

print('''
# 自定义训练循环
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

# 训练循环
for epoch in range(epochs):
    for batch in dataset:
        loss = train_step(batch_x, batch_y)
    print(f"Epoch {epoch}: Loss = {loss.numpy():.4f}")
''')

print()
print("=" * 60)
print("6. CNN 卷积神经网络")
print("=" * 60)

print('''
# CNN 模型 (图像分类)
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

# 编译
cnn_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 训练
cnn_model.fit(train_images, train_labels, epochs=5)
''')

print()
print("=" * 60)
print("7. RNN 循环神经网络")
print("=" * 60)

print('''
# RNN 模型 (序列数据)
rnn_model = keras.Sequential([
    layers.Embedding(10000, 64, input_length=100),
    layers.LSTM(64, return_sequences=True),
    layers.LSTM(32),
    layers.Dense(1, activation='sigmoid')
])

# 或者使用 GRU
gru_model = keras.Sequential([
    layers.Embedding(10000, 64),
    layers.GRU(64),
    layers.Dense(1, activation='sigmoid')
])
''')

print()
print("=" * 60)
print("8. 数据增强")
print("=" * 60)

print('''
# 数据增强 (Image Data Generator)
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# 应用到数据
augmented_train = train_images.map(lambda x: (data_augmentation(x), y))
''')

print()
print("=" * 60)
print("9. 迁移学习")
print("=" * 60)

print('''
# 迁移学习 - 使用预训练模型
base_model = keras.applications.VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# 冻结 base model
base_model.trainable = False

# 添加分类头
model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# 解冻后微调
base_model.trainable = True
model.compile(optimizer=keras.optimizers.Adam(1e-5), loss='categorical_crossentropy')
model.fit(train_dataset, epochs=5)
''')

print()
print("=" * 60)
print("10. 模型保存和加载")
print("=" * 60)

print('''
# 保存整个模型 (包含结构 + 权重 + 优化器)
model.save('my_model.keras')
loaded_model = keras.models.load_model('my_model.keras')

# 只保存权重
model.save_weights('weights.weights.h5')
model.load_weights('weights.weights.h5')

# SavedModel 格式 (TensorFlow 特有)
model.save('saved_model/')

# 导出为 TFLite (移动端部署)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
''')

print()
print("=" * 60)
print("11. 回调函数")
print("=" * 60)

print('''
from tensorflow.keras import callbacks

# 常用回调函数
cb = [
    # 早停
    callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),

    # 学习率调度
    callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3
    ),

    # 模型检查点
    callbacks.ModelCheckpoint(
        'best_model.keras',
        monitor='val_accuracy',
        save_best_only=True
    ),

    # TensorBoard
    callbacks.TensorBoard(
        log_dir='./logs'
    ),

    # 自定义回调
    callbacks.LambdaCallback(
        on_epoch_end=lambda epoch, logs: print(f"Epoch {epoch}")
    )
]

model.fit(x, y, callbacks=cb)
''')

print()
print("=" * 60)
print("12. 完整示例: MNIST 分类")
print("=" * 60)

print('''
import tensorflow as tf
from tensorflow.keras import layers

# 1. 加载数据
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 2. 数据预处理
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

# 4. 编译
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 5. 训练
model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# 6. 评估
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"测试准确率: {test_acc:.2%}")

# 7. 预测
predictions = model.predict(x_test[:5])
print(f"预测结果: {tf.argmax(predictions, axis=1).numpy()}")
''')
