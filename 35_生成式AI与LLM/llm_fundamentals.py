"""
大语言模型基础
============

介绍大语言模型(LLM)的工作原理、技术架构和训练方法。
"""

print("=" * 60)
print("1. 语言模型基础")
print("=" * 60)

print("""
语言模型 (Language Model):

定义:
  • 对文本序列的概率建模
  • P(w_1, w_2, ..., w_n)

N-gram模型:
  • 基于词频统计
  • 马尔可夫假设
  • 简单但效果有限

神经网络语言模型:
  • RNN/LSTM
  • Transformer
  • 效果显著提升
""")

print()
print("=" * 60)
print("2. Transformer架构")
print("=" * 60)

print("""
Transformer组成:

2.1 编码器-解码器结构

  Input → Encoder → Decoder → Output

  • Encoder: 理解输入
  • Decoder: 生成输出
  • 注意力机制连接

2.2 核心组件

  • Multi-Head Attention
  • Feed-Forward Network
  • Add & Norm (残差+层归一化)
  • Positional Encoding
""")

print()
print("=" * 60)
print("3. 自注意力机制")
print("=" * 60)

print("""
自注意力 (Self-Attention):

计算步骤:

1. Q, K, V 投影:
   Q = XW_Q, K = XW_K, V = XW_V

2. 注意力分数:
   scores = QK^T / sqrt(d_k)

3. 归一化:
   attention = softmax(scores)

4. 加权求和:
   output = attention * V

多头注意力:
  • 多个注意力头并行
  • 捕捉不同类型的关系
  • 增强表达能力
""")

print()
print("=" * 60)
print("4. 位置编码")
print("=" * 60)

print("""
位置编码 (Positional Encoding):

为什么需要:
  • Transformer并行处理
  • 需要注入位置信息

Sinusoidal编码:
  PE(pos, 2i) = sin(pos / 10000^(2i/d))
  PE(pos, 2i+1) = cos(pos / 10000^(2i/d))

相对位置编码:
  • RoPE (Rotary Position Embedding)
  • ALiBi
  • 更长的上下文
""")

print()
print("=" * 60)
print("5. GPT架构")
print("=" * 60)

print("""
GPT (Decoder-only):

特点:
  • 只使用解码器
  • 单向注意力
  • 因果语言建模

结构:
  • 多层Transformer解码器
  • 残差网络
  • 层归一化

训练目标:
  • 预测下一个token
  • 最大化 P(w_t | w_1, ..., w_{t-1})
""")

print()
print("=" * 60)
print("6. BERT架构")
print("=" * 60)

print("""
BERT (Encoder-only):

特点:
  • 只使用编码器
  • 双向注意力
  • 掩码语言建模

训练任务:
  1. MLM (Masked LM):
     • 随机掩码15%token
     • 预测被掩码的词

  2. NSP (Next Sentence Prediction):
     • 判断句子顺序

优势:
  • 理解能力强
  • 适合分类任务
""")

print()
print("=" * 60)
print("7. 模型规模")
print("=" * 60)

print("""
7.1 参数规模

  | 模型 | 参数量 |
  |------|--------|
  | GPT-1 | 117M |
  | GPT-2 | 1.5B |
  | GPT-3 | 175B |
  | GPT-4 | ~1.7T* |
  | LLaMA 3 70B | 70B |

  * 估算值

7.2 计算需求

  • 训练: 数千到数万个GPU
  • 推理: 单卡到多卡

7.3 扩展定律

  • Chinchilla定律
  • 更大模型需要更多数据
""")

print()
print("=" * 60)
print("8. 预训练过程")
print("=" * 60)

print("""
预训练 (Pre-training):

数据收集:
  • 网页文本
  • 代码仓库
  • 书籍
  • 对话数据

数据处理:
  • 清洗去重
  • 质量过滤
  • 分词 (Tokenization)

训练过程:
  • 无监督学习
  • 下一个token预测
  • 大规模计算

训练技巧:
  • 混合精度训练
  • 梯度累积
  • 分布式训练
""")

print()
print("=" * 60)
print("9. 微调方法")
print("=" * 60)

print("""
9.1 指令微调 (SFT)

  • 在指令-回答数据上微调
  • 提高指令遵循能力
  • 格式: Instruction → Response

9.2 RLHF

  步骤:
  1. 收集人类反馈
  2. 训练奖励模型
  3. PPO优化策略

  优势:
  • 对齐人类偏好
  • 减少有害输出

9.3 LoRA

  • 低秩适配
  • 减少微调成本
  • 参数效率高
""")

