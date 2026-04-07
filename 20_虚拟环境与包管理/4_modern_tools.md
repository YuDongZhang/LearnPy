# 4. 现代工具

## 工具对比

| 工具 | 定位 | 特点 | 推荐度 |
|------|------|------|--------|
| venv + pip | 内置基础方案 | 简单，人人都有 | 入门推荐 |
| uv | pip的替代品 | 极快（Rust写的），兼容pip | 强烈推荐 |
| poetry | 全功能包管理 | 依赖解析好，发布方便 | 正式项目推荐 |
| conda | 科学计算环境 | 管Python版本+非Python依赖 | 数据科学推荐 |
| pipenv | pip+venv整合 | 曾经流行，现在不太推荐 | 一般 |

## uv（2024年新星，强烈推荐）

Rust编写的Python包管理器，比pip快10-100倍。

### 安装
```bash
pip install uv
# 或
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 使用（兼容pip命令）
```bash
uv pip install requests          # 安装包
uv pip install -r requirements.txt  # 从文件安装
uv pip freeze                    # 导出依赖
uv venv                         # 创建虚拟环境
```

### uv项目管理
```bash
uv init my-project    # 初始化项目
uv add requests       # 添加依赖
uv remove requests    # 移除依赖
uv sync               # 同步环境
uv run python main.py # 在项目环境中运行
```

## poetry

全功能的Python包管理和发布工具。

### 安装
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 使用
```bash
poetry new my-project     # 创建项目
poetry init               # 在已有项目初始化
poetry add requests       # 添加依赖
poetry add pytest --group dev  # 添加开发依赖
poetry install            # 安装所有依赖
poetry run python main.py # 运行
poetry build              # 构建包
poetry publish            # 发布到PyPI
```

### poetry生成的文件
- `pyproject.toml` — 项目配置和依赖声明
- `poetry.lock` — 锁定的完整依赖（提交到Git）

## conda

Anaconda/Miniconda提供的环境管理，特点是能管理Python版本和非Python依赖（如CUDA）。

### 使用
```bash
conda create -n myenv python=3.11  # 创建环境+指定Python版本
conda activate myenv               # 激活
conda install numpy pandas         # 安装包
conda deactivate                   # 退出
conda env list                     # 列出环境
conda env export > environment.yml # 导出
conda env create -f environment.yml # 从文件创建
```

### 什么时候用conda
- 需要管理Python版本
- 需要安装CUDA/cuDNN等非Python依赖
- 做数据科学/机器学习

## 选择建议

```
刚入门 → venv + pip（内置，零配置）
追求速度 → uv（pip的完美替代）
正式项目 → poetry 或 uv
数据科学/AI → conda
```
