# 4. PyTorch 框架示例

> 上一篇用 TensorFlow/Keras 时，训练是 `model.fit()` 一行。
> 这一篇 PyTorch 会把训练循环**拆开写**——看起来更啰嗦，但恰好能让你看清上一篇被封装掉的东西：
> **前向、反向、清零、更新，这四步每一步到底在干什么。**
>
> 文中的输出都是 `4_pytorch_demo.py` 的真实运行结果。

---

## 1. PyTorch 的设计哲学：动态图

PyTorch 是 Facebook（现 Meta）2016 年开源的框架，和 TensorFlow 最大的区别是**计算图的构建时机**：

| | TensorFlow 1.x | **PyTorch** | TensorFlow 2.x |
|---|---|---|---|
| 计算图 | 先定义完整张图，再执行 | **运行时动态构建** | Eager 动态 + `@tf.function` 可编译 |
| 心智模型 | 声明式（像配置） | **命令式（像 numpy）** | 混合 |
| 调试 | 困难 | **简单，可断点** | 简单 |

PyTorch 的核心主张是：**"像写 Python 一样写深度学习"**。你写的 `x = a @ b` 会**立刻**执行并得到结果，而不是"向图里添加一个节点"。

```python
import torch
x = torch.tensor([1, 2, 3])
y = x * 2          # 立刻算出 [2, 4, 6]，不是"注册一个乘法操作"
```

因为是动态的，计算图**每次前向传播都重新构建一次**。这带来一个直接后果（第 3.4 节会看到）：**图用完就释放**，所以中间结果不能无限保留。

```bash
pip install torch torchvision torchaudio

# GPU 版本 (需要 CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

运行环境：本文验证于 **PyTorch 2.8.0+cpu**（CPU 版）。

```python
print(f"CUDA available: {torch.cuda.is_available()}  (CPU 版, 本示例在 CPU 上运行)")
```

真实输出 `CUDA available: False`——没有 GPU 也能跑完本文所有示例（数据很小）。GPU 的检查方式和用法见第 10 节。

---

## 2. 张量基础

```python
x = torch.tensor([1, 2, 3])
print(f"张量: {x.tolist()}, dtype={x.dtype}, shape={tuple(x.shape)}")
print(f"随机矩阵 (3x4):\n{torch.randn(3, 4).round(decimals=2).numpy()}")
```

真实输出：

```
张量: [1, 2, 3], dtype=torch.int64, shape=(3,)
随机矩阵 (3x4):
[[ 0.31  0.94  0.45  0.56]
 [ 0.05 -0.7  -2.04 -1.32]
 [-2.68 -0.18  0.36  1.25]]
```

**三个关键属性**（看任何张量先看这三个）：

| 属性 | 含义 | 为什么重要 |
|---|---|---|
| `dtype` | 数据类型 | 这里是 `int64`（因为输入是整数）。**模型权重必须是浮点型**（float32），整数张量不能求导 |
| `shape` | 形状 | `(3,)` 是一维；**形状不匹配是深度学习第一大类报错** |
| `device` | 所在设备 | CPU 还是 GPU。**模型和数据的 device 必须一致**，否则报错 |

**`torch.randn(3, 4)` 生成标准正态分布（均值 0、方差 1）的随机数**，注意输出里有 `-2.68`、`-2.04` 这样的负数——这正是它和 `torch.rand`（均匀分布 0~1）的区别。**权重初始化用的就是这类随机数**，上一篇第 10 节的 He 初始化也是基于正态分布再乘以 `sqrt(2/n)`。

`.round(decimals=2)` 只是为了打印好看，`.numpy()` 把 torch 张量转成 numpy 数组。

---

## 3. autograd：PyTorch 的自动微分

### 3.1 requires_grad 是什么

```python
t = torch.tensor(3.0, requires_grad=True)     # 声明"我要对它求导"
y = t ** 2                                    # y = t², 导数 2t
y.backward()                                  # 反向传播
print(f"dy/dx = {t.grad.item()}  (理论值 2x = 6.0)")
```

真实输出：`dy/dx = 6.0  (理论值 2x = 6.0)` ✓

**`requires_grad=True` 是整件事的开关**：

```python
t = torch.tensor(3.0)                # 默认 requires_grad=False
y = t ** 2
y.backward()
# RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

