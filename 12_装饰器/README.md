# 第十二章：装饰器

## 本章目标
- 理解装饰器的概念
- 掌握装饰器的基本语法
- 学会创建自定义装饰器
- 理解带参数的装饰器

---

## 1. 什么是装饰器

装饰器是一种特殊的函数，用于修改或增强其他函数的功能，而不需要修改原函数的代码。

**核心思想**：函数可以作为参数传递，也可以作为返回值返回。

```python
def my_decorator(func):
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@my_decorator
def say_hello():
    print("你好！")

say_hello()
```

---

## 2. 装饰器语法糖

`@decorator` 是装饰器的语法糖，等价于：

```python
def say_hello():
    print("你好！")

say_hello = my_decorator(say_hello)
```

---

## 3. 处理函数参数

使用 `*args` 和 `**kwargs` 接收任意参数：

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("执行前")
        result = func(*args, **kwargs)
        print("执行后")
        return result
    return wrapper
```

---

## 4. 保留函数信息

使用 `functools.wraps` 保留原函数的元信息：

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 5. 带参数的装饰器

```python
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("你好！")
```

---

## 6. 类装饰器

使用类实现装饰器：

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"调用次数: {self.count}")
        return self.func(*args, **kwargs)
```

---

## 7. 常见装饰器应用

| 应用场景 | 说明 |
|---------|------|
| 日志记录 | 记录函数调用信息 |
| 性能测试 | 测量函数执行时间 |
| 权限验证 | 检查用户权限 |
| 缓存 | 缓存函数结果 |
| 重试 | 失败后自动重试 |

---

## 8. 示例文件

请查看并运行以下示例文件：
- `decorator_basics.py` - 装饰器基础
- `practical_decorators.py` - 实用装饰器示例
- `advanced_decorators.py` - 高级装饰器

---

## 练习题

1. 编写一个装饰器，在函数执行前后打印"开始"和"结束"
2. 编写一个装饰器，计算函数执行时间
3. 编写一个带参数的装饰器，控制函数重复执行的次数

---

## 上一章 | 下一章

[第十一章：迭代器](../11_迭代器/README.md) | [第十三章：正则表达式](../13_正则表达式/README.md)
