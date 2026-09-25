# 3. TensorFlow 框架示例

> 上一篇（`2_neural_network.md`）我们用 numpy 手写了前向传播、反向传播和参数更新。
> 这一篇要回答：**框架到底替我们做了什么？为什么能少写那么多代码？**
>
> 阅读方法：每看到框架的一行 API，都回到 numpy 版问一句"它在替我写哪几行"。文中的输出都是 `3_tensorflow_demo.py` 的真实运行结果。

---

## 1. TensorFlow 是什么，为什么现在能像写普通 Python 一样用

TensorFlow 是 Google 2015 年开源的深度学习框架。理解它的关键是**两代设计的差别**：

| | TensorFlow 1.x | TensorFlow 2.x（现在用的） |
|---|---|---|
| 计算方式 | **静态图**：先"画好"整张计算图，再一次性执行 | **动态图**（Eager Execution）：写一行执行一行 |
| 调试 | 只能看到图，不能断点、不能 print 中间结果 | 和普通 Python 一样，随时 print、随时调试 |
| 感受 | 像在写配置文件 | 像在写 numpy |

1.x 的静态图之所以被淘汰，是因为**它没法调试**：你写的是"图的定义"，而不是"执行过程"，中间任何一步都看不见。2.x 引入 Eager 之后，`tf.constant([[1,2],[3,4]])` 会**立刻**变成一个真实的张量，能直接 `.numpy()` 打印出来看。

代价是失去了一部分性能优化空间，所以 2.x 提供了 `@tf.function`：**把 Python 函数编译成图**，既能调试又能加速——第 9 节会看到。

```bash
pip install tensorflow
```

运行环境：本文与代码验证于 **TensorFlow 2.20.0 + Keras 3.10.0**。

---

## 2. 张量与基础运算：手算一遍

**张量（Tensor）就是多维数组**，`tf.Tensor` 之于 TensorFlow，相当于 `np.ndarray` 之于 numpy。名字里的 "Tensor" 其实就来自这里。

维度对应的叫法：

| 维度 | 叫法 | 例子 |
|---|---|---|
| 0 维 | 标量 scalar | `3.14`（一个损失值） |
| 1 维 | 向量 vector | `[1, 2, 3]`（一个样本的特征） |
| 2 维 | 矩阵 matrix | `(32, 64)`（一个 batch 的样本） |
| 3 维 | 张量 | `(32, 28, 28)`（一批灰度图） |
| 4 维 | 张量 | `(32, 3, 224, 224)`（一批彩色图：批, 通道, 高, 宽） |

代码第 1 节：

```python
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
print(f"a + b =\n{tf.add(a, b).numpy()}")
print(f"a @ b =\n{tf.matmul(a, b).numpy()}")
```

真实输出：

```
a + b =
[[ 6  8]
 [10 12]]
a @ b =
[[19 22]
 [43 50]]
```

**两种运算的区别必须分清**：

`a + b` 是**逐元素相加**（element-wise），对应位置的数直接相加：

```
[[1+5, 2+6], [3+7, 4+8]] = [[6, 8], [10, 12]]
```

`a @ b` 是**矩阵乘法**，行乘列再求和：

```
(a@b)[0][0] = 1×5 + 2×7 = 19      ← a 的第 1 行 · b 的第 1 列
(a@b)[0][1] = 1×6 + 2×8 = 22      ← a 的第 1 行 · b 的第 2 列
(a@b)[1][0] = 3×5 + 4×7 = 43      ← a 的第 2 行 · b 的第 1 列
(a@b)[1][1] = 3×6 + 4×8 = 50      ← a 的第 2 行 · b 的第 2 列
```

**为什么矩阵乘法这么重要？** 回到上一篇第 5 节的全连接层：`z = X @ W + b`。`(200, 64) @ (64, 128) = (200, 128)` 这个式子，一次算完了 200 个样本 × 128 个神经元的全部加权求和。**神经网络的计算本质上几乎全是矩阵乘法**——这就是它适合用 GPU 的原因（GPU 擅长并行的乘加运算）。

**`tf.constant` vs `tf.Variable`**：`constant` 不可改，`Variable` 可改。**只有 `Variable` 能被自动微分求导并更新**——模型的权重全是 `Variable`，输入数据是 `constant`。

