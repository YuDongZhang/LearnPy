"""
5. 项目环境搭建实战 - 代码示例
一键生成项目骨架：目录结构 + .gitignore + pyproject.toml
"""

import os


# ============================================================
# 项目骨架生成器
# ============================================================
def create_project(name: str = "my_project"):
    """创建一个标准Python项目骨架"""
    dirs = [
        f"{name}/src/{name}",
        f"{name}/tests",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # __init__.py
    with open(f"{name}/src/{name}/__init__.py", "w") as f:
        f.write(f'"""{ name} package."""\n\n__version__ = "0.1.0"\n')

    # main.py
    with open(f"{name}/src/{name}/main.py", "w") as f:
        f.write('def main():\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n')

    # test
    with open(f"{name}/tests/test_main.py", "w") as f:
        f.write(f'from {name}.main import main\n\ndef test_main():\n    main()  # 不报错即通过\n')

    # .gitignore
    gitignore = """.venv/
venv/
__pycache__/
*.pyc
*.pyo
dist/
build/
*.egg-info/
.env
.idea/
.vscode/
"""
    with open(f"{name}/.gitignore", "w") as f:
        f.write(gitignore)

    # pyproject.toml
    pyproject = f"""[project]
name = "{name}"
version = "0.1.0"
description = ""
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.pytest.ini_options]
testpaths = ["tests"]
"""
    with open(f"{name}/pyproject.toml", "w") as f:
        f.write(pyproject)

    # README
    with open(f"{name}/README.md", "w") as f:
        f.write(f"# {name}\n\n## 快速开始\n\n```bash\npython -m venv .venv\nsource .venv/bin/activate\npip install -e .[dev]\npytest\n```\n")

    # 打印结构
    print(f"项目 {name}/ 已创建:")
    for root, dirs, files in os.walk(name):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        level = root.replace(name, "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        for file in files:
            print(f"{indent}  {file}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    project_name = input("项目名称（回车使用demo_project）: ").strip() or "demo_project"
    create_project(project_name)
    print(f"\n下一步:")
    print(f"  cd {project_name}")
    print(f"  python -m venv .venv")
    print(f"  source .venv/bin/activate  # Linux/Mac")
    print(f"  .venv\\Scripts\\activate     # Windows")
    print(f"  pip install -e .[dev]")
    print(f"  pytest")
