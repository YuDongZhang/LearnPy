# 第九章：模块与包

## 本章目标
- 理解模块的概念
- 学会导入和使用模块
- 掌握自定义模块的创建
- 理解包的结构和使用

---

## 1. 什么是模块

模块是一个包含 Python 代码的 `.py` 文件。使用模块可以：
- 组织代码，使其更易维护
- 实现代码复用
- 避免命名冲突

---

## 2. 导入模块

### import 语句
```python
import math
print(math.sqrt(16))
```

### from...import 语句
```python
from math import sqrt, pi
print(sqrt(16))
print(pi)
```

### as 别名
```python
import math as m
print(m.sqrt(16))

from math import sqrt as square_root
print(square_root(16))
```

---

## 3. 常用内置模块

| 模块 | 说明 |
|------|------|
| `math` | 数学函数 |
| `random` | 随机数 |
| `datetime` | 日期时间 |
| `os` | 操作系统接口 |
| `sys` | 系统相关 |
| `json` | JSON 处理 |
| `re` | 正则表达式 |

---

## 4. 自定义模块

创建一个 `mymath.py` 文件：

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

PI = 3.14159
```

然后在其他文件中导入使用：

```python
from mymath import add, PI

print(add(3, 5))
print(PI)
```

---

## 5. `__name__` 变量

当一个模块被直接运行时，`__name__` 的值是 `"__main__"`：

```python
def main():
    print("程序启动")

if __name__ == "__main__":
    main()
```

这样可以区分模块是被导入还是直接运行。

---

## 6. 包 (Package)

包是一个包含 `__init__.py` 文件的目录，用于组织多个模块：

```
mypackage/
├── __init__.py
├── module1.py
└── module2.py
```

使用包：

```python
from mypackage import module1
from mypackage.module2 import some_function
```

---

## 7. 模块搜索路径

Python 会按以下顺序搜索模块：
1. 当前目录
2. `PYTHONPATH` 环境变量指定的目录
3. Python 安装目录的默认路径

查看搜索路径：

```python
import sys
print(sys.path)
```

---

## 8. 示例文件

请查看并运行以下示例文件：
- `import_demo.py` - 导入模块示例
- `custom_module.py` - 自定义模块
- `package_demo.py` - 包的使用示例

---

## 练习题

1. 使用 `random` 模块生成一个 1-100 的随机整数
2. 使用 `datetime` 模块输出当前日期和时间
3. 创建一个自定义模块，包含计算圆面积和周长的函数

---

## 上一章 | 下一章

[第八章：面向对象](../08_面向对象/README.md) | [第十章：列表推导式与生成器](../10_列表推导式与生成器/README.md)
