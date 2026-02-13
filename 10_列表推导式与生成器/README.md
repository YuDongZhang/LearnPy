# 第十章：列表推导式与生成器

## 本章目标
- 掌握列表推导式语法
- 学会字典和集合推导式
- 理解生成器的概念
- 掌握 yield 关键字的使用

---

## 1. 列表推导式

列表推导式是用简洁的语法创建列表的方式。

### 基本语法
```python
[表达式 for 变量 in 可迭代对象]
```

示例：
```python
squares = [x**2 for x in range(5)]
print(squares)
```

### 带条件的列表推导式
```python
evens = [x for x in range(10) if x % 2 == 0]
print(evens)
```

### 带 if-else 的列表推导式
```python
result = ["偶数" if x % 2 == 0 else "奇数" for x in range(5)]
print(result)
```

---

## 2. 嵌套列表推导式

```python
matrix = [[j for j in range(3)] for i in range(3)]
print(matrix)

flat = [x for row in matrix for x in row]
print(flat)
```

---

## 3. 字典推导式

```python
names = ["张三", "李四", "王五"]
name_dict = {name: len(name) for name in names}
print(name_dict)
```

---

## 4. 集合推导式

```python
numbers = [1, 2, 2, 3, 3, 3, 4]
unique = {x for x in numbers}
print(unique)
```

---

## 5. 生成器表达式

生成器表达式语法类似列表推导式，但使用圆括号：

```python
gen = (x**2 for x in range(5))
print(gen)
for value in gen:
    print(value)
```

**区别**：列表推导式立即生成所有元素，生成器表达式惰性生成，节省内存。

---

## 6. 生成器函数

使用 `yield` 关键字定义生成器函数：

```python
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

for num in count_up(5):
    print(num)
```

每次调用 `yield` 会暂停函数并返回值，下次调用从暂停处继续。

---

## 7. 生成器方法

| 方法 | 说明 |
|------|------|
| `next(gen)` | 获取下一个值 |
| `gen.send(value)` | 发送值到生成器 |
| `gen.close()` | 关闭生成器 |

---

## 8. 为什么使用生成器

- **节省内存**：惰性计算，不一次性生成所有数据
- **处理大数据**：适合处理大文件或无限序列
- **管道操作**：可以链式处理数据

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num, end=" ")
```

---

## 9. 示例文件

请查看并运行以下示例文件：
- `list_comprehension.py` - 列表推导式详解
- `dict_set_comprehension.py` - 字典和集合推导式
- `generator_demo.py` - 生成器示例

---

## 练习题

1. 使用列表推导式生成 1-100 中所有能被 3 整除的数
2. 使用字典推导式将列表 `['a', 'b', 'c']` 转换为 `{0: 'a', 1: 'b', 2: 'c'}`
3. 编写一个生成器函数，无限生成斐波那契数列

---

## 上一章 | 下一章

[第九章：模块与包](../09_模块与包/README.md) | [第十一章：迭代器](../11_迭代器/README.md)