这个报错是新手必踩的坑，含义很直白：**你没说要对谁求导，PyTorch 就没记录它的计算过程，自然算不出梯度**。

### 3.2 计算图是"跟着数据长出来的"

执行 `y = t ** 2` 时，PyTorch 顺手在 `y` 上挂了一个 `grad_fn`：

```
t (requires_grad=True, 叶子节点)
│  ↑ .grad 会存这里
└─ PowBackward0  ← y.grad_fn，记录了"我是由 t 的 2 次幂算出来的"
   │
   └─ y
```

**关键**：每个张量都知道"我是怎么来的"（`grad_fn`），整条链就自动串成了一张图。**你不需要手动构建图**——这就是"动态图"的实现方式，图是随着你的代码执行自然生长的。

`y.backward()` 做的事情：**从 `y` 出发，沿着 `grad_fn` 反向走完整张图，用链式法则算出每个叶子节点的梯度，累加写进 `t.grad`**。

对照上一篇第 7 节，完全是一回事：

| 手写 numpy | PyTorch |
|---|---|
| `dz2 = (a2 - y) / m` | 自动求出 |
| `dW2 = a1.T @ dz2` | 自动求出 |
| `self.W2 -= lr * dW2` | `optimizer.step()` |

**区别是：框架自动处理了所有链式法则和形状变换。** 上一篇你手推了 `∂L/∂z = a - y` 那个漂亮结果，PyTorch 内部也是这么算的（这类"融合化简"是自动微分引擎的优化之一）。

### 3.3 `.grad` 为什么存在张量自身上

注意 `t.grad`——**梯度是挂在参数上的属性，不是 `backward()` 的返回值**。

**为什么这样设计？** 因为一张网络有几十上百个参数，如果 `backward()` 返回一个列表，你还得自己维护"哪个梯度对应哪个参数"的映射，极易出错。挂在参数上之后，梯度和参数永远绑定在一起，`optimizer` 只需遍历 `model.parameters()` 就能拿到每个参数的梯度：

```python
for p in model.parameters():
    p.data -= lr * p.grad      # 这就是 optimizer.step() 的核心
```

### 3.4 一个容易被忽略的细节：图用完就释放

```python
y.backward()      # 第一次：正常
y.backward()      # 第二次：RuntimeError: Trying to backward through the graph a second time
```

因为 `backward()` 结束后，为了**省内存**，PyTorch 会**释放掉计算图里的中间缓存**。需要重复反向传播（如多个 loss 分别 backward）时要加 `retain_graph=True`。

**这个设计反映出 PyTorch 的核心权衡**：动态图灵活，但图是临时的，所以必须主动管理内存。相比 TF 1.x 那种"图常驻"，动态图在训练循环里每次都重建图，反而更省内存。

---

## 4. 定义网络：nn.Module

```python
class Net(nn.Module):
    """64 -> 128 -> 10"""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)
```

**固定套路**（结构永远是这两部分）：

| 部分 | 干什么 | 注意 |
|---|---|---|
| `__init__` | **声明有哪些层**（以及它们的形状） | 必须调用 `super().__init__()`，否则 nn.Module 的内部机制不工作 |
| `forward` | **定义数据怎么流过这些层** | 名字必须是 `forward`，PyTorch 按约定调用它 |

**`nn.Linear(64, 128)` 是什么？** 就是全连接的 `z = x @ W.T + b`，内部管理一个 (128, 64) 的权重和一个 (128,) 的偏置，**并且自动设好 `requires_grad=True`**。对比上一篇手写 `W1 = np.random.randn(2, 8) * np.sqrt(2/n_in)`——形状、初始化、梯度开关，框架全包了。

