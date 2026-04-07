"""
1. 虚拟环境 - 代码示例
演示如何用代码检查和管理虚拟环境。
"""

import sys
import os
import subprocess


# ============================================================
# 1. 检查是否在虚拟环境中
# ============================================================
def check_venv():
    """检查当前是否在虚拟环境中"""
    in_venv = sys.prefix != sys.base_prefix
    print(f"当前Python: {sys.executable}")
    print(f"sys.prefix: {sys.prefix}")
    print(f"sys.base_prefix: {sys.base_prefix}")
    print(f"在虚拟环境中: {'是' if in_venv else '否'}")
    return in_venv


# ============================================================
# 2. 查看Python和pip路径
# ============================================================
def show_paths():
    """显示关键路径信息"""
    import site
    print(f"\nPython版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"包安装路径: {site.getsitepackages()}")
    print(f"用户包路径: {site.getusersitepackages()}")


# ============================================================
# 3. 列出已安装的包
# ============================================================
def list_packages():
    """用代码列出已安装的包"""
    import pkg_resources
    packages = sorted(pkg_resources.working_set, key=lambda p: p.key)
    print(f"\n已安装 {len(packages)} 个包:")
    for pkg in packages[:10]:
        print(f"  {pkg.key:30s} {pkg.version}")
    if len(packages) > 10:
        print(f"  ... 还有 {len(packages) - 10} 个")


# ============================================================
# 4. 用代码创建虚拟环境
# ============================================================
def create_venv_demo():
    """演示用代码创建虚拟环境"""
    import venv

    venv_path = ".demo_venv"
    if os.path.exists(venv_path):
        print(f"\n虚拟环境已存在: {venv_path}")
    else:
        print(f"\n创建虚拟环境: {venv_path}")
        venv.create(venv_path, with_pip=True)
        print("创建完成")

    # 显示结构
    if os.path.exists(venv_path):
        print(f"\n{venv_path}/ 目录内容:")
        for item in os.listdir(venv_path):
            print(f"  {item}/")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("1. 检查虚拟环境")
    print("=" * 50)
    check_venv()

    print("\n" + "=" * 50)
    print("2. 路径信息")
    print("=" * 50)
    show_paths()

    print("\n" + "=" * 50)
    print("3. 已安装的包")
    print("=" * 50)
    list_packages()
