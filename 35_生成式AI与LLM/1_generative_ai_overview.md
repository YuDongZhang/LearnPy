# 1. 生成式AI概述

## 什么是生成式AI

**生成式AI (Generative AI)** 是人工智能的一个重要分支，指能够**创建新内容**的AI系统，包括文本、图像、音频、视频等，通常基于大规模预训练模型。

| 对比 | 判别式AI | 生成式AI |
|------|---------|---------|
| 任务 | 分类、预测（如图像识别） | 创建新内容（如写作、绘画） |
| 输出 | 标签/数值 | 全新内容 |

核心能力：内容创作、问答对话、代码生成、知识推理。

## 发展历程

| 年份 | 里程碑 |
|------|--------|
| 2013 | VAE (变分自编码器) |
| 2014 | GAN (生成对抗网络) |
| 2017 | Transformer 论文 |
| 2018 | GPT, BERT |
| 2020 | GPT-3, DALL-E |
| 2022 | ChatGPT, Stable Diffusion |
| 2023 | GPT-4, LLaMA, Claude |
| 2024 | GPT-4o, Claude 3, Gemini |

## 主要技术路线

| 路线 | 代表模型 | 用途 |
|------|---------|------|
| 大语言模型 (LLM) | GPT、Claude、LLaMA、Gemini | 文本生成 |
| 扩散模型 (Diffusion) | Stable Diffusion、DALL-E、Midjourney | 图像生成 |
| 其他生成模型 | VAE、GAN、Flow-based | 早期生成技术 |

## Transformer 架构

Transformer (2017) 是现代生成式AI的基石：

- **核心组件**：自注意力机制 (Self-Attention)、位置编码、前馈网络 (FFN)、残差连接 & 层归一化
- **自注意力公式**：Attention(Q, K, V) = softmax(QK^T / √d_k) V
- **优势**：并行计算效率高、捕捉长距离依赖、可扩展性强

## GPT 系列演进

| 模型 | 年份 | 参数量 | 特点 |
|------|------|--------|------|
| GPT-1 | 2018 | 1.17亿 | 无监督预训练 + 有监督微调 |
| GPT-2 | 2019 | 15亿 | 零样本学习 |
| GPT-3 | 2020 | 1750亿 | Few-shot 学习、强大泛化 |
| GPT-3.5 | 2022 | - | RLHF 微调，ChatGPT 背后的模型 |
| GPT-4 | 2023 | - | 多模态、更强推理、更长上下文 |

## LLM 关键概念

| 概念 | 说明 |
|------|------|
| 预训练 | 在大规模文本语料上预测下一个 token，学习通用知识 |
| 微调 | 在特定数据上继续训练：指令微调 (Instruction Tuning)、对齐微调 (RLHF) |
| 上下文学习 | Zero-shot（无示例）、Few-shot（少量示例）、Chain-of-Thought（思维链） |
| 涌现能力 | 模型规模超过阈值后出现的推理、编程、数学等新能力 |

## 应用领域

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

## 评估指标

- **文本生成**：BLEU (n-gram 重叠)、ROUGE (召回率)、Perplexity (困惑度)
- **能力评估**：MMLU (多任务理解)、HumanEval (代码)、Big-Bench (综合)
- **对话评估**：Chatbot Arena、LLM-as-a-Judge
- **安全**：有害内容检测、偏见检测

## 开源模型与本地部署

常见开源模型：LLaMA 2/3（Meta，商业可用）、Mistral 7B、Mixtral 8x7B（专家混合）、Qwen（阿里）、ChatGLM（智谱）、Falcon、BLOOM。

本地部署工具：Ollama、llama.cpp、vLLM。

API 服务：OpenAI (GPT-4/GPT-4o)、Anthropic (Claude)、Google (Gemini)、国内的百度文心一言、阿里通义千问、智谱 GLM。

## 第一个 LLM 程序

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一个专业的Python教练"},
        {"role": "user", "content": "什么是生成式AI？"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

## 学习路径建议

1. 生成式AI基础概念
2. 大语言模型发展历程
3. Transformer架构
4. Prompt工程
5. LLM API调用
6. RAG检索增强生成
7. 实战项目

## 代码

讲解对应的示例代码见 `1_generative_ai_overview.py`。