**注意 `nn.Linear` 存的是 `W.T`**（形状 `(out, in)` 而非 `(in, out)`），这是它和 numpy 手写时的一个差异，往前计算时自动转置。

**为什么不能直接调 `model.forward(x)`，而要 `model(x)`？**

```python
model(x)             # ✅ 正确
model.forward(x)     # ⚠️ 能跑，但跳过了 nn.Module 的包装逻辑
```

`model(x)` 实际调用的是 `nn.Module.__call__`，它会在 `forward` 前后自动处理 hook、`model.train()`/`eval()` 的状态切换等。**永远用 `model(x)`**。

### 参数量手算

```python
print(f"参数量: {sum(p.numel() for p in model.parameters()):,}")
```

真实输出 `参数量: 9,610`。

```python
sum(p.numel() for p in model.parameters())
```

逐项拆解：

| 代码 | 含义 |
|---|---|
| `model.parameters()` | 递归遍历所有子层的**可训练参数**（只含 `requires_grad=True` 的） |
| `p.numel()` | number of elements，该张量的**元素总数**（不是维度数） |
| `sum(...)` | 全部加起来 |

手算验证（公式仍是 `输入×输出 + 输出`）：

```
fc1: Linear(64→128):  64 × 128 + 128 = 8,320
fc2: Linear(128→10):  128 × 10 + 10  = 1,290
dropout:                              =     0   ← 没有参数
──────────────────────────────────────────────
合计                                   9,610   ✓
```

自测：`print(model)` 会打印出网络结构，能看到 `fc1: Linear(in_features=64, out_features=128, bias=True)`——**这就是 `nn.Linear` 内部管理的东西**。

---

## 5. DataLoader：数据是怎么被切碎的

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train_ds = TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train))
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
```

真实输出：

```
训练集 1437 条 / 测试集 360 条
训练集 batch 数: 23 (batch_size=64)
```

**三个概念的关系（PyTorch 的数据管道）**：

```
TensorDataset  →  DataLoader  →  训练循环
「有什么数据」   「怎么取数据」    「怎么用」
```

| 组件 | 职责 | 本文用法 |
|---|---|---|
| `TensorDataset(X, y)` | **把特征和标签配对**，第 i 个元素是 `(X[i], y[i])` | 数据已在内存里，直接包一层 |
| `DataLoader(ds, batch_size, shuffle)` | **按 batch 切分、打乱、迭代** | `batch_size=64`，训练集 `shuffle=True` |
| `for inputs, labels in train_loader` | 每次取出一批 | 见第 6 节 |

**`len(train_loader)` 为什么是 23？** 因为 `1437 / 64 = 22.45`，不能整除，最后一批只有 29 条，所以是 `⌈1437/64⌉ = 23` 批。

**`shuffle=True` 为什么重要？** 如果数据按类别排好序，每个 batch 可能全是同一类，梯度方向会剧烈摆动。打乱后每批的类别分布接近整体，梯度估计更稳。**训练集要打乱，测试集不用**（测试只看结果，顺序无关，还方便对齐标签）。

**为什么测试集 `batch_size=256`？** 因为评估只前向、不反向，不更新参数，**没有梯度累积的问题**，大批次能更快跑完、更省开销。

`TensorDataset` 之所以够用，是因为我们已经把数据读进内存了。**真实项目的数据量大得多**，这时要继承 `torch.utils.data.Dataset` 自定义 `__getitem__`，实现"用哪条读哪条"（懒加载），否则内存装不下。

---

## 6. 训练循环：四步逐行拆解（本文核心）

这是 PyTorch 区别于 Keras 的地方——**同样的事情要自己写**。也正因为自己写，每一步都看得见。

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(1, 11):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        outputs = model(inputs)            # ① 前向传播
        loss = criterion(outputs, labels)  # ② 计算损失

        optimizer.zero_grad()              # ③ 清零梯度
        loss.backward()                    # ④ 反向传播
        optimizer.step()                   # ⑤ 更新参数

        running_loss += loss.item()
```

