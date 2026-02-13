# 第五章：数据结构

## 本章目标
- 掌握列表 (List) 的使用
- 掌握元组 (Tuple) 的使用
- 掌握字典 (Dictionary) 的使用
- 掌握集合 (Set) 的使用

---

## 1. 列表 (List)

列表是有序、可变的集合：

```python
fruits = ["苹果", "香蕉", "橙子"]
fruits.append("葡萄")    # 添加元素
fruits[0] = "草莓"       # 修改元素
del fruits[1]            # 删除元素
```

### 常用操作
| 方法 | 说明 |
|------|------|
| append() | 添加元素 |
| insert() | 插入元素 |
| remove() | 删除元素 |
| pop() | 弹出元素 |
| sort() | 排序 |
| reverse() | 反转 |

---

## 2. 元组 (Tuple)

元组是有序、不可变的集合：

```python
point = (3, 4)
x, y = point  # 解包
```

元组一旦创建就不能修改，适合存储不变的数据。

---

## 3. 字典 (Dictionary)

字典是键值对的集合：

```python
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

person["job"] = "工程师"  # 添加
person["age"] = 26        # 修改
del person["city"]        # 删除
```

---

## 4. 集合 (Set)

集合是无序、不重复元素的集合：

```python
numbers = {1, 2, 3, 4, 5}
numbers.add(6)      # 添加
numbers.remove(1)   # 删除
```

集合支持交集、并集、差集运算。

---

## 5. 示例文件

请查看并运行以下示例文件：
- `list_demo.py` - 列表详解
- `tuple_demo.py` - 元组详解
- `dict_demo.py` - 字典详解
- `set_demo.py` - 集合详解

---

## 练习题

1. 创建一个列表，存储你喜欢的5部电影，并实现添加、删除、排序操作
2. 使用字典存储学生信息（姓名、年龄、成绩），并实现查找功能
3. 使用集合找出两个列表的公共元素

---

## 上一章

[第四章：函数](../04_函数/README.md)