print()
print("=" * 60)
print("10. 推理优化")
print("=" * 60)

print("""
10.1 量化

  • INT8/INT4量化
  • 减少内存和计算
  • 保持性能

10.2 蒸馏

  • 知识蒸馏
  • 小模型学习大模型

10.3 推理框架

  • vLLM
  • TensorRT-LLM
  • llama.cpp

10.4 批处理

  • Continuous Batching
  • PagedAttention
""")

print()
print("=" * 60)
print("11. 上下文长度")
print("=" * 60)

print("""
上下文窗口:

发展历程:
  • GPT-3: 4K
  • GPT-3.5: 4K/16K
  • GPT-4: 8K/32K
  • Claude 2: 100K
  • GPT-4 Turbo: 128K
  • Gemini 1.5: 1M+

技术挑战:
  • 注意力复杂度 O(n²)
  • 显存限制

解决方案:
  • 稀疏注意力
  • 滑动窗口
  • 线性注意力
""")

print()
print("=" * 60)
print("12. Tokenization")
print("=" * 60)

print("""
分词 (Tokenization):

BPE (Byte Pair Encoding):
  • 合并高频字节对
  • 平衡词表和粒度

WordPiece:
  • 类似BPE
  • 谷歌系模型使用

SentencePiece:
  • 无监督文本分词
  • 支持多种语言

词表大小:
  • GPT-2: 50K
  • GPT-3/4: 100K
  • LLaMA: 32K
""")

print()
print("=" * 60)
print("13. 涌现能力")
print("=" * 60)

print("""
涌现能力 (Emergent Abilities):

定义:
  • 规模超过阈值后出现的新能力
  • 小模型不具备

典型能力:
  • 思维链推理
  • 零样本学习
  • 指令遵循
  • 代码编写

争议:
  • 可能是评估指标设计
  • 连续 vs 离散能力
""")

print()
print("=" * 60)
print("14. 幻觉问题")
print("=" * 60)

print("""
幻觉 (Hallucination):

定义:
  • 生成看似合理但错误的内容

原因:
  • 训练数据偏差
  • 最大化概率的解码策略
  • 知识边界不清晰

缓解方法:
  • RAG (检索增强)
  • 事实核查
  • Chain-of-Thought
  • 提示词约束
""")

print()
print("=" * 60)
print("15. 多模态模型")
print("=" * 60)

print("""
多模态LLM:

15.1 架构

  • 视觉编码器 + LLM
  • 跨模态对齐
  • 端到端训练

15.2 代表模型

  • GPT-4V: 图像理解
  • Gemini: 原生多模态
  • LLaVA: 开源方案
  • DALL-E: 图像生成

15.3 应用

  • 视觉问答
  • 图像描述
  • 图表理解
""")

print()
print("=" * 60)
print("16. 代码模型")
print("=" * 60)

print("""
代码生成模型:

16.1 专业模型

  • CodeLlama
  • StarCoder
  • DeepSeek-Coder

16.2 训练方法

  • 代码预训练
  • 指令微调
  • SQL微调

16.3 评估

  • HumanEval
  • MBPP
  • Codex Eval
""")

print()
print("=" * 60)
print("17. PyTorch实现")
print("=" * 60)

print('''
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size = x.size(0)

        # 线性变换
        Q = self.W_q(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        # 注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attention = torch.softmax(scores, dim=-1)
        out = torch.matmul(attention, V)

        # 输出
        out = out.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        return self.W_o(out)
''')

print()
print("=" * 60)
print("18. 使用Hugging Face")
print("=" * 60)

print('''
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载模型
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 生成文本
input_text = "Once upon a time"
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    temperature=0.7,
    do_sample=True
)

print(tokenizer.decode(outputs[0]))

# 使用Pipeline
from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")
result = generator("In a world where", max_new_tokens=50)
print(result)
''')

print()
print("=" * 60)
print("19. LLM原理总结")
print("=" * 60)

print("""
大语言模型要点:

✓ 核心架构:
  • Transformer
  • 自注意力机制
  • 位置编码

✓ 训练范式:
  • 预训练 (语言建模)
  • 指令微调 (SFT)
  • 对齐微调 (RLHF)

✓ 模型系列:
  • GPT: Decoder-only
  • BERT: Encoder-only
  • T5: Encoder-Decoder

✓ 关键技术:
  • Tokenization
  • 量化
  • LoRA
  • 上下文扩展

✓ 挑战:
  • 幻觉问题
  • 推理效率
  • 知识更新
""")
