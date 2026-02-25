"""
生成式AI概述
==========

介绍生成式AI的基本概念、发展历程和应用领域。
"""

print("=" * 60)
print("1. 生成式AI简介")
print("=" * 60)

print("""
生成式AI (Generative AI):

定义:
  • 能够创建新内容的AI系统
  • 包括文本、图像、音频、视频等
  • 基于大规模预训练模型

与判别式AI的区别:
  • 判别式AI: 分类、预测 (如图像识别)
  • 生成式AI: 创建新内容 (如写作、绘画)

核心能力:
  • 内容创作
  • 问答对话
  • 代码生成
  • 知识推理
""")

print()
print("=" * 60)
print("2. 生成式AI发展历程")
print("=" * 60)

print("""
| 年份 | 里程碑 |
|------|--------|
| 2013 | VAE (变分自编码器) |
| 2014 | GAN (生成对抗网络) |
| 2017 | Transformer 论文 |
| 2018 | GPT, BERT |
| 2019 | GPT-2, BigGAN |
| 2020 | GPT-3, DALL-E |
| 2021 | GPT-3.5, CLIP |
| 2022 | ChatGPT, Stable Diffusion |
| 2023 | GPT-4, LLaMA, Claude |
| 2024 | GPT-4o, Claude 3, Gemini |
""")

print()
print("=" * 60)
print("3. 主要技术路线")
print("=" * 60)

print("""
3.1 大语言模型 (LLM)

  基于Transformer的文本生成模型:
  • GPT系列 (OpenAI)
  • Claude系列 (Anthropic)
  • LLaMA系列 (Meta)
  • Gemini (Google)

3.2 扩散模型 (Diffusion)

  图像生成的主流技术:
  • Stable Diffusion
  • DALL-E
  • Midjourney

3.3 其他生成模型

  • VAE: 变分自编码器
  • GAN: 生成对抗网络
  • Flow-based models
""")

print()
print("=" * 60)
print("4. Transformer架构")
print("=" * 60)

print("""
Transformer (2017):

核心组件:
  • 自注意力机制 (Self-Attention)
  • 位置编码 (Positional Encoding)
  • 前馈网络 (FFN)
  • 残差连接 & 层归一化

自注意力公式:
  Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V

优势:
  • 并行计算效率高
  • 捕捉长距离依赖
  • 可扩展性强
""")

print()
print("=" * 60)
print("5. GPT系列模型")
print("=" * 60)

print("""
GPT (Generative Pre-trained Transformer):

GPT-1 (2018):
  • 1.17亿参数
  • 无监督预训练 + 有监督微调

GPT-2 (2019):
  • 15亿参数
  • 零样本学习

GPT-3 (2020):
  • 1750亿参数
  • Few-shot学习
  • 强大的泛化能力

GPT-3.5 (2022):
  • RLHF微调
  • ChatGPT背后的模型

GPT-4 (2023):
  • 多模态能力
  • 更强的推理能力
  • 更长的上下文
""")

print()
print("=" * 60)
print("6. LLM关键概念")
print("=" * 60)

print("""
6.1 预训练 (Pre-training)

  • 在大规模文本语料上训练
  • 预测下一个token (语言建模)
  • 学习通用知识

6.2 微调 (Fine-tuning)

  • 在特定数据上继续训练
  • 指令微调 (Instruction Tuning)
  • 对齐微调 (RLHF)

6.3 上下文学习

  • Zero-shot: 无示例
  • Few-shot: 少量示例
  • Chain-of-Thought: 思维链

6.4 涌现能力

  • 大规模后出现的新能力
  • 推理、编程、数学等
""")

print()
print("=" * 60)
print("7. 生成式AI应用")
print("=" * 60)

print("""
| 领域 | 应用 |
|------|------|
| 文本 | 写作助手、客服、翻译 |
| 图像 | AI绘画、图片编辑 |
| 音频 | 语音合成、音乐生成 |
| 视频 | 视频生成、编辑 |
| 代码 | 代码生成、调试 |
| 教育 | 个性化辅导 |
| 医疗 | 辅助诊断 |
| 金融 | 分析报告 |

企业应用场景:
  • 智能客服
  • 内容审核
  • 数据分析
  • 自动化流程
""")

print()
print("=" * 60)
print("8. LLM评估指标")
print("=" * 60)

