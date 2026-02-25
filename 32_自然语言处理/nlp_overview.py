"""
自然语言处理概述与发展历程
=========================

介绍 NLP 的基本概念和发展历程。
"""

print("=" * 60)
print("1. NLP 简介")
print("=" * 60)

print("""
自然语言处理 (Natural Language Processing, NLP):
  研究如何让计算机理解和生成人类语言

NLP 的挑战:
  • 歧义性: "意思" 可以是意义、意图、想法...
  • 多样性: 同一种表达有多种方式
  • 上下文依赖: 理解需要上下文
  • 隐含意义: 讽刺、隐喻等

NLP vs NLU vs NLG:
  • NLP: 自然语言处理 (总称)
  • NLU: 自然语言理解 (理解含义)
  • NLG: 自然语言生成 (生成文本)
""")

print()
print("=" * 60)
print("2. NLP 任务类型")
print("=" * 60)

print("""
2.1 文本分类
  • 情感分析: 正面/负面
  • 主题分类: 新闻分类
  • 垃圾邮件检测

2.2 序列标注
  • 命名实体识别 (NER): 识别人名、地名
  • 词性标注 (POS): 名词、动词...
  • 分词: 中文分词

2.3 序列到序列
  • 机器翻译: 中文 → 英文
  • 文本摘要: 长文 → 短文
  • 对话系统: 问答

2.4 文本生成
  • 写作助手
  • 代码生成
  • 诗歌创作

2.5 问答系统
  • 阅读理解
  • 知识问答
""")

print()
print("=" * 60)
print("3. NLP 发展历程")
print("=" * 60)

print("""
1950s-1980s: 规则时代
  • 基于规则的方法
  • 词典和语法分析
  • 局限: 难以处理复杂语言

1990s-2010s: 统计学习时代
  • 统计机器学习
  • 词袋模型 (Bag of Words)
  • TF-IDF
  • HMM, CRF

2013-2017: 词向量时代
  • Word2Vec (2013)
  • GloVe (2014)
  • 预训练词向量

2017-: 深度学习时代
  • RNN/LSTM/GRU
  • Attention 机制
  • Transformer (2017)
  • BERT (2018)
  • GPT 系列 (2018-)

2020-: 大语言模型时代
  • GPT-3 (2020)
  • ChatGPT (2022)
  • LLaMA, Claude 等
""")

print()
print("=" * 60)
print("4. 词向量")
print("=" * 60)

print("""
为什么需要词向量?
  • 计算机无法直接处理文本
  • 需要将文本转换为数值表示

4.1 One-Hot 编码
  • 词表: [我, 爱, 中国]
  • 我:   [1, 0, 0]
  • 爱:   [0, 1, 0]
  • 问题: 维度高, 稀疏, 无语义

4.2 词嵌入 (Word Embedding)
  • 词向量: 词 → 密集向量 (如 300维)
  • 语义相近的词向量也相近
  • Word2Vec, GloVe, FastText

4.3 词向量性质
  • 国王 - 男人 + 女人 ≈ 女王
  • 巴黎 - 法国 + 日本 ≈ 东京
""")

print()
print("=" * 60)
print("5. 主流 NLP 框架")
print("=" * 60)

print("""
5.1 Hugging Face Transformers
  • 最流行的 NLP 库
  • 提供预训练模型
  • 简单易用

  pip install transformers

5.2 PyTorch NLP
  • PyTorch 生态
  • 提供数据集和模型

  pip install torchtext

5.3 spaCy
  • 工业级 NLP
  • 多语言支持
  • 快速高效

  pip install spacy

5.4 NLTK
  • 经典 NLP 库
  • 教学友好

  pip install nltk
""")

print()
print("=" * 60)
print("6. 常用数据集")
print("=" * 6)