### 6.1 五个步骤

| 步骤 | 代码 | 等价于上一篇手写的 |
|---|---|---|
| ① 前向传播 | `outputs = model(inputs)` | `nn.forward(X)` |
| ② 计算损失 | `loss = criterion(outputs, labels)` | `nn.loss(y)` |
| ③ **清零梯度** | `optimizer.zero_grad()` | *（手写版没有这一步，见 6.2）* |
| ④ 反向传播 | `loss.backward()` | `nn.backward(X, y, lr)` 的前半段 |
| ⑤ 更新参数 | `optimizer.step()` | `nn.backward(X, y, lr)` 的后半段 `W -= lr * dW` |

**`criterion` 和 `optimizer` 为什么要在循环外创建？**

- `criterion = nn.CrossEntropyLoss()`：损失函数**没有可学参数**，只是一个计算规则的实例，创建一次就够
- `optimizer = optim.Adam(model.parameters(), ...)`：`model.parameters()` 把参数的**引用**交给优化器，所以优化器能看到后续所有更新。如果放在循环内，每轮都会重建优化器，**Adam 累积的动量状态会被清空**（这是 Adam 学习率自适应的依据），训练效果直接变差。

### 6.2 为什么必须 zero_grad()——最容易踩的坑

**PyTorch 的梯度是累加的。** `loss.backward()` 执行的是 `p.grad += 新算出来的梯度`，**是加号，不是赋值**。

所以如果把 `zero_grad()` 去掉，会发生什么：

```
第 1 批:  p.grad = g₁
第 2 批:  p.grad = g₁ + g₂          ← 梯度越滚越大
第 3 批:  p.grad = g₁ + g₂ + g₃
...
第 k 批:  p.grad = g₁ + ... + g_k   ← 梯度是真实值的 k 倍
```

更新规则是 `p -= lr * p.grad`，梯度被放大 k 倍，**等效于学习率变成了 k 倍**。第 3 批时已经是 3 倍，越往后越夸张 → 参数乱飞、loss 变 NaN、训练彻底崩掉。

**验证方法**：把代码里的 `optimizer.zero_grad()` 注释掉再跑一次，你会看到 loss 迅速变成 `nan`。**动手试一次，比读十遍都记得牢。**

**为什么 PyTorch 要设计成累加？** 因为这带来两种有用的能力：

1. **大 batch 模拟**：显存装不下大 batch 时，可以分几次前向累积梯度，再统一 `step()` 一次——等效于一个大 batch
2. **多 loss 合并**：多个损失（如多任务学习）可以各自 `backward()`，梯度自动叠加

代价就是**必须手动清零**。这是 PyTorch 和 Keras 手感上最大的差别——Keras 的 `fit` 内部自动做了这件事，所以你从没意识到它的存在。

### 6.3 backward() 和 step() 各干什么

```
loss.backward()
  → 沿计算图反向走一遍，用链式法则算出每个参数的梯度
  → 写进 p.grad（累加）
  → 然后释放计算图的中间缓存

optimizer.step()
  → 遍历所有参数，按 p -= lr * p.grad 更新
  → 对 Adam 来说还包含：更新一阶动量、二阶动量、做偏差修正、自适应缩放
```

**注意 `step()` 和 `backward()` 的顺序**：必须先有梯度（`backward`）才能更新（`step`）。反过来会更新到旧的梯度上，等于用上一批的方向走这一步。

**`optimizer.zero_grad()` 的位置为什么在 `backward()` 之前？** 只要在 `backward()` 前清零就行（因为它要清的是上一轮的梯度）。有人习惯写在 `step()` 之后，效果一样。但**绝不能写在 `backward()` 之后**，那等于刚算完就抹掉。

### 6.4 `model.train()` 和 `running_loss`

```python
model.train()                       # 切到训练模式
running_loss = 0.0
...
    running_loss += loss.item()     # 累加本轮的 loss
...
print(f"  epoch {epoch:2d}: 平均 loss = {running_loss / len(train_loader):.4f}")
```