---

## 3. 自动微分 GradientTape：框架的核心价值

这是**整个框架最值钱的部分**。上一篇第 7 节我们手推了反向传播，TF 把它自动化了。

代码第 2 节：

```python
x = tf.Variable(3.0)
with tf.GradientTape() as tape:      # 开始"录像"
    y = x ** 2                       # y = x², 导数 2x
print(f"dy/dx = {tape.gradient(y, x).numpy()}  (理论值 2x = 6.0)")
```

真实输出：`dy/dx = 6.0  (理论值 2x = 6.0)` ✓

### 3.1 "Tape"（磁带）这个比喻

`GradientTape` 字面意思是"梯度磁带"，非常形象：**它在 `with` 块内把每一步运算按顺序"录"下来，包括运算类型和中间结果**，然后倒带播放，用链式法则逐段算出导数。

```
with tf.GradientTape() as tape:
    y = x ** 2
         │
         └─► 磁带记录: "操作 = 幂运算, 指数 = 2, 输入 = x"

tape.gradient(y, x)   ← 倒带，套用幂函数求导公式 d(x²)/dx = 2x，代入 x=3 → 6.0
```

**为什么必须"录"？** 因为导数公式需要知道"是怎么算出来的"。如果只给一个结果 `y=9`，谁也不知道它是 `3²` 还是 `3+6`，导数自然无从谈起。这也是为什么 `tape.gradient()` 必须在 `with` 块**之外**、且只能调用**一次**——录完才能倒带，倒带一次磁带就消耗掉了。

### 3.2 它和上一篇手推的关系

| 上一篇（手推） | 这一篇（框架） |
|---|---|
| 手写链式法则 `∂L/∂z = ∂L/∂a · ∂a/∂z` | `tape.gradient(loss, params)` |
| 手写 `dz2 = a2 - y` | 框架自动识别出 Sigmoid+交叉熵并化简 |
| 手写 `dW1 = X.T @ dz1` | 框架自动处理转置和 batch 维度 |
| 手写 `W -= lr * dW` | `optimizer.apply_gradients()` |

**框架的价值在于**：链式法则的推导是机械的、容易出错的（尤其在 CNN/Transformer 这种复杂结构里），交给框架做既准确又通用。但**你仍然需要懂原理**——否则 loss 不下降时，你完全不知道从哪里查。

一句话：**框架负责"怎么求梯度"，你负责"设计网络结构、选损失、调超参、看结果"**。

---

## 4. 数据准备：为什么像素要除以 16

代码第 3 节用的是 sklearn 自带的 digits 数据集——**8×8 的手写数字灰度图，共 1797 张，离线可用**（避免首次运行下载 11MB 的 MNIST）。

