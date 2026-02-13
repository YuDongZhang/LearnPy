# 第四章：函数

## 本章目标
- 理解函数的概念和作用
- 学会定义和调用函数
- 掌握参数传递
- 理解返回值和作用域

---

## 1. 什么是函数

函数是一段可重复使用的代码块，用于完成特定任务。

```python
def greet():
    print("你好！")

greet()  # 调用函数
```

---

## 2. 函数参数

### 位置参数
```python
def add(a, b):
    return a + b

result = add(3, 5)  # result = 8
```

### 默认参数
```python
def greet(name="朋友"):
    print(f"你好，{name}！")

greet()        # 你好，朋友！
greet("张三")  # 你好，张三！
```

### 关键字参数
```python
def info(name, age):
    print(f"{name}今年{age}岁")

info(age=25, name="张三")
```

---

## 3. 返回值

使用 `return` 返回结果：

```python
def square(x):
    return x * x

result = square(5)  # result = 25
```

---

## 4. 变量作用域

- **局部变量**：函数内部定义，只能在函数内使用
- **全局变量**：函数外部定义，可以在任何地方使用

```python
x = 10  # 全局变量

def func():
    x = 5  # 局部变量
    print(x)  # 输出 5
```

---

## 5. 示例文件

请查看并运行以下示例文件：
- `basic_function.py` - 函数基础
- `parameters.py` - 参数详解
- `return_value.py` - 返回值
- `scope.py` - 变量作用域

---

## 练习题

1. 编写函数计算圆的面积
2. 编写函数判断一个数是否为质数
3. 编写函数实现简单的计算器（加减乘除）

---

## 上一章 | 下一章

[第三章：控制流程](../03_控制流程/README.md) | [第五章：数据结构](../05_数据结构/README.md)
