# 第十四章：数据库操作

## 本章目标
- 理解 SQLite 数据库
- 掌握基本 SQL 语句
- 学会 Python 操作 SQLite

---

## 1. SQLite

SQLite 是轻量级嵌入式数据库。

---

## 2. 基本操作

```python
import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
```

---

## 上一章 | 下一章

[第十三章：正则表达式](../13_正则表达式/README.md) | [第十五章：网络请求](../15_网络请求/README.md)