print("""
8.1 文本生成评估

  • BLEU: n-gram重叠
  • ROUGE: 召回率
  • Perplexity: 困惑度

8.2 能力评估

  • MMLU: 多任务理解
  • HumanEval: 代码能力
  • Big-Bench: 综合能力

8.3 对话评估

  • Chatbot Arena
  • LLM-as-a-Judge

8.4 安全

  • 有害内容评估检测
  • 偏见检测
""")

print()
print("=" * 60)
print("9. 开源模型")
print("=" * 60)

print("""
9.1 LLaMA系列

  Meta开源:
  • LLaMA 2: 7B, 13B, 70B
  • LLaMA 3: 8B, 70B
  • 许可: 商业可用

9.2 Mistral系列

  • Mistral 7B
  • Mixtral 8x7B (专家混合)

9.3 其他开源

  • Falcon
  • BLOOM
  • Qwen (阿里)
  • ChatGLM (智谱)

9.4 本地部署

  • Ollama
  • llama.cpp
  • vLLM
""")

print()
print("=" * 60)
print("10. API服务")
print("=" * 60)

print("""
10.1 OpenAI API

  • GPT-4, GPT-4 Turbo
  • GPT-3.5 Turbo
  • Embeddings
  • DALL-E 图像

10.2 Anthropic API

  • Claude 3.5
  • Claude 3
  • 长上下文

10.3 Google API

  • Gemini Pro/Ultra
  • 多模态

10.4 国内API

  • 百度文心一言
  • 阿里通义千问
  • 智谱GLM
""")

print()
print("=" * 60)
print("11. 提示词工程")
print("=" * 60)

print("""
11.1 基本原则

  • 清晰明确的指令
  • 分解复杂任务
  • 指定输出格式
  • 提供示例

11.2 常用技巧

  • System Prompt: 设置角色
  • Few-shot: 提供示例
  • Chain-of-Thought: 思考过程
  • ReAct: 推理+行动

11.3 高级模式

  • Role Play: 角色扮演
  • Tree of Thoughts: 思维树
  • Self-Consistency: 自一致性
""")

print()
print("=" * 60)
print("12. RAG技术")
print("=" * 60)

print("""
RAG (Retrieval Augmented Generation):

原理:
  • 检索相关文档
  • 拼接到prompt
  • 生成答案

优势:
  • 解决知识时效性问题
  • 减少幻觉
  • 可引用来源

组件:
  • 向量数据库
  • 文本分割
  • 相似度检索
  • 重排序
""")

print()
print("=" * 60)
print("13. Agent技术")
print("=" * 60)

print("""
LLM Agent:

定义:
  • LLM + 工具 + 记忆
  • 自主规划和执行

核心组件:
  • Planning: 任务分解
  • Tool Use: 调用API
  • Memory: 记忆存储
  • Reflection: 反思改进

知名框架:
  • LangChain
  • LlamaIndex
  • AutoGPT
  • BabyAGI
""")

print()
print("=" * 60)
print("14. 安装依赖")
print("=" * 60)

print("""
pip install openai
pip install anthropic
pip install google-generativeai

pip install transformers
pip install torch
pip install accelerate

pip install langchain
pip install langchain-openai

pip install sentence-transformers
pip install faiss-cpu

pip install python-dotenv
""")

print()
print("=" * 60)
print("15. 第一个LLM程序")
print("=" * 60)

print('''
import os
from openai import OpenAI

# 设置API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 调用GPT
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一个专业的Python教练"},
        {"role": "user", "content": "什么是生成式AI？"}
    ],
    temperature=0.7,
    max_tokens=500
)

# 获取回复
print(response.choices[0].message.content)
''')

print()
print("=" * 60)
print("16. 生成式AI总结")
print("=" * 60)

print("""
生成式AI要点:

✓ 核心技术:
  • Transformer架构
  • 自注意力机制
  • 大规模预训练

✓ 主流模型:
  • GPT系列
  • Claude系列
  • 开源LLaMA等

✓ 重要概念:
  • 预训练与微调
  • 上下文学习
  • Prompt工程
  • RAG
  • Agent

✓ 应用领域:
  • 文本生成
  • 代码开发
  • 图像生成
  • 智能对话

✓ 学习建议:
  • 掌握Transformer原理
  • 实践Prompt工程
  • 学习RAG和Agent
""")
