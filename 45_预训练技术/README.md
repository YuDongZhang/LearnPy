# 第四十五章：预训练技术

## 本章目标

- 理解LLM预训练的完整流程
- 掌握训练数据的收集和清洗
- 了解分布式训练技术
- 理解RLHF和DPO对齐技术
- 了解Tokenizer的设计

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 内容 |
|------|----------|----------|------|
| 1 | 1_pretrain_overview.md | 1_pretrain_overview.py | 预训练流程概述 |
| 2 | 2_data_pipeline.md | 2_data_pipeline.py | 数据收集与清洗 |
| 3 | 3_tokenizer.md | 3_tokenizer.py | Tokenizer设计 |
| 4 | 4_distributed_training.md | 4_distributed_training.py | 分布式训练 |
| 5 | 5_alignment.md | 5_alignment.py | RLHF与DPO对齐 |
| 6 | 6_scaling_laws.md | 6_scaling_laws.py | Scaling Laws |

## 前置知识

- Transformer深入（第44章）
- 深度学习基础（第31章）

## 安装依赖

```bash
pip install torch transformers tokenizers datasets
pip install trl  # RLHF/DPO训练
```

## 章节导航

[上一章：Transformer深入](../44_Transformer深入/README.md) | [下一章：多模态](../46_多模态/README.md)