**`model.train()` 做了什么？** 它是个开关，通知所有层"现在是训练"：

| 层 | 训练模式 | 评估模式 |
|---|---|---|
| `Dropout` | **随机关闭**部分神经元 | 全部保留（用完整网络） |
| `BatchNorm` | 用**当前 batch** 的均值/方差，并更新滑动平均 | 用训练期累积的滑动平均，**不更新** |

**所以 `model.train()` 和 `model.eval()` 必须配对使用**——忘了写 `eval()`，Dropout 在推理时还在随机丢神经元，预测结果每次都不一样，这是非常典型的 bug。

**`loss.item()` 为什么要调 `.item()`？** `loss` 是一个**带计算图的张量**。如果直接累加 `running_loss += loss`，会把整张计算图都挂在 `running_loss` 上，**内存会一直涨**（图释放不掉）。`.item()` 把它取出成一个普通 Python 浮点数，计算图就被解放了。这是 PyTorch 里非常实用的一个习惯。

**除以 `len(train_loader)` 是因为 `running_loss` 累加的是每批的 loss 之和，要取平均。**

### 6.5 真实训练日志

```
  epoch  1: 平均 loss = 2.1802
  epoch  3: 平均 loss = 1.4687
  epoch  5: 平均 loss = 0.8268
  epoch 10: 平均 loss = 0.3532
```

**loss 从 2.1802 稳定降到 0.3532**——训练正常。

**epoch 1 的 2.1802 是什么水平？** 10 分类任务瞎猜的交叉熵是 `-ln(1/10) = ln(10) ≈ 2.303`。2.1802 比它略低，说明模型刚开始只能微弱地优于瞎猜，符合"参数基本还是随机初始化"的预期。

**这个初始值是个很实用的诊断锚点**：如果第一轮 loss 明显高于 2.303，说明初始化、数据处理或损失函数有问题；如果第一轮就远低于 2.303，要警惕数据泄露（答案不小心混进了输入）。

---

## 7. 评估：eval() 和 no_grad()

```python
model.eval()
correct = total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        preds = model(inputs).argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
print(f"测试集准确率: {correct / total:.2%}")
```

真实输出 `测试集准确率: 92.78%`。

**`model.eval()` + `torch.no_grad()` 是两个不同的东西，别记混**：

| | `model.eval()` | `torch.no_grad()` |
|---|---|---|
| 作用层面 | **层的计算行为** | **是否构建计算图** |
| 影响 | Dropout 关闭、BatchNorm 用滑动平均 | 不记录 `grad_fn`、不保存中间结果 |
| 不写会怎样 | 结果不稳定、不准 | 结果**正确**，但显存/内存暴涨 |

**`torch.no_grad()` 为什么能省内存？** 回顾第 3.2 节：只要前置张量带 `requires_grad`，运算就会挂 `grad_fn` 并保存反向传播需要的中间结果。推理时根本不需要反向，这些全在浪费。关掉之后，前向计算变成纯数值运算。

**必须两个都写**：`eval()` 保证**算得对**，`no_grad()` 保证**算得省**。

**`argmax(dim=1)` 和 Keras 的 `np.argmax(preds, axis=1)` 是一回事**——取概率最大的类别下标。`dim=1` 表示在"10 个类别"这一维上取最大值（`dim=0` 是 batch 维，取错了结果就完全无意义）。

**为什么不用 `sklearn` 的 accuracy_score？** 都可以。这里手写是为了展示 `correct / total` 这种"累积正确数除以总数"的基本统计方式。

**92.78% 和上一篇 Keras 的 96.94% 差了不少，怎么解释？** 这不是框架优劣，而是**配置差异**：

| | Keras 篇 | PyTorch 篇 |
|---|---|---|
| 网络 | 64→**128→64**→10（3 层） | 64→**128**→10（2 层） |
| 参数量 | 17,226 | 9,610 |

