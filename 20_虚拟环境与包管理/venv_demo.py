"""
虚拟环境演示
============

Python 虚拟环境的创建和使用。
"""

print("=" * 50)
print("1. 什么是虚拟环境")
print("=" * 50)

print("虚拟环境的作用:")
print("  - 隔离项目依赖")
print("  - 避免包版本冲突")
print("  - 方便在不同项目间切换")

print("\n不使用虚拟环境的问题:")
print("  项目A需要Django 2.x")
print("  项目B需要Django 3.x")
print("  系统只有一个Django版本，无法同时满足")

print()
print("=" * 50)
print("2. 创建虚拟环境")
print("=" * 50)

print("方法一：使用 venv (Python 3.3+ 推荐)")
print("-" * 30)
print("""
# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境
# Windows:
myenv\\Scripts\\activate
# Linux/Mac:
source myenv/bin/activate

# 退出虚拟环境
deactivate
""")

print("\n方法二：使用 virtualenv")
print("-" * 30)
print("""
# 安装 virtualenv
pip install virtualenv

# 创建虚拟环境
virtualenv myenv

# 激活
source myenv/bin/activate  # Linux/Mac
myenv\\Scripts\\activate   # Windows
""")

print()
print("=" * 50)
print("3. 虚拟环境常用操作")
print("=" * 50)

print("查看虚拟环境中的包:")
print("  pip list")

print("\n导出依赖:")
print("  pip freeze > requirements.txt")

print("\n从文件安装:")
print("  pip install -r requirements.txt")

print("\n查看虚拟环境位置:")
print("  which python  # Linux/Mac")
print("  where python  # Windows")

print()
print("=" * 50)
print("4. venv 结构")
print("=" * 50)

print("""
myenv/
├── Include/          # C头文件
├── Lib/              # 安装的包
│   └── site-packages/
├── Scripts/          # 可执行文件 (Windows)
│   ├── activate
│   ├── python.exe
│   └── pip.exe
├── bin/              # 可执行文件 (Linux/Mac)
│   ├── activate
│   ├── python3
│   └── pip
└── pyvenv.cfg       # 配置文件
""")

print()
print("=" * 50)
print("5. 使用虚拟环境的好处")
print("=" * 50)

benefits = [
    ("隔离依赖", "每个项目有独立的包环境"),
    ("版本控制", "不同项目使用不同版本的同一包"),
    ("干净环境", "不影响系统Python环境"),
    ("方便协作", "他人可以用requirements.txt复现环境"),
]

for benefit, desc in benefits:
    print(f"  ✓ {benefit}: {desc}")

print()
print("=" * 50)
print("6. pyenv (Linux/Mac)")
print("=" * 50)

print("pyenv - Python 版本管理工具")
print("""
# 安装 pyenv
curl https://pyenv.run | bash

# 安装 Python 版本
pyenv install 3.11.0

# 切换版本
pyenv global 3.11.0
pyenv local 3.10.0

# 查看已安装版本
pyenv versions
""")

print()
print("=" * 50)
print("7. conda 环境管理")
print("=" * 50)

print("Anaconda/Miniconda 提供的环境管理")
print("""
# 创建环境
conda create -n myenv python=3.11

# 激活环境
conda activate myenv

# 退出环境
conda deactivate

# 查看环境
conda env list

# 导出环境
conda env export > environment.yml

# 从文件创建
conda env create -f environment.yml
""")

print()
print("=" * 50)
print("8. 最佳实践")
print("=" * 50)

practices = [
    "为每个项目创建独立的虚拟环境",
    "在项目根目录创建 .gitignore 排除 venv/ 或 env/",
    "使用 requirements.txt 记录依赖",
    "不要把虚拟环境提交到版本库",
    "使用 pip-compile 生成确定性依赖",
]

print("建议:")
for i, practice in enumerate(practices, 1):
    print(f"  {i}. {practice}")

print("\n.gitignore 示例:")
print("""
# 虚拟环境
venv/
env/
myenv/

# 依赖文件（可选）
# requirements.txt 应该提交
""")