```python
digits = load_digits()
X = digits.data.astype("float32") / 16.0     # 像素 0-16 归一化到 0-1
y = digits.target
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

真实输出：

```
数据形状: (1797, 64)  (1797 张 8x8 图片, 摊平成 64 维)
类别: 0-9 共 10 类 | 训练集 1437 / 测试集 360
```

**为什么除以 16？** digits 的像素值是 0~16 的整数（4 位量化），除以 16 后统一到 **0~1**。

**归一化不是可选的装饰，它直接影响能不能训好**：

- 输入尺度差异大会导致损失曲面被"拉长"，梯度方向偏向数值大的那个特征，模型在另一个方向上几乎不动（想象一个又长又窄的山谷，梯度下降会来回横跳）
- 数值过大还会让激活值进入 Sigmoid/Tanh 的饱和区，导数趋近 0 → 梯度消失（上一篇第 10 节）
- 统一到 0~1（或标准化到均值 0、方差 1）后，各特征被公平对待，收敛快得多

**`train_test_split` 的 `random_state=42` 是什么？** 随机种子。固定它之后，每次运行划分结果完全一样，**实验结果可复现**——这是做实验必须养成的习惯，否则"上次 96%、这次 94%"你都不知道是模型变了还是数据划分变了。

**为什么 64 维？** 8×8=64，把二维图片摊平成一维向量。全连接层只认向量，不认二维结构——**这个"摊平"动作恰好丢掉了一个重要信息：像素之间的空间位置关系**。这正是下一篇 CNN 要解决的核心问题（不摊平，用卷积保留空间结构）。先记住这个伏笔。

---

## 5. 搭建模型：参数量是怎么算出来的

```python
model = keras.Sequential([
    keras.Input(shape=(64,)),          # Keras 3 推荐用 Input 层声明输入
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
```

**Sequential 的含义**：数据像流水线一样依次穿过每一层，前一层输出就是后一层输入。适合简单的单向堆叠。

**逐层理解**：

| 层 | 输入维度 | 输出维度 | 干了什么 |
|---|---|---|---|
| `Input(shape=(64,))` | — | — | 声明输入形状（64 个像素）。Keras 3 必须有，否则第一层无法确定权重形状 |
| `Dense(128, relu)` | 64 | 128 | 全连接：`z = x @ W + b`，`W` 是 (64,128) |
| `Dropout(0.2)` | 128 | 128 | 训练时随机丢弃 20% 神经元，防过拟合（形状不变） |
| `Dense(64, relu)` | 128 | 64 | 再压一层 |
| `Dense(10, softmax)` | 64 | 10 | 输出 10 个类别的概率（0~9） |

**手算参数量**（全连接的公式：`输入数 × 输出数 + 输出数`，加的是偏置）：

```
第 1 层 Dense(64→128): 64 × 128 + 128 = 8192 + 128 = 8,320
第 2 层 Dense(128→64): 128 × 64 + 64  = 8192 + 64  = 8,256
第 3 层 Dense(64→10):  64 × 10 + 10   = 640 + 10   =   650
Dropout:                                            0（没有参数）
────────────────────────────────────────────────────────
合计:                                              17,226
```

对照 `model.summary()` 的真实输出——**完全一致**：

```
│ dense (Dense)      │ (None, 128)  │  8,320  │
│ dropout (Dropout)  │ (None, 128)  │      0  │
│ dense_1 (Dense)    │ (None, 64)   │  8,256  │
│ dense_2 (Dense)    │ (None, 10)   │    650  │
 Total params: 17,226
```

**`(None, 128)` 里的 `None` 是什么？** 是 **batch 维度**，表示"一次可以喂任意数量的样本"。所以同一份模型能处理 1 张图也能处理 1000 张图——这个维度在定义模型时不需要固定。

**为什么 `Dropout` 参数量是 0？** 它只做"随机把某些输出置 0"的操作，没有任何要学的权重。判别方法很简单：**只有 `Dense`、`Conv2D` 这类带权重矩阵的层才有参数**。

**`activation="relu"` 为什么写在 `Dense` 参数里？** 等价于 `Dense(128)` 后面再跟一个 `layers.ReLU()`，只是写法更紧凑。注意**最后一层不要加 ReLU**——输出层要的是概率（softmax），加 ReLU 会把负数砍掉，破坏概率分布。

---

## 6. compile：这三个参数决定了"怎么训"

```python
model.compile(
    optimizer="adam",                          # 优化器
    loss="sparse_categorical_crossentropy",    # 损失函数
    metrics=["accuracy"],                      # 评估指标
)
```

这三个分别对应上一篇的三个概念，只是换了个名字：

| compile 参数 | 对应上一篇 | 作用 |
|---|---|---|
| `optimizer` | 第 8 节 优化器 | 拿到梯度后怎么更新参数（Adam 内部含自适应学习率 + 动量） |
| `loss` | 第 6 节 损失函数 | 把误差变成一个可导的数，**反向传播的起点** |
| `metrics` | — | 只用于**给人看**的评价指标，**不参与梯度计算** |

**`sparse_categorical_crossentropy` 里 "sparse" 是什么意思？** 这是最容易困惑的点，关键在**标签的格式**：

| 标签格式 | 例子（3 分类） | 该用哪个 loss |
|---|---|---|
| **整数索引**（sparse） | `2` | `sparse_categorical_crossentropy` |
| **one-hot 向量** | `[0, 0, 1]` | `categorical_crossentropy` |

我们的 `y` 是 `digits.target`，即 `6, 9, 3, 7, 2...` 这样的整数，所以用 **sparse** 版。如果写成非 sparse 版会直接报形状错误——**这是新手最常见的报错之一**。

**`metrics=["accuracy"]` 为什么不算梯度？** 因为准确率是"预测对的比例"，它**不可导**（要么对要么错，是个阶跃函数），无法提供梯度方向。它只是打印出来给人看的。同理，任何自定义指标都属于这一类。

**`loss` 必须可导**——这是硬性要求，回到上一篇第 6 节的结论。

---

## 7. fit：一行代码背后的整个训练循环

```python
history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=0,
)
```

### 7.1 fit 到底做了什么

`model.fit` 是**整个上一篇第 12 节训练循环的封装**。它内部（简化后）等价于：

```python
for epoch in range(epochs):                       # 数据集过 10 遍
    for x_batch, y_batch in 把数据按 32 切成小批:    # 每批 32 条
        with tf.GradientTape() as tape:           # ① 开始录像
            predictions = model(x_batch)          # ② 前向传播
            loss = loss_fn(y_batch, predictions)  # ③ 计算损失
        gradients = tape.gradient(loss, model.trainable_variables)  # ④ 反向传播
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))  # ⑤ 更新参数
```

**逐项对照**：

| 你的代码 | 它在替你做 |
|---|---|
| `epochs=10` | 外层循环跑 10 遍 |
| `batch_size=32` | 内层循环把数据切成 32 条一批**（为什么分批见下）** |
| `validation_split=0.2` | 从训练集里**再切出 20% 当验证集**，不参与训练，只用来监控 |
| `verbose=0` | 不打印进度条（所以代码里手动打印了 history） |
| 返回值 `history` | 记录了每轮的 `loss`、`accuracy`、`val_accuracy`，供你画曲线分析 |

### 7.2 为什么要分批（batch）而不是一次全喂？

```
一次全喂（batch = 全部 1437 条）:
  内存占用大；一个 epoch 只更新 1 次参数 → 收敛极慢

