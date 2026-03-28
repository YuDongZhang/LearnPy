# 7. Python独有特性（Java没有的）

## 列表推导式

```python
# 一行创建列表
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# 字典推导式
d = {k: v for k, v in zip(keys, values)}

# 集合推导式
s = {x % 10 for x in range(100)}
```

## 解包

```python
# 元组解包
a, b, c = 1, 2, 3
x, y = y, x  # 交换变量，不需要temp

# 列表解包
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2,3,4]
first, *mid, last = [1, 2, 3, 4, 5]  # mid=[2,3,4]

# 字典解包
def func(**kwargs): ...
merged = {**dict1, **dict2}
```

## 生成器

```python
# 惰性求值，不占内存
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 生成器表达式
total = sum(x**2 for x in range(1000000))  # 不创建列表
```

## 装饰器

```python
# 给函数加功能，不改原代码
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time()-start:.2f}s")
        return result
    return wrapper

@timer
def slow_func():
    time.sleep(1)
```

## 上下文管理器

```python
# 自动资源管理
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"耗时: {time.time()-start:.2f}s")

with timer():
    do_something()
```

## 多重赋值和交换

```python
a, b, c = 1, 2, 3
a, b = b, a  # 交换，Java需要temp变量
```

## 链式比较

```python
if 0 < x < 100:  # Java: if (x > 0 && x < 100)
    ...
```

## walrus运算符（:=）

```python
# 赋值的同时使用
if (n := len(data)) > 10:
    print(f"数据太多: {n}")

# 循环中
while (line := f.readline()):
    process(line)
```

## 字典合并（3.9+）

```python
merged = dict1 | dict2  # Java没有这么简洁的方式
```

## 下划线用法

```python
_ = "忽略的变量"
1_000_000  # 数字分隔符，等于1000000
for _ in range(10):  # 不需要循环变量
    do_something()
```

## 关键记忆点

1. **列表推导式** — `[expr for x in iter if cond]`，替代Stream
2. **解包** — `a, b = b, a` 交换，`first, *rest = list` 拆分
3. **生成器** — `yield` 惰性求值，处理大数据
4. **装饰器** — `@decorator` 给函数加功能
5. **f-string** — `f"hello {name}"` 字符串格式化
6. **with语句** — 自动资源管理
7. **链式比较** — `0 < x < 100`
8. **一切皆对象** — 函数也是对象，可以传递、赋值
