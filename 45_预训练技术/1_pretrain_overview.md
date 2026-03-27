# 1. 预训练流程概述

## LLM训练三阶段

```
阶段1: 预训练 (Pre-training)
  大量无标注文本 → 学习语言知识 → Base Model

阶段2: 指令微调 (SFT - Supervised Fine-Tuning)
  指令数据 → 学习遵循指令 → Chat Model

阶段3: 对齐 (Alignment)
  人类偏好数据 → RLHF/DPO → 更安全、更有用的模型
```

## 预训练

### 目标
预测下一个token（Next Token Prediction）：
```
输入: "今天天气"
标签: "天天气很"（右移一位）
损失: CrossEntropyLoss
```

### 数据规模
| 模型 | 训练数据 |
|------|---------|
| GPT-3 | 300B tokens |
| LLaMA 2 | 2T tokens |
| LLaMA 3 | 15T tokens |
| Qwen2.5 | 18T tokens |

### 算力需求
训练一个7B模型约需：
- 数据：1-2T tokens
- 算力：约1000 GPU·天（A100）
- 成本：约$100万-$500万

## 指令微调（SFT）

在Base Model上用指令数据微调：
```json
{"instruction": "翻译成英文", "input": "你好", "output": "Hello"}
```
数据量：几千到几万条高质量数据。

## 对齐（Alignment）

让模型输出符合人类偏好：
- RLHF：用奖励模型+强化学习
- DPO：直接偏好优化，更简单

## 完整流程

```
数据收集 → 数据清洗 → Tokenizer训练 → 预训练 → SFT → 对齐 → 评估 → 部署
```