分批（batch = 32 条）:
  一个 epoch 更新 ⌈1437/32⌉ = 45 次参数 → 收敛快得多
  还带来随机性，有助于跳出局部最优
```

代价是每次更新的方向只是"一批数据的近似方向"，会有噪声、loss 曲线会有抖动——但这通常**反而是好事**（噪声帮助跳出浅的局部最优）。所以 `batch_size` 是"梯度准确性"和"更新频率"之间的权衡。

### 7.3 `validation_split=0.2` 的作用

它按比例把训练数据分成两份：`80%` 真正训练，`20%` 只做验证。

**验证集绝不能参与训练。** 因为你需要一个"模型没见过"的数据集来诚实评估它——训练集上的表现好是理所当然的（甚至可以靠死记硬背达到 100%），只有没见过的新数据才能反映真实水平。这就是上一篇第 9 节"过拟合"的检测手段。

### 7.4 真实训练日志怎么读

```
  epoch  1: loss=2.1168, acc=32.90%, val_acc=70.49%
  epoch  2: loss=1.3707, acc=74.50%, val_acc=85.07%
  epoch  3: loss=0.6672, acc=86.25%, val_acc=90.62%
  epoch  4: loss=0.4295, acc=89.64%, val_acc=90.62%
  epoch  5: loss=0.3137, acc=92.34%, val_acc=91.67%
  epoch  6: loss=0.2566, acc=92.43%, val_acc=93.40%
  epoch  7: loss=0.1929, acc=95.74%, val_acc=93.40%
  epoch  8: loss=0.1802, acc=94.87%, val_acc=93.75%
  epoch  9: loss=0.1415, acc=96.43%, val_acc=94.79%
  epoch 10: loss=0.1582, acc=95.65%, val_acc=94.44%
