"""
pip 包管理演示
=============

pip - Python 包管理器的常用命令和技巧。
"""

print("=" * 50)
print("1. pip 基础命令")
print("=" * 50)

commands = [
    ("pip install package", "安装包"),
    ("pip install package==1.0.0", "安装指定版本"),
    ("pip install package>=1.0.0", "安装最低版本"),
    ("pip uninstall package", "卸载包"),
    ("pip list", "列出已安装的包"),
    ("pip show package", "查看包信息"),
    ("pip search package", "搜索包（已禁用）"),
    ("pip help", "查看帮助"),
]

print("常用命令:")
for cmd, desc in commands:
    print(f"  {cmd:35s} - {desc}")

print()
print("=" * 50)
print("2. requirements.txt")
print("=" * 50)

print("作用：记录项目依赖，方便他人安装")
print("\n生成依赖文件:")
print("  pip freeze > requirements.txt")

print("\n内容示例:")
print("""
Django==3.2.0
requests==2.25.1
numpy==1.20.0
""")

print("\n安装依赖:")
print("  pip install -r requirements.txt")

print("\n安装时排除系统包:")
print("  pip freeze --exclude-system > requirements.txt")

print()
print("=" * 50)
print("3. 依赖版本说明")
print("=" * 50)

print("版本指定方式:")
print("  package==1.0.0     精确版本")
print("  package>=1.0.0     最低版本")
print("  package<=1.0.0     最高版本")
print("  package>=1.0.0,<2.0.0  版本范围")
print("  package~=1.0.0     兼容版本（1.0.x）")

print("\n语义版本 (Semantic Versioning):")
print("  1.0.0 -> major.minor.patch")
print("  major  - 不兼容的API变化")
print("  minor  - 向后兼容的新功能")
print("  patch  - 向后兼容的bug修复")

print()
print("=" * 50)
print("4. 升级和降级")
print("=" * 50)

print("升级包:")
print("  pip install --upgrade package")
print("  pip install -U package")

print("\n升级 pip 自身:")
print("  python -m pip install --upgrade pip")

print("\n安装最新版本:")
print("  pip install --upgrade --force-reinstall package")

print()
print("=" * 50)
print("5. pip 镜像源")
print("=" * 50)

print("国内常用镜像源:")
print("  阿里云: https://mirrors.aliyun.com/pypi/simple/")
print("  豆瓣: https://pypi.doubanio.com/simple/")
print("  清华: https://pypi.tuna.tsinghua.edu.cn/simple/")

print("\n临时使用镜像:")
print("  pip install package -i https://mirrors.aliyun.com/pypi/simple/")

print("\n设置为默认镜像:")
print("  pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/")

print()
print("=" * 50)
print("6. 虚拟环境 + pip 最佳实践")
print("=" * 50)

print("""
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 开发项目...

# 5. 更新依赖文件
pip freeze > requirements.txt

# 6. 退出虚拟环境
deactivate
""")

print()
print("=" * 50)
print("7. pipenv (推荐)")
print("=" * 50)

print("pipenv - 结合虚拟环境和pip的工具")
print("""
# 安装 pipenv
pip install pipenv

# 创建项目环境并安装依赖
pipenv install requests

# 开发模式安装
pipenv install -d pytest

# 运行脚本
pipenv run python main.py

# 进入虚拟环境
pipenv shell

# 更新所有依赖
pipenv update

# 生成锁定文件
pipenv lock
""")

print("\npipenv 自动创建:")
print("  Pipfile - 项目依赖声明")
print("  Pipfile.lock - 锁定版本")

print()
print("=" * 50)
print("8. poetry (现代工具)")
print("=" * 50)

print("poetry - 现代化的Python打包和依赖管理工具")
print("""
# 安装 poetry
curl -sS https://install.python-poetry.org | python3 -

# 初始化项目
poetry init

# 添加依赖
poetry add requests
poetry add pytest --dev

# 安装依赖
poetry install

# 构建包
poetry build
""")

print()
print("=" * 50)
print("9. pyproject.toml (现代标准)")
print("=" * 50)

print("PEP 518 引入的构建系统配置")
print("""
[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25"

[tool.poetry.dev-dependencies]
pytest = "^6.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
""")

print()
print("=" * 50)
print("10. 包分发")
print("=" * 50)

print("打包 Python 包:")
print("""
# 安装打包工具
pip install build

# 构建包
python -m build

# 发布到 PyPI
pip install twine
twine upload dist/*
""")

print("\n项目结构:")
print("""
my_package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
├── tests/
├── pyproject.toml
└── README.md
""")

print()
print("=" * 50)
print("11. pip 常用选项")
print("=" * 50)

options = [
    ("-r FILE", "从文件安装依赖"),
    ("-U, --upgrade", "升级包"),
    ("--force-reinstall", "强制重装"),
    ("--no-cache-dir", "不使用缓存"),
    ("-q, --quiet", "安静模式"),
    ("-v, --verbose", "详细输出"),
    ("--dry-run", "模拟安装"),
    ("--user", "安装到用户目录"),
]

print("常用选项:")
for opt, desc in options:
    print(f"  {opt:25s} - {desc}")
