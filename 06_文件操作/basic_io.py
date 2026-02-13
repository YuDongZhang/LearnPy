"""
基本文件读写
============

使用 open() 函数打开文件。
推荐使用 with 语句，自动处理文件关闭。
"""

import os

print("=" * 40)
print("1. 写入文件")
print("=" * 40)

file_path = "d:\\project\\LearnPy\\06_文件操作\\demo.txt"

with open(file_path, "w", encoding="utf-8") as f:
    f.write("第一行内容\n")
    f.write("第二行内容\n")
    f.write("第三行内容\n")

print(f"文件已写入: {file_path}")

print()
print("=" * 40)
print("2. 读取文件 - read()")
print("=" * 40)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print("读取全部内容:")
    print(content)

print("-" * 40)

print("读取指定字符数:")
with open(file_path, "r", encoding="utf-8") as f:
    partial = f.read(10)
    print(f"前10个字符: '{partial}'")

print()
print("=" * 40)
print("3. 读取文件 - readline()")
print("=" * 40)

with open(file_path, "r", encoding="utf-8") as f:
    print("逐行读取:")
    line1 = f.readline()
    line2 = f.readline()
    print(f"第1行: {line1.strip()}")
    print(f"第2行: {line2.strip()}")

print()
print("=" * 40)
print("4. 读取文件 - readlines()")
print("=" * 40)

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"读取为列表 (共{len(lines)}行):")
    for i, line in enumerate(lines, 1):
        print(f"  {i}: {line.strip()}")

print()
print("=" * 40)
print("5. 逐行遍历")
print("=" * 40)

print("最常用的读取方式:")
with open(file_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.strip()}")

print()
print("=" * 40)
print("6. 追加内容")
print("=" * 40)

with open(file_path, "a", encoding="utf-8") as f:
    f.write("追加的第一行\n")
    f.write("追加的第二行\n")

print("已追加内容，读取验证:")
with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())

print()
print("=" * 40)
print("7. 写入多行")
print("=" * 40)

new_file = "d:\\project\\LearnPy\\06_文件操作\\demo2.txt"
lines_to_write = [
    "Python 是一门优雅的语言\n",
    "它简洁而强大\n",
    "适合初学者学习\n"
]

with open(new_file, "w", encoding="utf-8") as f:
    f.writelines(lines_to_write)

print(f"已写入多行到: {new_file}")

print()
print("=" * 40)
print("8. 文件指针")
print("=" * 40)

with open(file_path, "r", encoding="utf-8") as f:
    print(f"初始位置: {f.tell()}")
    
    content = f.read(5)
    print(f"读取5个字符后位置: {f.tell()}")
    
    f.seek(0)
    print(f"seek(0) 后位置: {f.tell()}")
    
    first_char = f.read(1)
    print(f"第一个字符: '{first_char}'")

print()
print("=" * 40)
print("9. 检查文件是否存在")
print("=" * 40)

if os.path.exists(file_path):
    print(f"文件存在: {file_path}")
    print(f"文件大小: {os.path.getsize(file_path)} 字节")
else:
    print("文件不存在")

print()
print("=" * 40)
print("10. 清理演示文件")
print("=" * 40)

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"已删除: {file_path}")

if os.path.exists(new_file):
    os.remove(new_file)
    print(f"已删除: {new_file}")