```

**三列的含义**：

- **`loss` 一路下降（2.1168 → 0.1582）**：这是训练**正常**的首要标志。loss 不降或乱跳，说明学习率、数据、损失函数哪里有问题。
- **`acc`（训练准确率）上升**：模型在训练数据上越做越好。
- **`val_acc`（验证准确率）**：从 70.49% 涨到 94.79% 附近，说明**泛化能力也在提升**，不是死记硬背。

**几个值得注意的细节**：

1. **epoch 1 的 acc=32.90% 但 val_acc=70.49%**：训练准确率反而**低于**验证准确率，这看似矛盾，其实很常见——因为 `acc` 是整个 epoch 的平均值，而模型在这个 epoch 内一直在变强，前期拉低了平均；`val_acc` 是在 epoch **结束后**用最终参数算的。看懂这一点就不会被误导。
2. **epoch 7 的 acc=95.74% 高于 epoch 8 的 94.87%**：训练准确率出现小幅回落是正常的，因为每批数据的难度不同、且参数在持续变动。**看趋势，不要盯单点**。
3. **`val_acc` 到后期增长变慢（93.40% → 93.75% → 94.79% → 94.44%）**：最后还降了一点，这是**过拟合的早期信号**。此时应该考虑：加大 Dropout、加 L2 正则、或者用 `EarlyStopping` 早停（见第 12 节）。**如果继续训到 100 轮，val_acc 很可能持续走低而 acc 继续升高**——那才是典型的过拟合。

**判断过拟合的方法**：盯住 `acc` 与 `val_acc` 的**差距**。差距小 → 健康；差距持续拉大（如 acc=99% 而 val_acc=85%）→ 过拟合，需要正则化。

---

## 8. 评估与预测

```python
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"测试集准确率: {test_acc:.2%}")
```

真实输出：`测试集准确率: 96.94%`

**验证集和测试集有什么区别？** 这是个高频疑问：

| | 验证集 validation | 测试集 test |
|---|---|---|
| 来源 | 从训练集里切出来的 20% | 一开始就留出来，`train_test_split` 切的 360 条 |
| 用途 | **训练过程中**监控、调超参、早停 | **训练完全结束后**做最终评估 |
| 能用几次 | 反复用（每次调参都看） | **最好只用一次** |

**为什么测试集只能用一次？** 如果你反复看测试集结果来调超参，测试集就变相成了验证集，你其实是在"针对测试集调优"，它就不再是"没见过的新数据"了，评估结果会虚高。这是机器学习实验的纪律问题。

预测：

```python
preds = model.predict(x_test[:5], verbose=0)
print(f"前5张图预测: {np.argmax(preds, axis=1).tolist()}")
```

真实输出：

```
前5张图预测: [6, 9, 3, 7, 2]
前5张图真实: [6, 9, 3, 7, 2]
```

**`np.argmax(preds, axis=1)` 在做什么？** 模型的输出是 10 个概率，比如 `[0.01, 0.02, ..., 0.97, ...]`。`argmax` 取**最大值的下标**，也就是"概率最高的那个类别"。`axis=1` 表示"在每一行（每个样本）的 10 个值里找最大的"。

**为什么输出 10 个数而不是直接给一个类别？** 因为概率携带更多信息——"60% 是 3，30% 是 5"和"99% 是 3"背后的确定性完全不同。下游可以根据置信度做决策（比如置信度太低就转人工）。

---

## 9. 手动挡：GradientTape 自定义训练循环

`model.fit` 是自动挡，但有些场景需要更细的控制（自定义损失、多模型交替训练、GAN 的对抗训练等），这时用第 3 节的 `GradientTape` 手写循环：

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)      # ① 前向
        loss = loss_fn(y, predictions)             # ② 损失
    gradients = tape.gradient(loss, model.trainable_variables)   # ③ 反向
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))  # ④ 更新
    return loss
```

**逐行拆解**：

| 代码 | 说明 |
|---|---|
| `@tf.function` | 把这个 Python 函数**编译成计算图**。第一次调用时追踪、编译，之后执行编译好的图，**速度显著提升**（这是 TF 1.x 静态图优势的"按需启用"版本） |
| `with tf.GradientTape() as tape` | 开始录像，**必须包住前向计算** |
| `model(x, training=True)` | `training=True` 很关键：它告诉 Dropout/BatchNorm **"现在是训练模式"**，Dropout 才会生效。推理时应传 `training=False`（或 `model(...)` 默认） |
| `tape.gradient(loss, model.trainable_variables)` | 一次求出**所有**可训练参数的梯度，返回一个列表。对比上一篇手写 `dW1, db1, dW2, db2` 四个变量——框架自动梳理了整个计算图 |
| `zip(gradients, variables)` | 把"梯度"和"参数"配成对，`apply_gradients` 需要这种配对形式 |

