"""
3. 依赖管理 - 代码示例
演示requirements.txt的生成、解析和pyproject.toml的生成。
"""

import subprocess
import sys


# ============================================================
# 1. 生成requirements.txt
# ============================================================
def generate_requirements():
    """生成requirements.txt"""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True, text=True
    )
    with open("requirements.txt", "w") as f:
        f.write(result.stdout)
    lines = result.stdout.strip().split("\n")
    print(f"已生成 requirements.txt ({len(lines)} 个包)")


# ============================================================
# 2. 解析requirements.txt
# ============================================================
def parse_requirements(filepath: str = "requirements.txt"):
    """解析requirements.txt，提取包名和版本"""
    try:
        with open(filepath) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{filepath} 不存在，先运行 generate_requirements()")
        return []

    packages = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            packages.append({"name": name, "version": version})
        else:
            packages.append({"name": line, "version": "any"})

    print(f"解析到 {len(packages)} 个依赖:")
    for pkg in packages[:5]:
        print(f"  {pkg['name']:30s} {pkg['version']}")
    return packages


# ============================================================
# 3. 生成pyproject.toml模板
# ============================================================
def generate_pyproject(project_name: str = "my-project"):
    """生成pyproject.toml模板"""
    content = f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "My Python project"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black",
    "ruff",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
'''
    with open("pyproject.toml", "w") as f:
        f.write(content)
    print(f"已生成 pyproject.toml")
    print(content)


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("1. 生成requirements.txt")
    print("=" * 50)
    generate_requirements()

    print("\n" + "=" * 50)
    print("2. 解析requirements.txt")
    print("=" * 50)
    parse_requirements()

    print("\n" + "=" * 50)
    print("3. 生成pyproject.toml")
    print("=" * 50)
    generate_pyproject()
