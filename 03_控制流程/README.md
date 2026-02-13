# 第三章：控制流程

## 本章目标
- 掌握 if 条件判断
- 学会使用 for 循环
- 学会使用 while 循环
- 理解 break 和 continue

---

## 1. 条件判断 (if)

根据条件执行不同的代码：

```python
age = 18

if age >= 18:
    print("成年人")
else:
    print("未成年人")
```

### if-elif-else 结构
```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

---

## 2. for 循环

遍历序列中的每个元素：

```python
for i in range(5):
    print(i)  # 输出 0, 1, 2, 3, 4
```

### 遍历列表
```python
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(fruit)
```

---

## 3. while 循环

当条件为真时重复执行：

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

---

## 4. break 和 continue

- `break`: 跳出整个循环
- `continue`: 跳过本次循环，继续下一次

```python
for i in range(10):
    if i == 5:
        break  # 到5就停止
    print(i)
```

---

## 5. 示例文件

请查看并运行以下示例文件：
- `if_statement.py` - 条件判断示例
- `for_loop.py` - for 循环示例
- `while_loop.py` - while 循环示例
- `break_continue.py` - break 和 continue 示例

---

## 练习题

1. 判断一个数是奇数还是偶数
2. 打印 1 到 100 中所有能被 3 整除的数
3. 使用循环计算 1+2+3+...+100 的和

---

## 上一章 | 下一章

[第二章：数据类型与变量](../02_数据类型与变量/README.md) | [第四章：函数](../04_函数/README.md)