**`training=True` 这个参数意义重大**：它体现了**训练模式和推理模式的差异**。Dropout 只在训练时随机丢弃，推理时必须关掉（否则结果不稳定）；BatchNorm 在两种模式下对统计量的处理也不同。这就是为什么下一篇 PyTorch 里要显式写 `model.train()` / `model.eval()`。

**什么时候用哪种？**

- 结构标准、损失标准 → 用 `model.fit`，省事
- 需要自定义损失、多优化器、对抗训练、梯度裁剪 → 用 `GradientTape` 手写

---

## 10. 函数式 API：Sequential 不够用的时候

`Sequential` 只能表达"一条直线串下去"。当模型需要**多输入、多输出、分支、跳跃连接**（如 ResNet）时，要用函数式 API——**把层当作函数来调用**：

```python
inputs = keras.Input(shape=(64,))
h = layers.Dense(64, activation="relu")(inputs)      # 注意结尾的 (inputs)
outputs = layers.Dense(10, activation="softmax")(h)
model2 = keras.Model(inputs=inputs, outputs=outputs)
```

**关键区别看括号**：

```python
layers.Dense(64)          # 创建一个层对象（还没接上任何东西）
layers.Dense(64)(inputs)  # 把这个层"作用"在 inputs 上，返回新张量
```

这就是"函数式"的含义：**层就是函数，网络就是函数的复合**。因为中间结果都是显式的变量（`h`、`outputs`），你可以随意把它接到多个地方：

```
Sequential 只能这样:       函数式还能这样:
  x → A → B → y              x ─► A ─┬─► B ─┐
                                     └─► C ─┴─► 相加 → y   ← 分支/残差
```

真实输出对比参数量：

```
函数式模型参数量: 4,810
Sequential 模型参数量: 17,226
```

**两者参数量不同是正常的**，因为结构不一样：函数式那个只有 `Dense(64)` 和 `Dense(10)` 两层（`64×64+64 = 4160`，`64×10+10 = 650`，合计 4,810），比 Sequential 少了一层 128 维的。

---

## 11. 保存与加载

```python
with tempfile.TemporaryDirectory() as tmp_dir:     # 用临时目录, 不留垃圾文件
    path = os.path.join(tmp_dir, "model.keras")
    model.save(path)                               # 保存结构 + 权重
    loaded = keras.models.load_model(path)
    acc = loaded.evaluate(x_test, y_test, verbose=0)[1]
```

真实输出：`重新加载后测试集准确率: 96.94% (与保存前一致)` ✓

**为什么准确率必须一致？** 这是**保存加载正确性的验证方法**。如果重新加载后准确率变了，说明权重没存全或结构不匹配。**养成这个验证习惯**——上线前模型加载出错是最危险的 bug 之一，本地验一遍能省掉大量排错时间。

三种保存形式：

| 写法 | 保存内容 | 用途 |
|---|---|---|
| `model.save('m.keras')` | 结构 + 权重 + 优化器状态 | **推荐**，可直接 `load_model` 复原 |
| `model.save_weights('w.h5')` | 只有权重 | 需要自己先重建相同结构再 `load_weights` |
| `model.save('dir/')` | SavedModel 格式 | 生产部署（TF Serving） |

**为什么代码用 `tempfile.TemporaryDirectory()`？** 它在 `with` 块结束时**自动删除整个目录**，避免在项目里堆积临时模型文件。这是一个值得学的整洁习惯。

---

## 12. 常用能力速查

以下能力代码里没有完整演示，但都属于"知道有这个选项，需要时查文档"的部分。

### 回调函数 callbacks

训练过程中自动触发的挂钩，解决的是"**训练过程不可控**"的问题：

```python
cb = [
    callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3),
    callbacks.ModelCheckpoint('best_model.keras', save_best_only=True),
    callbacks.TensorBoard(log_dir='./logs'),
]
model.fit(x, y, callbacks=cb)
```

| 回调 | 解决什么问题 | 关键参数 |
|---|---|---|
| `EarlyStopping` | 过拟合（val_loss 开始上升就停） | `patience=5` 容忍 5 轮不改善；`restore_best_weights` 回滚到最佳的权重，而不是停在最差的那轮 |
| `ReduceLROnPlateau` | 学习率固定导致后期震荡 | 验证损失不降就**自动把 lr 减半**（`factor=0.5`），相当于从大步走近到小步微调 |
| `ModelCheckpoint` | 训到一半崩了就全白干 | 自动存权重，`save_best_only` 只留最好的 |
| `TensorBoard` | 曲线那么多，print 看不清 | 启动可视化面板看 loss/acc 曲线、计算图 |

