# 1. 虚拟环境

## 为什么需要虚拟环境

不同项目可能依赖同一个包的不同版本：
```
项目A → Django 3.2
项目B → Django 5.0
```
系统只能装一个版本，虚拟环境让每个项目有独立的包空间。

类比Java：虚拟环境 ≈ 每个项目有自己的Maven本地仓库。

## venv（推荐，Python内置）

### 创建

```bash
# 在项目目录下创建
python -m venv .venv
```

> 约定用 `.venv` 作为目录名（带点号，隐藏目录）

### 激活

```bash
# Windows (CMD)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Git Bash)
source .venv/Scripts/activate

# Linux / Mac
source .venv/bin/activate
```

激活后命令行前面会出现 `(.venv)` 标识。

### 退出

```bash
deactivate
```

### 删除

直接删除 `.venv` 目录即可。

## 虚拟环境目录结构

```
.venv/
├── Include/           # C头文件
├── Lib/               # 安装的包
│   └── site-packages/ # 第三方包都在这里
├── Scripts/           # Windows可执行文件
│   ├── activate       # 激活脚本
│   ├── python.exe     # Python解释器
│   └── pip.exe        # pip
└── pyvenv.cfg         # 配置文件
```

## 重要规则

1. **不要把 `.venv` 提交到Git** — 在 `.gitignore` 中加入 `.venv/`
2. **每个项目一个虚拟环境** — 隔离依赖
3. **用 `requirements.txt` 记录依赖** — 别人用它重建环境
4. **激活后再装包** — 确保包装到虚拟环境里

## 验证是否在虚拟环境中

```bash
# 看Python路径是否指向.venv
which python    # Linux/Mac
where python    # Windows
```

```python
import sys
print(sys.prefix)  # 如果是.venv路径，说明在虚拟环境中
```
