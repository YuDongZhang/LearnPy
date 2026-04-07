"""
4. 现代工具 - 代码示例
演示uv和poetry的命令速查，以及工具检测。
"""

import shutil
import subprocess


# ============================================================
# 1. 检测已安装的工具
# ============================================================
def detect_tools():
    """检测系统中安装了哪些Python包管理工具"""
    tools = {
        "pip": "pip --version",
        "uv": "uv --version",
        "poetry": "poetry --version",
        "conda": "conda --version",
        "pipenv": "pipenv --version",
    }

    print("已安装的工具:")
    for name, cmd in tools.items():
        exe = shutil.which(name)
        if exe:
            try:
                result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
                version = result.stdout.strip() or result.stderr.strip()
                print(f"  ✓ {name:10s} {version}")
            except Exception:
                print(f"  ✓ {name:10s} (已安装)")
        else:
            print(f"  ✗ {name:10s} 未安装")


# ============================================================
# 2. 命令速查表
# ============================================================
def print_cheatsheet():
    """打印各工具的命令对照表"""
    print("\n命令对照表:")
    print(f"{'操作':12s} | {'pip':30s} | {'uv':30s} | {'poetry':25s}")
    print("-" * 105)

    commands = [
        ("安装包", "pip install requests", "uv pip install requests", "poetry add requests"),
        ("卸载包", "pip uninstall requests", "uv pip uninstall requests", "poetry remove requests"),
        ("列出包", "pip list", "uv pip list", "poetry show"),
        ("导出依赖", "pip freeze > req.txt", "uv pip freeze > req.txt", "poetry export"),
        ("从文件装", "pip install -r req.txt", "uv pip install -r req.txt", "poetry install"),
        ("创建环境", "python -m venv .venv", "uv venv", "poetry install"),
        ("升级包", "pip install -U pkg", "uv pip install -U pkg", "poetry update pkg"),
    ]

    for op, pip_cmd, uv_cmd, poetry_cmd in commands:
        print(f"{op:12s} | {pip_cmd:30s} | {uv_cmd:30s} | {poetry_cmd:25s}")


# ============================================================
# 3. 安装建议
# ============================================================
def print_recommendation():
    """打印工具选择建议"""
    print("\n工具选择建议:")
    print("  刚入门        → venv + pip（内置，零配置）")
    print("  追求速度      → uv（pip的10-100倍速度）")
    print("  正式项目      → poetry 或 uv")
    print("  数据科学/AI   → conda（管Python版本+CUDA）")
    print()
    print("安装uv:")
    print("  pip install uv")
    print()
    print("安装poetry:")
    print("  curl -sSL https://install.python-poetry.org | python3 -")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("1. 检测已安装工具")
    print("=" * 50)
    detect_tools()

    print("\n" + "=" * 50)
    print("2. 命令速查表")
    print("=" * 50)
    print_cheatsheet()

    print("\n" + "=" * 50)
    print("3. 选择建议")
    print("=" * 50)
    print_recommendation()
