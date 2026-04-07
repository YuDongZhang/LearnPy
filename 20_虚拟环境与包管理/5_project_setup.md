# 5. 项目环境搭建实战

## 场景：从零搭建一个Python项目

### 方案A：venv + pip（最基础）

```bash
# 1. 创建项目目录
mkdir my-project && cd my-project

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 4. 安装依赖
pip install requests flask

# 5. 导出依赖
pip freeze > requirements.txt

# 6. 创建.gitignore
echo ".venv/" > .gitignore
```

### 方案B：uv（推荐）

```bash
# 1. 初始化项目
uv init my-project && cd my-project

# 2. 添加依赖
uv add requests flask

# 3. 运行
uv run python main.py
```

### 方案C：poetry

```bash
# 1. 创建项目
poetry new my-project && cd my-project

# 2. 添加依赖
poetry add requests flask
poetry add pytest --group dev

# 3. 运行
poetry run python main.py
```

## 项目结构模板

```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── .venv/              # 不提交到Git
├── .gitignore
├── pyproject.toml      # 或 requirements.txt
└── README.md
```

## .gitignore模板

```
# 虚拟环境
.venv/
venv/
env/

# Python缓存
__pycache__/
*.pyc
*.pyo

# IDE
.idea/
.vscode/
*.swp

# 构建产物
dist/
build/
*.egg-info/

# 环境变量
.env
```

## 团队协作流程

```
开发者A：
  1. 创建项目 + 虚拟环境
  2. 安装依赖
  3. 导出 requirements.txt / poetry.lock
  4. 提交到Git

开发者B：
  1. git clone
  2. 创建虚拟环境
  3. pip install -r requirements.txt（或 poetry install）
  4. 开始开发
```
