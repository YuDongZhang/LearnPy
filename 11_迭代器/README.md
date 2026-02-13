# 第十一章：迭代器

## 本章目标
- 理解迭代器的概念
- 掌握 `__iter__` 和 `__next__` 方法
- 学会创建自定义迭代器
- 理解可迭代对象与迭代器的区别

---

## 1. 什么是迭代器

迭代器是一个可以记住遍历位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有元素被访问完结束。

**特点：**
- 只能往前不会后退
- 惰性计算，节省内存
- 实现了 `__iter__` 和 `__next__` 方法

---

## 2. 可迭代对象 vs 迭代器

| 类型 | 说明 | 方法 |
|------|------|------|
| 可迭代对象 | 可以被遍历的对象 | `__iter__` |
| 迭代器 | 可以不断返回下一个值的对象 | `__iter__` + `__next__` |

```python
my_list = [1, 2, 3]
print(iter(my_list))
```

列表本身不是迭代器，但可以通过 `iter()` 函数获取其迭代器。

---

## 3. 手动使用迭代器

```python
my_list = [1, 2, 3]
my_iter = iter(my_list)

print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
```

当没有更多元素时，`next()` 会抛出 `StopIteration` 异常。

---

## 4. 创建自定义迭代器

通过实现 `__iter__` 和 `__next__` 方法：

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for num in CountDown(5):
    print(num)
```

---

## 5. 迭代器的优势

- **节省内存**：不需要一次性存储所有数据
- **惰性计算**：只在需要时计算下一个值
- **无限序列**：可以表示无限的数据流

---

## 6. 常见迭代器函数

| 函数 | 说明 |
|------|------|
| `iter(obj)` | 获取对象的迭代器 |
| `next(it)` | 获取下一个值 |
| `enumerate()` | 带索引的迭代 |
| `zip()` | 并行迭代 |
| `map()` | 映射迭代 |
| `filter()` | 过滤迭代 |

---

## 7. 示例文件

请查看并运行以下示例文件：
- `iterator_basics.py` - 迭代器基础
- `custom_iterator.py` - 自定义迭代器
- `iterator_tools.py` - 迭代器工具

---

## 练习题

1. 创建一个迭代器，返回 1 到 n 的平方数
2. 创建一个迭代器，无限循环返回列表中的元素
3. 使用 `enumerate` 和 `zip` 实现两个列表的并行遍历（带索引）

---

## 上一章 | 下一章

[第十章：列表推导式与生成器](../10_列表推导式与生成器/README.md) | [第十二章：装饰器](../12_装饰器/README.md)
