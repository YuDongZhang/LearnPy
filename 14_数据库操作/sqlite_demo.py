"""
SQLite 数据库操作
================

使用 sqlite3 模块操作 SQLite 数据库。
"""

import sqlite3
import os

db_path = "d:\\project\\LearnPy\\14_数据库操作\\test.db"

print("=" * 40)
print("1. 连接和创建表")
print("=" * 40)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT
)
""")

conn.commit()
print("表创建成功")

print()
print("=" * 40)
print("2. 插入数据")
print("=" * 40)

users = [
    ("张三", 25, "zhangsan@example.com"),
    ("李四", 30, "lisi@example.com"),
    ("王五", 28, "wangwu@example.com"),
]

cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)
conn.commit()
print(f"插入 {cursor.rowcount} 条记录")

print()
print("=" * 40)
print("3. 查询数据")
print("=" * 40)

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print("所有用户:")
for row in rows:
    print(f"  {row}")

print()
print("=" * 40)
print("4. 条件查询")
print("=" * 40)

cursor.execute("SELECT * FROM users WHERE age > ?", (25,))
rows = cursor.fetchall()
print(f"年龄>25的用户: {rows}")

print()
print("=" * 40)
print("5. 更新数据")
print("=" * 40)

cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "张三"))
conn.commit()
print(f"更新 {cursor.rowcount} 条记录")

print()
print("=" * 40)
print("6. 删除数据")
print("=" * 40)

cursor.execute("DELETE FROM users WHERE name = ?", ("王五",))
conn.commit()
print(f"删除 {cursor.rowcount} 条记录")

print()
print("=" * 40)
print("7. 事务")
print("=" * 40)

try:
    cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ("赵六", 35, "zhaoliu@example.com"))
    cursor.execute("UPDATE users SET age = ? WHERE name = ?", (40, "李四"))
    conn.commit()
    print("事务提交成功")
except Exception as e:
    conn.rollback()
    print(f"事务回滚: {e}")

print()
print("=" * 40)
print("8. 清理")
print("=" * 40)

cursor.close()
conn.close()

if os.path.exists(db_path):
    os.remove(db_path)
    print(f"删除数据库: {db_path}")
