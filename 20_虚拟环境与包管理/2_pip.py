"""
2. pip包管理 - 代码示例
演示用代码调用pip和管理包。
"""

import subprocess
import sys


def run_pip(*args):
    """安全地调用pip命令"""
    cmd = [sys.executable, "-m", "pip"] + list(args)
    print(f"$ pip {' '.join(args)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout[:500])
    if result.returncode != 0 and result.stderr:
        print(f"错误: {result.stderr[:200]}")
    return result.returncode == 0


# ============================================================
# 1. 查看pip版本和配置
# ============================================================
def demo_pip_info():
    """查看pip基本信息"""
    run_pip("--version")
    run_pip("config", "list")


# ============================================================
# 2. 列出已安装的包
# ============================================================
def demo_list():
    """列出包"""
    run_pip("list", "--format=columns")


# ============================================================
# 3. 查看包详情
# ============================================================
def demo_show():
    """查看包详情"""
    run_pip("show", "pip")


# ============================================================
# 4. 检查过期的包
# ============================================================
def demo_outdated():
    """检查哪些包有新版本"""
    run_pip("list", "--outdated", "--format=columns")


# ============================================================
# 5. 导出依赖
# ============================================================
def demo_freeze():
    """导出当前环境的依赖"""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")
    print(f"当前环境有 {len(lines)} 个包:")
    for line in lines[:5]:
        print(f"  {line}")
    if len(lines) > 5:
        print(f"  ... 还有 {len(lines) - 5} 个")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("1. pip信息")
    print("=" * 50)
    demo_pip_info()

    print("\n" + "=" * 50)
    print("2. 已安装的包")
    print("=" * 50)
    demo_list()

    print("\n" + "=" * 50)
    print("3. 包详情")
    print("=" * 50)
    demo_show()

    print("\n" + "=" * 50)
    print("4. 导出依赖")
    print("=" * 50)
    demo_freeze()