**网络更小、参数更少，表现差一些是合理的**。对比实验一定要控制变量，否则结论不可靠——这是实验设计的常识。

---

## 8. CNN：形状是怎么一层层变的

```python
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(32 * 2 * 2, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))   # 8x8 -> 4x4
        x = self.pool(torch.relu(self.conv2(x)))   # 4x4 -> 2x2
        x = torch.flatten(x, 1)
        return self.fc(x)
```

代码用一段**探针**把每步的形状打印出来（真实输出）：

```
  输入:       (4, 1, 8, 8)
  经过 conv1: (4, 16, 8, 8)
  经过 pool:  (4, 16, 4, 4)
  经过 conv2: (4, 32, 4, 4)
  经过 pool:  (4, 32, 2, 2)
  展平后:     (4, 128)
CNN 参数量: 6,090
```

**四维张量 `(N, C, H, W)` 的含义**（PyTorch 的固定顺序）：

| 位置 | 含义 | 本例 |
|---|---|---|
| N | batch 大小 | 4（探针输入了 4 张图） |
| C | **通道数**（channels / 特征图数量） | 1（灰度图）→ 16 → 32 |
| H | 高度 | 8 → 4 → 2 |
| W | 宽度 | 8 → 4 → 2 |

**逐层变化的原因**：

| 步骤 | 尺寸变化 | 为什么 |
|---|---|---|
| `conv1(1→16, k=3, pad=1)` | C: 1→16，H/W 不变 | **padding=1** 在边缘补一圈 0，抵消卷积核造成的缩小：`8 - 3 + 2×1 + 1 = 8`。通道 1→16 表示**用 16 个不同的卷积核提取 16 种特征** |
| `pool(k=2)` | 8→4 | 每 2×2 区域取最大值，尺寸减半。**通道数不变**（池化只在空间维度操作） |
| `conv2(16→32, k=3, pad=1)` | C: 16→32，H/W 不变 | 输入 16 个通道 → 每个输出通道对这 16 个通道**全部**做卷积再求和 |
| `pool(k=2)` | 4→2 | 再减半 |
| `flatten(x, 1)` | (4,32,2,2) → (4,128) | 把每张图的 `32×2×2=128` 个值摊平成一维，**因为全连接层只接受向量** |

**`flatten(x, 1)` 的 `1` 是什么意思？** 从第 1 维开始展平，**保留第 0 维（batch）**。写成 `flatten(x)` 会把 batch 也摊平，那就全乱了。

**`nn.Linear(32*2*2, 10)` 里的 `32*2*2` 必须和展平后的 128 对应**——这是 CNN 里最常见的报错来源：改了卷积层或输入尺寸后，忘了同步改全连接层的输入维度，运行时报 `mat1 and mat2 shapes cannot be multiplied`。

**参数量手算（6,090）**：

```
conv1: Conv2d(1→16, 3×3)  = 1 × 16 × 3 × 3 + 16  =  144 + 16 =   160
conv2: Conv2d(16→32, 3×3) = 16 × 32 × 3 × 3 + 32 = 4608 + 32 = 4,640
fc:    Linear(128→10)                            =  1280 + 10 = 1,290
pool / flatten:                                               =     0
─────────────────────────────────────────────────────────────────────
合计                                                          6,090   ✓
```

**卷积层的参数公式：`输入通道 × 输出通道 × 核高 × 核宽 + 输出通道`**。

**对比一下"参数少"这个宣传**：全连接处理 8×8 灰度图到 10 类，若中间隐层也用 128，参数量是 `64×128+128 = 8,320`（比这个 CNN 还多）。而 CNN 用的是 **3×3 的小核在整张图上滑动，权值共享**——`conv1` 只有 9 个权重（外加 16 个偏置），**与图片大小完全无关**。输入变成 224×224 时，CNN 的参数量不变，全连接层却会爆炸式增长。

**为什么池化层没有参数？** 它只做"取最大值"这种固定的聚合操作，没有任何需要学习的东西。

