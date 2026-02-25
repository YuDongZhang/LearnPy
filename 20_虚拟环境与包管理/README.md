# 第二十章：虚拟环境与包管理

## 本章目标
- 掌握 Python 虚拟环境的创建和使用
- 学会使用 pip 管理包
- 了解 requirements.txt 和 pyproject.toml
- 掌握包的分发和发布

---

## 1. 为什么需要虚拟环境

- 隔离项目依赖，避免版本冲突
- 方便项目部署
- 保持系统环境干净

---

## 2. venv 虚拟环境

Python 3.3+ 内置的虚拟环境工具：

```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

---

## 3. pip 包管理

Python 的包管理工具：

```bash
pip install package_name
pip uninstall package_name
pip list
pip freeze > requirements.txt
```

---

## 4. 示例文件

| 文件 | 内容 |
|------|------|
| `venv_demo.py` | 虚拟环境使用演示 |
| `pip_demo.py` | pip 常用命令 |

---

## 5. 章节总结

- **虚拟环境**：venv、virtualenv
- **包管理**：pip、pipenv、poetry
- **依赖管理**：requirements.txt、pyproject.toml

---

## 上一章

[第十八章：测试与调试](../18_测试与调试/README.md)