**配合用法**：`EarlyStopping` 防过拟合，`ReduceLROnPlateau` 让后期更稳——这两个几乎总是搭配使用。

### 数据增强

针对图像，**在训练时随机变换输入，但不改变语义**：

```python
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),     # 随机水平翻转
    layers.RandomRotation(0.1),          # 随机旋转 ±10%
    layers.RandomZoom(0.1),              # 随机缩放
])
```

**为什么增强有用？** 一张猫的图片水平翻转后仍然是猫。等于**免费扩大了数据集**，并且强迫模型学到"翻转不变"的特征，而不是死记某个像素位置。注意：**验证/测试集不做增强**（要保持原样的确定性）。

### 迁移学习

数据少的时候，用别人在海量数据上预训练好的模型，只改最后几层：

```python
base_model = keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False       # 冻结预训练层

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dense(10, activation="softmax"),
])

base_model.trainable = True        # 解冻后用小学习率微调
model.compile(optimizer=keras.optimizers.Adam(1e-5), loss='categorical_crossentropy')
```

**为什么这样有效？** 预训练模型在 ImageNet（1400 万张图）上学到的浅层特征（边缘、纹理、颜色）是**通用的**，大多数视觉任务都用得上。你的小数据集只负责教它"怎么把这些通用特征组合成本任务的答案"。

**关键顺序和参数**：

- `include_top=False`：去掉 ImageNet 专用的 1000 类分类头，只保留特征提取主体
- `trainable = False`：**冻结**，训练时不更新这些层的权重，避免小数据集把预训练知识冲垮
- 解冻微调时**学习率要调小（1e-5）**：因为此时参数已经很好了，大学习率会把它们毁掉
- `GlobalAveragePooling2D`：把特征图在空间维度上取平均，压成一个向量——比 `Flatten` 参数少得多

---

## 13. 切换到 MNIST（真实数据）

代码用的是 8×8 的 digits，方便离线跑。换成标准的 MNIST（28×28，6 万张）只需两步：

```python
# 1. 换数据源
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0    # 28×28=784, 像素 0-255 → 0-1
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# 2. 把模型输入的 64 改成 784, 其余代码完全不变
keras.Input(shape=(784,))
```

**改动只有两个数字**，说明前面的整个流程（模型定义、compile、fit、evaluate）是**通用的**——这正是用框架的价值。

注意 `reshape(-1, 784)` 的 `-1`：让 numpy 自动推断这一维的大小（60000），也是 28×28=784 的来处。归一化从 `/16` 变成 `/255`，因为 MNIST 像素是 0~255。

> 首次运行需联网下载约 11MB 数据。

---

## 14. 本文小结

| 你写的代码 | 框架替你做了什么 | 对应上一篇 |
|---|---|---|
| `layers.Dense(128, "relu")` | 创建权重矩阵并管理参数 | 第 1、5 节 |
| `GradientTape` | 自动求链式法则的全部梯度 | **第 7 节（核心）** |
| `compile(optimizer=...)` | 实现参数更新策略 | 第 8 节 |
| `compile(loss=...)` | 计算可导的误差 | 第 6 节 |
| `fit()` | 外层 epoch 循环 + 内层 batch 循环 + 前向/反向/更新 + 验证 | **第 12 节全流程** |
| `model.summary()` | 自动推导每层形状与参数量 | 第 5 节 |

**框架让你少写的代码，正是上一篇你手写过的那些**。所以如果上一篇的原理没吃透，用框架时就会变成"抄配方"——能跑，但 loss 不降时无从下手。

下一篇 `4_pytorch_demo.md` 会看到同一个网络、同一份数据，PyTorch 是怎么写、以及和 TF 的设计哲学差在哪里。

## 代码

讲解对应的示例代码见 `3_tensorflow_demo.py`，可直接运行。

代码中的数据使用 sklearn 自带的 digits 数据集（8×8 手写数字，离线可用、无需下载），模型结构与本文示例一致，只需把输入维度从 64 换成 784 即可切换到 MNIST。