> 卷积的滑动计算细节、为什么它能保留空间结构、感受野等，见下一篇 `5_cnn_image_classification.md`。

---

## 9. 保存与加载：为什么推荐存 state_dict

```python
model.eval()
with tempfile.TemporaryDirectory() as tmp_dir:      # 用临时目录, 不留垃圾文件
    path = os.path.join(tmp_dir, "model.pth")
    torch.save(model.state_dict(), path)            # 推荐: 只保存权重

    reloaded = Net()
    reloaded.load_state_dict(torch.load(path))
    reloaded.eval()

    probe = torch.from_numpy(X_test[:5])
    with torch.no_grad():
        same = torch.allclose(model(probe), reloaded(probe))
```

真实输出：`重新加载后输出与原模型一致: True` ✓

**`state_dict` 是什么？** 一个 Python 字典，把**每一层的名字映射到它的权重张量**：

```python
{'fc1.weight': tensor(...), 'fc1.bias': tensor(...),
 'fc2.weight': tensor(...), 'fc2.bias': tensor(...)}
```

**两种保存方式的区别**：

| 方式 | 存什么 | 优点 | 风险 |
|---|---|---|---|
| `torch.save(model, path)` | 整个模型对象（**含类的定义路径**） | 一行搞定 | **依赖类的路径**：代码重构后路径变了就加载失败；跨项目/跨版本很脆弱 |
| `torch.save(model.state_dict(), path)` | **只有权重数值** | 稳定、可移植、体积小 | 需要自己先 `Net()` 建好结构再 `load_state_dict` |

**所以推荐 `state_dict`**。多写一行 `Net()`，换来的是加载的可靠性。

**两个关键细节**：

1. **`reloaded = Net()` 必须在 `load_state_dict` 之前**，且结构和原模型**完全一致**。`load_state_dict` 是按名字"对号入座"地填权重，名字或形状对不上会直接报错——这个报错机制其实是好事，能及早发现结构不一致。
2. **`model.eval()` 要在保存和加载后都调用**（代码里保存前调了一次）。原因见第 7 节：`eval()` 影响 Dropout 的行为。**如果保存时是训练模式、加载后忘了切回 `eval()`，两次前向结果就会不同**——这类"结果对不上"的 bug 极难排查，所以第 7 节强调过两个模式必须配对。

**`torch.allclose()` 是验证手段**：逐元素比较两个张量是否近似相等（浮点运算有微小误差，不能用 `==`）。**这个习惯值得学**——模型保存/加载是最容易出静默错误的地方，本地验一遍能省掉线上排障的大量时间。

**checkpoint（断点续训）**：训练中断后要接着训，光存权重不够，还要存优化器状态（Adam 的动量）：

```python
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),   # Adam 的动量状态
    'loss': loss,
}
```

**为什么必须存 `optimizer_state_dict`？** 因为 Adam 的更新依赖历史梯度的一阶/二阶动量（第 6.1 节提到过）。不存的话，续训时动量从零开始，训练曲线会出现明显的"重新爬坡"。

---

## 10. 扩展阅读（速查）

### 迁移学习

```python
import torchvision.models as models

model = models.resnet18(weights='DEFAULT')          # 预训练权重

for param in model.parameters():
    param.requires_grad = False                     # 冻结主干

num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 10)              # 换掉分类头

for param in model.layer4.parameters():
    param.requires_grad = True                      # 解冻最后一组卷积层微调

optimizer = optim.Adam(model.parameters(), lr=1e-4) # 微调用小学习率
```

**逐行理解**：

| 代码 | 为什么 |
|---|---|
| `weights='DEFAULT'` | 加载 ImageNet 预训练权重。**注意：旧写法 `pretrained=True` 已弃用** |
| `requires_grad = False` | 冻结：这些层的参数不更新，也不用算梯度（**顺带省显存**） |
| `model.fc = nn.Linear(...)` | 替换分类头。`in_features` 是原模型全连接层的输入维度，自动读出来比手写数字可靠 |
| 解冻 `layer4` | 让**靠近输出**的层参与微调（浅层特征更通用，深层更任务相关） |
| `lr=1e-4` | 预训练权重已经很好，大学习率会把它们破坏掉 |

