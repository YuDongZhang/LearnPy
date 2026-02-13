# 第六章：文件操作

## 本章目标
- 掌握文件的读写操作
- 理解文件打开模式
- 学会处理文件路径
- 掌握 JSON 和 CSV 文件处理

---

## 1. 打开和关闭文件

```python
# 方式1：手动关闭
f = open("test.txt", "r", encoding="utf-8")
content = f.read()
f.close()

# 方式2：使用 with 语句（推荐）
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

---

## 2. 文件打开模式

| 模式 | 说明 |
|------|------|
| `r` | 只读（默认） |
| `w` | 写入（覆盖） |
| `a` | 追加 |
| `x` | 创建新文件 |
| `b` | 二进制模式 |
| `+` | 读写模式 |

---

## 3. 读取文件

```python
# 读取全部
content = f.read()

# 读取一行
line = f.readline()

# 读取所有行为列表
lines = f.readlines()

# 逐行遍历
for line in f:
    print(line)
```

---

## 4. 写入文件

```python
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.writelines(["Line1\n", "Line2\n"])
```

---

## 5. 示例文件

- `basic_io.py` - 基本读写操作
- `file_modes.py` - 文件模式详解
- `json_demo.py` - JSON 文件处理
- `csv_demo.py` - CSV 文件处理
- `path_demo.py` - 文件路径操作

---

## 上一章 | 下一章

[第五章：数据结构](../05_数据结构/README.md) | [第七章：异常处理](../07_异常处理/README.md)
