# 3. 依赖管理

## requirements.txt

Python项目的依赖清单，类比Java的 `pom.xml` 或 `build.gradle`。

### 生成

```bash
pip freeze > requirements.txt
```

### 内容示例

```
requests==2.31.0
numpy==1.26.0
pandas==2.1.0
flask>=3.0.0
```

### 从文件安装

```bash
pip install -r requirements.txt
```

## 问题：pip freeze的缺陷

`pip freeze` 会导出所有包（包括依赖的依赖），导致：
- 文件很长，分不清哪些是直接依赖
- 升级一个包可能需要手动调整多个版本

## 更好的方案：手动维护 + pip-compile

### 手动维护 requirements.in

只写直接依赖：
```
# requirements.in
requests
flask
numpy
```

### 用pip-compile锁定版本

```bash
pip install pip-tools
pip-compile requirements.in  # 生成requirements.txt（含所有依赖和精确版本）
pip-sync requirements.txt    # 安装并同步环境
```

## pyproject.toml（现代标准）

PEP 518/621定义的项目配置文件，一个文件管所有：

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31",
    "flask>=3.0",
]

[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"
```

## 依赖管理最佳实践

1. 直接依赖写在 `requirements.in` 或 `pyproject.toml`
2. 用工具锁定完整依赖（pip-compile / poetry lock）
3. 锁定文件提交到Git
4. CI/CD中用锁定文件安装，确保一致性
