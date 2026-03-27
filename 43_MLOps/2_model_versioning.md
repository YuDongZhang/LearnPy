# 2. 模型版本管理

## 需要版本化的东西

| 对象 | 工具 | 说明 |
|------|------|------|
| 代码 | Git | 训练脚本、配置 |
| 数据 | DVC | 训练数据、测试数据 |
| 模型 | MLflow | 模型文件、权重 |
| Prompt | Git | System Prompt、模板 |
| 配置 | Git | 超参数、环境配置 |

## MLflow

最流行的ML实验管理平台：
- 实验追踪（参数、指标、产物）
- 模型注册（版本管理、状态流转）
- 模型部署（REST API）

### 核心概念
- Experiment：一组相关的训练运行
- Run：一次训练运行
- Artifact：训练产物（模型文件等）
- Model Registry：模型注册中心

### 模型状态流转
```
None → Staging → Production → Archived
```

## DVC（Data Version Control）

Git管不了大文件，DVC专门管理数据和模型文件：
```bash
dvc init
dvc add data/train.json
git add data/train.json.dvc
git commit -m "add training data v1"
```

## Weights & Biases（W&B）

云端实验追踪平台：
- 自动记录训练曲线
- 超参数对比
- 团队协作
- 可视化丰富
