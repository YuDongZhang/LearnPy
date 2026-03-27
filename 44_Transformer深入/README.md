# 第四十四章：Transformer深入

## 本章目标

- 从零实现Self-Attention机制
- 理解位置编码（绝对/旋转RoPE）
- 掌握Multi-Head Attention
- 理解KV Cache推理优化
- 从零搭建一个mini Transformer
- 了解主流LLM架构差异

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 内容 |
|------|----------|----------|------|
| 1 | 1_attention.md | 1_attention.py | 注意力机制从零实现 |
| 2 | 2_positional_encoding.md | 2_positional_encoding.py | 位置编码 |
| 3 | 3_transformer_block.md | 3_transformer_block.py | Transformer Block |
| 4 | 4_kv_cache.md | 4_kv_cache.py | KV Cache推理优化 |
| 5 | 5_mini_transformer.md | 5_mini_transformer.py | 从零搭建mini GPT |
| 6 | 6_llm_architectures.md | 6_llm_architectures.py | 主流LLM架构对比 |

## 前置知识

- Python基础
- 深度学习入门（第31章）
- PyTorch基础

## 安装依赖

```bash
pip install torch numpy matplotlib
```

## 章节导航

[上一章：MLOps](../43_MLOps/README.md) | [下一章：预训练技术](../45_预训练技术/README.md)
