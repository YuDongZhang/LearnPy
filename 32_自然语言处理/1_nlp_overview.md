# 1. NLP概述

## 什么是自然语言处理

**自然语言处理 (Natural Language Processing, NLP)** 是人工智能与语言学的交叉学科，研究如何让计算机理解和生成人类语言。

三个相关概念：
- **NLP**：自然语言处理（总称）
- **NLU**：自然语言理解（理解含义）
- **NLG**：自然语言生成（生成文本）

NLP 的挑战：
- 歧义性："意思"可以是意义、意图、想法...
- 多样性：同一种表达有多种方式
- 上下文依赖：理解需要上下文
- 隐含意义：讽刺、隐喻等

## NLP任务类型

| 任务类型 | 说明 | 示例 |
|---------|------|------|
| 文本分类 | 给文本打标签 | 情感分析、新闻分类、垃圾邮件检测 |
| 序列标注 | 给每个 token 打标签 | 命名实体识别(NER)、词性标注(POS)、分词 |
| 序列到序列 | 输入序列 → 输出序列 | 机器翻译、文本摘要、对话系统 |
| 文本生成 | 生成新文本 | 写作助手、代码生成、诗歌创作 |
| 问答系统 | 根据问题给出答案 | 阅读理解、知识问答 |

## 发展历程

| 时期 | 时代 | 代表方法 |
|------|------|---------|
| 1950s-1980s | 规则时代 | 词典和语法分析，难以处理复杂语言 |
| 1990s-2010s | 统计学习时代 | 词袋模型、TF-IDF、HMM、CRF |
| 2013-2017 | 词向量时代 | Word2Vec (2013)、GloVe (2014) |
| 2017- | 深度学习时代 | RNN/LSTM、Attention、Transformer (2017)、BERT (2018) |
| 2020- | 大语言模型时代 | GPT-3 (2020)、ChatGPT (2022)、LLaMA 等 |

## 词向量

计算机无法直接处理文本，需要将文本转换为数值表示。

**One-Hot 编码**：词表 [我, 爱, 中国] 中，"我" → [1, 0, 0]。问题：维度高、稀疏、无语义。

**词嵌入 (Word Embedding)**：词 → 密集向量（如 300 维），语义相近的词向量也相近。

词向量的神奇性质：
```
国王 - 男人 + 女人 ≈ 女王
巴黎 - 法国 + 日本 ≈ 东京
```

## 预训练-微调范式

```
预训练: 在大规模语料上学习通用表示
微调:   在下游任务上微调
```

优势：数据需求少、效果好、可迁移。

| 模型 | 年份 | 特点 |
|------|------|------|
| BERT | 2018 | 双向编码器 |
| GPT | 2018 | 单向解码器 |
| RoBERTa | 2019 | BERT 改进 |
| ALBERT | 2019 | 轻量级 BERT |
| T5 | 2019 | Text-to-Text 统一框架 |
| GPT-3 | 2020 | 1750亿参数大语言模型 |
| GPT-4 | 2023 | 多模态 |

## 主流NLP框架

| 框架 | 特点 | 安装 |
|------|------|------|
| Hugging Face Transformers | 最流行，提供海量预训练模型 | `pip install transformers` |
| torchtext | PyTorch 生态，提供数据集和模型 | `pip install torchtext` |
| spaCy | 工业级，多语言支持，快速高效 | `pip install spacy` |
| NLTK | 经典 NLP 库，教学友好 | `pip install nltk` |
| jieba | 中文分词 | `pip install jieba` |

## 常用数据集

- 英文：IMDb、SST-2（情感分析），CoNLL-2003（NER），GLUE（基准测试），SQuAD（问答）
- 中文：ChnSentiCorp（情感分析），MSRA（NER），LCQMC（文本匹配），CMRC（问答）
- 预训练语料：Wikipedia、BookCorpus、Common Crawl

## NLP项目流程

```
1. 数据收集     →  爬虫 / 公开数据集 / API
2. 数据预处理   →  清洗、分词、去停用词
3. 特征工程     →  词向量、词频统计
4. 模型选择     →  传统(SVM/朴素贝叶斯) 或 深度学习(LSTM/Transformer)
5. 训练调优     →  超参数调整、正则化、早停
6. 评估部署     →  准确率/F1/BLEU、模型部署
```

## 评估指标

| 任务 | 指标 |
|------|------|
| 分类 | Accuracy、Precision、Recall、F1 |
| 序列标注 | entity-level F1、token-level accuracy |
| 机器翻译 | BLEU、METEOR |
| 摘要 | ROUGE |
| 问答 | Exact Match (EM)、F1 |

## 第一个NLP程序

```python
from transformers import pipeline

# 情感分析
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

## 学习路径建议

1. 基础：文本预处理、词向量、传统机器学习
2. 深度学习：RNN/LSTM、序列到序列、Attention
3. Transformer：原理、BERT/GPT 使用、微调
4. 进阶：大语言模型、Prompt Engineering、部署

## 代码

讲解对应的示例代码见 `1_nlp_overview.py`。