print("""
6.1 英文数据集
  • IMDb 影评情感分析
  • SST-2 情感分析
  • CoNLL-2003 命名实体识别
  • GLUE 基准测试
  • SQuAD 问答

6.2 中文数据集
  • ChnSentiCorp 情感分析
  • MSRA 命名实体识别
  • LCQMC 文本匹配
  • CMRC 问答

6.3 预训练语料
  • Wikipedia
  • BookCorpus
  • Common Crawl
""")

print()
print("=" * 60)
print("7. NLP 流程")
print("=" * 60)

print("""
典型 NLP 项目流程:

1. 数据收集
   • 爬虫获取
   • 公开数据集
   • API 接口

2. 数据预处理
   • 清洗: 去除噪声
   • 分词: 切分成词/字
   • 去停用词
   • 词性标注

3. 特征工程
   • 词向量
   • 词频统计
   • 特征选择

4. 模型选择
   • 传统: SVM, 朴素贝叶斯
   • 深度学习: LSTM, Transformer

5. 训练调优
   • 超参数调整
   • 正则化
   • 早停

6. 评估部署
   • 准确率, F1, BLEU
   • 模型部署
   • 在线预测
""")

print()
print("=" * 60)
print("8. 评估指标")
print("=" * 60)

print("""
8.1 分类任务
  • Accuracy: 准确率
  • Precision: 精确率
  • Recall: 召回率
  • F1 Score: F1 分数

8.2 序列标注
  • entity-level F1
  • token-level accuracy

8.3 机器翻译
  • BLEU (Bilingual Evaluation Understudy)
  • METEOR
  • ROUGE (摘要)

8.4 问答
  • Exact Match (EM)
  • F1 Score
""")

print()
print("=" * 60)
print("9. 预训练模型时代")
print("=" * 60)

print("""
9.1 预训练-微调范式

  预训练: 在大规模语料上学习通用表示
  微调:   在下游任务上微调

  优势:
    ✓ 数据需求少
    ✓ 效果好
    ✓ 可迁移

9.2 代表模型

  • BERT (2018): 双向编码器
  • GPT (2018): 单向解码器
  • RoBERTa (2019): BERT 改进
  • ALBERT (2019): 轻量级 BERT
  • T5 (2019): Text-to-Text
  • GPT-2/3 (2019/2020): 大语言模型
  • GPT-4 (2023): 多模态

9.3 Hugging Face Hub
  • 100,000+ 预训练模型
  • 10,000+ 数据集
  • 简单 API 调用
""")

print()
print("=" * 60)
print("10. 安装 NLP 库")
print("=" * 60)

print("""
pip install transformers torch
pip install datasets accelerate
pip install tokenizers
pip install spacy
pip install jieba          # 中文分词
pip install snownlp        # 中文情感分析
pip install ltp           # 哈工大语言技术平台

# 中文 spaCy 模型
python -m spacy download zh_core_web_sm
""")

print()
print("=" * 60)
print("11. 第一个 NLP 程序")
print("=" * 60)

print("""
# 使用 Hugging Face Transformers

from transformers import pipeline

# 情感分析
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
print(result)
# [{'label': 'POSITIVE', 'score': 0.9998}]

# 中文情感分析
classifier = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-chinanews-chinese")
result = classifier("这个产品很好用")
print(result)

# 问答系统
question_answerer = pipeline("question-answering")
result = question_answerer(
    question="What is AI?",
    context="Artificial intelligence is..."
)
print(result)
""")

print()
print("=" * 60)
print("12. NLP 学习路径")
print("=" * 60)

print("""
推荐学习路线:

阶段1: 基础
  • 文本预处理
  • 词向量
  • 传统机器学习方法

阶段2: 深度学习
  • RNN/LSTM 原理
  • 序列到序列模型
  • Attention 机制

阶段3: Transformer
  • Transformer 原理
  • BERT/GPT 使用
  • 微调技术

阶段4: 进阶
  • 大语言模型使用
  • Prompt Engineering
  • 模型部署

实战项目:
  • 情感分析
  • 命名实体识别
  • 机器翻译
  • 文本摘要
  • 问答系统
  • 对话机器人
""")
