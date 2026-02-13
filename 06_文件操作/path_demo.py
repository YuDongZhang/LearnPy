"""
文件路径操作
============

使用 os 和 pathlib 模块处理文件路径。
pathlib 是更现代、更推荐的方式。
"""

import os
from pathlib import Path

print("=" * 40)
print("1. os.path 模块")
print("=" * 40)

path = "d:\\project\\LearnPy\\06_文件操作\\test.txt"

print(f"路径: {path}")
print(f"目录名: {os.path.dirname(path)}")
print(f"文件名: {os.path.basename(path)}")
print(f"扩展名: {os.path.splitext(path)[1]}")
print(f"绝对路径: {os.path.abspath('test.txt')}")

print()
print("=" * 40)
print("2. pathlib 模块（推荐）")
print("=" * 40)

p = Path("d:\\project\\LearnPy\\06_文件操作\\test.txt")

print(f"路径: {p}")
print(f"父目录: {p.parent}")
print(f"文件名: {p.name}")
print(f"文件名(无扩展名): {p.stem}")
print(f"扩展名: {p.suffix}")
print(f"所有部分: {p.parts}")

print()
print("=" * 40)
print("3. 路径拼接")
print("=" * 40)

print("os.path.join:")
path1 = os.path.join("d:\\project", "LearnPy", "test.txt")
print(f"  {path1}")

print()
print("Path / 运算符:")
path2 = Path("d:\\project") / "LearnPy" / "test.txt"
print(f"  {path2}")

print()
print("=" * 40)
print("4. 检查路径")
print("=" * 40)

p = Path("d:\\project\\LearnPy")

print(f"路径: {p}")
print(f"是否存在: {p.exists()}")
print(f"是否是文件: {p.is_file()}")
print(f"是否是目录: {p.is_dir()}")

print()
print("=" * 40)
print("5. 创建目录")
print("=" * 40)

new_dir = Path("d:\\project\\LearnPy\\06_文件操作\\test_dir")

new_dir.mkdir(exist_ok=True)
print(f"目录已创建: {new_dir}")

print()
print("=" * 40)
print("6. 遍历目录")
print("=" * 40)

demo_dir = Path("d:\\project\\LearnPy\\06_文件操作")

print("目录中的 .py 文件:")
for file in demo_dir.glob("*.py"):
    print(f"  {file.name}")

print()
print("=" * 40)
print("7. 文件操作")
print("=" * 40)

test_file = Path("d:\\project\\LearnPy\\06_文件操作\\path_test.txt")

test_file.write_text("Hello Path!", encoding="utf-8")
print(f"文件已创建: {test_file}")

content = test_file.read_text(encoding="utf-8")
print(f"文件内容: {content}")

print(f"文件大小: {test_file.stat().st_size} 字节")

test_file.unlink()
print("文件已删除")

print()
print("=" * 40)
print("8. 获取文件信息")
print("=" * 40)

p = Path("d:\\project\\LearnPy\\06_文件操作\\path_demo.py")

if p.exists():
    stat = p.stat()
    print(f"文件: {p.name}")
    print(f"大小: {stat.st_size} 字节")
    import datetime
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
    print(f"修改时间: {mtime}")

print()
print("=" * 40)
print("9. 递归查找文件")
print("=" * 40)

project_dir = Path("d:\\project\\LearnPy")

print("所有 README.md 文件:")
for file in project_dir.rglob("README.md"):
    print(f"  {file.relative_to(project_dir)}")

print()
print("=" * 40)
print("10. 清理")
print("=" * 40)

test_dir = Path("d:\\project\\LearnPy\\06_文件操作\\test_dir")
if test_dir.exists():
    test_dir.rmdir()
    print(f"已删除目录: {test_dir}")
