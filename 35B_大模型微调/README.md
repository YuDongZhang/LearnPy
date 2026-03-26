# 第35B章：大模型微调（Fine-tuning）

## 本章目标

- 理解大模型微调的概念和应用场景
- 掌握主流微调方法（全量微调、LoRA、QLoRA、P-Tuning）
- 学会使用Hugging Face生态进行微调
- 掌握数据集准备和训练流程
- 了解微调工具（LLaMA-Factory、Unsloth）
- 动手完成微调实战项目

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 内容 |
|------|----------|----------|------|
| 1 | 1_finetune_overview.md | 1_finetune_overview.py | 微调概述与方法对比 |
| 2 | 2_dataset_preparation.md | 2_dataset_preparation.py | 数据集准备与处理 |
| 3 | 3_full_finetune.md | 3_full_finetune.py | 全量微调 |
| 4 | 4_lora.md | 4_lora.py | LoRA与QLoRA微调 |
| 5 | 5_peft_methods.md | 5_peft_methods.py | 其他PEFT方法 |
| 6 | 6_training_tips.md | 6_training_tips.py | 训练技巧与调优 |
| 7 | 7_finetune_tools.md | 7_finetune_tools.py | 微调工具实战 |
| 8 | 8_finetune_project.md | 8_finetune_project.py | 微调实战项目 |

## 学习路径

1. 先读 md 了解概念，再看对应 py 代码
2. 建议按编号顺序学习
3. 第4节（LoRA）是重点，务必掌握
4. 第8节为综合实战，建议前7节学完再看

## 前置知识

- Python基础
- 深度学习入门（第31章）
- 生成式AI与LLM（第35章）

## 安装依赖

```bash
pip install torch transformers datasets peft accelerate
pip install bitsandbytes  # 量化支持
pip install trl            # 训练工具
pip install wandb          # 训练监控（可选）
```

## 硬件要求

| 微调方法 | 最低显存 | 推荐显存 |
|---------|---------|---------|
| 全量微调(7B) | 60GB+ | 80GB(A100) |
| LoRA(7B) | 16GB | 24GB |
| QLoRA(7B) | 6GB | 12GB |
| QLoRA(13B) | 12GB | 24GB |

> 没有GPU也可以学习，代码中提供了小模型和CPU模式的示例。

## 章节导航

[上一章：生成式AI与LLM](../35_生成式AI与LLM/README.md) | [下一章：LLM Agent](../36_LLM_Agent/README.md)
