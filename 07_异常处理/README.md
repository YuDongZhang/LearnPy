# 第七章：异常处理

## 本章目标
- 理解异常的概念
- 掌握 try/except 语句
- 学会自定义异常
- 掌握调试技巧

---

## 1. 什么是异常

异常是程序运行时发生的错误。如果不处理，程序会崩溃。

```python
print(10 / 0)  # ZeroDivisionError
print(int("abc"))  # ValueError
```

---

## 2. try/except 语句

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为零")
```

---

## 3. 异常类型

| 异常 | 说明 |
|------|------|
| `Exception` | 所有异常的基类 |
| `ValueError` | 值错误 |
| `TypeError` | 类型错误 |
| `ZeroDivisionError` | 除零错误 |
| `IndexError` | 索引越界 |
| `KeyError` | 键不存在 |
| `FileNotFoundError` | 文件不存在 |

---

## 4. 完整结构

```python
try:
    # 可能出错的代码
except SomeError as e:
    # 处理异常
else:
    # 无异常时执行
finally:
    # 始终执行
```

---

## 5. 示例文件

- `basic_try.py` - 基本异常处理
- `multiple_except.py` - 多异常处理
- `raise_demo.py` - 抛出异常
- `custom_exception.py` - 自定义异常
- `debug_tips.py` - 调试技巧

---

## 上一章 | 下一章

[第六章：文件操作](../06_文件操作/README.md) | [第八章：面向对象](../08_面向对象/README.md)