**这和 Keras 篇的迁移学习是同一套思路**，只是 API 不同：Keras 用 `base_model.trainable = False`，PyTorch 用 `requires_grad = False`。**冻结的本质都是"关掉这个参数的梯度，让优化器跳过它"**。

### GPU 训练

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CNN().to(device)

for inputs, labels in train_loader:
    inputs, labels = inputs.to(device), labels.to(device)
```

**要点**：`model` 和**每一批数据**都要 `.to(device)`。模型上了 GPU 而数据还在 CPU，运算时会报设备不匹配的错误。`nn.DataParallel(model)` 可做多卡并行（更推荐 `DistributedDataParallel`）。

### PyTorch Lightning

进一步封装训练循环，省去手写那四步：

```python
import pytorch_lightning as pl

class LitModel(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        return nn.functional.cross_entropy(y_hat, y)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=0.001)

trainer = pl.Trainer(max_epochs=10)
trainer.fit(LitModel(), train_loader)
```

`training_step` 返回 loss，Lightning 自动处理 `zero_grad` / `backward` / `step`、设备迁移、日志记录、多卡训练。

**这和 Keras 的 `model.fit` 是同一个层次的抽象**——把第 6 节的样板代码收起来。需 `pip install pytorch-lightning`。

**该不该用？** 建议先手写过第 6 节的循环，理解那五步之后再上封装。否则出了问题只会盯着 `trainer.fit` 发呆。

---

## 11. TensorFlow vs PyTorch 对照表

同一个 64→128→10 的网络，两篇的写法对照：

| 环节 | TensorFlow/Keras | PyTorch |
|---|---|---|
| 声明层 | `layers.Dense(128, activation='relu')` | `self.fc1 = nn.Linear(64, 128)` + `forward` 里 `torch.relu` |
| 定义计算 | `Sequential` 自动按顺序连接 | **必须手写 `forward`** |
| 损失 + 优化器 | `model.compile(optimizer=..., loss=...)` | `criterion = nn.CrossEntropyLoss()` + `optim.Adam(...)` |
| **训练循环** | `model.fit(...)` 一行 | **手写五步** |
| 自动求导 | `with tf.GradientTape(): ...` | `loss.backward()`（图自动构建） |
| 更新参数 | `optimizer.apply_gradients(...)` | `optimizer.step()` |
| **清零梯度** | `fit` 内部自动做 | **必须手写 `optimizer.zero_grad()`** |
| 模式切换 | `model(x, training=True/False)` 参数控制 | **`model.train()` / `model.eval()` 全局开关** |
| 参数量 | `model.count_params()` | `sum(p.numel() for p in model.parameters())` |
| 保存 | `model.save('m.keras')`（含结构） | `torch.save(model.state_dict(), ...)`（只权重） |

**该怎么选？**

- **PyTorch**：调试直观、动态图灵活、学术界主流、论文复现和自定义模型方便 → **入门推荐，也是本文其余章节的默认选择**
- **TensorFlow/Keras**：`fit` 上手极快、部署工具链（TF Serving / TFLite / TF.js）成熟 → 快速原型、移动端/生产部署

**两者的核心概念完全相通**：前向传播、损失、反向传播、优化器、参数更新——这些在 [2_neural_network.md](2_neural_network.md) 里已经手推过一遍。**换个框架只是换 API，原理不变**。

## 代码

讲解对应的示例代码见 `4_pytorch_demo.py`，可直接运行。

代码中的数据使用 sklearn 自带的 digits 数据集（8×8 手写数字，离线可用、无需下载），完整覆盖张量、自动求导、nn.Module、DataLoader、训练循环、CNN、模型保存。最后的 PyTorch Lightning 一节需要额外安装 `pip install pytorch-lightning`。