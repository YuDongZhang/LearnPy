"""
文件模式详解
============

open() 函数的第二个参数指定文件模式。
不同模式决定文件的读写方式和行为。
"""

import os

demo_dir = "d:\\project\\LearnPy\\06_文件操作"

print("=" * 40)
print("1. 读取模式 'r'")
print("=" * 40)

file_path = os.path.join(demo_dir, "mode_r.txt")

with open(file_path, "w", encoding="utf-8") as f:
    f.write("测试内容")

with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())

print("特点: 只能读取，文件必须存在")

print()
print("=" * 40)
print("2. 写入模式 'w'")
print("=" * 40)

file_path = os.path.join(demo_dir, "mode_w.txt")

with open(file_path, "w", encoding="utf-8") as f:
    f.write("新内容")

print("特点: 覆盖写入，文件不存在则创建")

with open(file_path, "r", encoding="utf-8") as f:
    print(f"内容: {f.read()}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write("再次写入会覆盖")

with open(file_path, "r", encoding="utf-8") as f:
    print(f"覆盖后: {f.read()}")

print()
print("=" * 40)
print("3. 追加模式 'a'")
print("=" * 40)

file_path = os.path.join(demo_dir, "mode_a.txt")

with open(file_path, "w", encoding="utf-8") as f:
    f.write("初始内容\n")

with open(file_path, "a", encoding="utf-8") as f:
    f.write("追加内容1\n")
    f.write("追加内容2\n")

print("特点: 在文件末尾追加，不覆盖原有内容")

with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())

print()
print("=" * 40)
print("4. 创建模式 'x'")
print("=" * 40)

file_path = os.path.join(demo_dir, "mode_x.txt")

try:
    with open(file_path, "x", encoding="utf-8") as f:
        f.write("新创建的文件")
    print(f"文件创建成功: {file_path}")
except FileExistsError:
    print("文件已存在，无法创建")

print("特点: 创建新文件，文件存在则报错")

print()
print("=" * 40)
print("5. 读写模式 '+'")
print("=" * 40)

file_path = os.path.join(demo_dir, "mode_plus.txt")

with open(file_path, "w+", encoding="utf-8") as f:
    f.write("Hello World")
    f.seek(0)
    content = f.read()
    print(f"写入后读取: {content}")

print("w+: 写入 + 读取，会覆盖原文件")

print("-" * 40)

with open(file_path, "r+", encoding="utf-8") as f:
    content = f.read()
    print(f"原内容: {content}")
    f.seek(0)
    f.write("Hi")

with open(file_path, "r", encoding="utf-8") as f:
    print(f"修改后: {f.read()}")

print("r+: 读取 + 写入，文件必须存在")

print()
print("=" * 40)
print("6. 二进制模式 'b'")
print("=" * 40)

file_path = os.path.join(demo_dir, "mode_binary.bin")

data = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])

with open(file_path, "wb") as f:
    f.write(data)

with open(file_path, "rb") as f:
    content = f.read()
    print(f"二进制内容: {content}")
    print(f"解码后: {content.decode('utf-8')}")

print("特点: 用于处理图片、视频等二进制文件")

print()
print("=" * 40)
print("7. 模式组合")
print("=" * 40)

print("常用组合:")
print("  'r'  - 只读")
print("  'w'  - 写入（覆盖）")
print("  'a'  - 追加")
print("  'r+' - 读写（文件需存在）")
print("  'w+' - 读写（覆盖）")
print("  'a+' - 读写（追加）")
print("  'rb' - 二进制读取")
print("  'wb' - 二进制写入")

print()
print("=" * 40)
print("8. 清理演示文件")
print("=" * 40)

files_to_clean = [
    "mode_r.txt", "mode_w.txt", "mode_a.txt",
    "mode_x.txt", "mode_plus.txt", "mode_binary.bin"
]

for filename in files_to_clean:
    file_path = os.path.join(demo_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"已删除: {filename}")
