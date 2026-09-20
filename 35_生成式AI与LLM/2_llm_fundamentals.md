# 2. 大语言模型基础

## 语言模型

**语言模型 (Language Model)** 对文本序列的概率建模：P(w_1, w_2, ..., w_n)。

| 阶段 | 模型 | 特点 |
|------|------|------|
| 统计 | N-gram | 基于词频统计、马尔可夫假设，效果有限 |
| 神经网络 | RNN/LSTM | 序列建模，难以并行 |
| Transformer | GPT/BERT | 并行计算、长距离依赖，效果显著提升 |

## Transformer 架构

经典结构为编码器-解码器：Input → Encoder → Decoder → Output。

核心组件：
- Multi-Head Attention（多头注意力）
- Feed-Forward Network（前馈网络）
- Add & Norm（残差连接 + 层归一化）
- Positional Encoding（位置编码）

## 自注意力机制

计算步骤：

```
1. Q, K, V 投影:   Q = XW_Q,  K = XW_K,  V = XW_V
2. 注意力分数:     scores = QK^T / sqrt(d_k)
3. 归一化:         attention = softmax(scores)
4. 加权求和:       output = attention · V
```

**多头注意力**：多个注意力头并行，各自捕捉不同类型的关系，增强表达能力。

## 位置编码

Transformer 并行处理序列，需要额外注入位置信息：

- **Sinusoidal 编码**：PE(pos, 2i) = sin(pos / 10000^(2i/d))，PE(pos, 2i+1) = cos(...)
- **相对位置编码**：RoPE (旋转位置编码)、ALiBi，支持更长上下文

## 三大架构

| 架构 | 代表 | 注意力 | 训练目标 | 适用场景 |
|------|------|--------|---------|---------|
| Decoder-only | GPT | 单向 | 因果语言建模（预测下一个 token） | 文本生成 |
| Encoder-only | BERT | 双向 | 掩码语言建模 (MLM) + 句序预测 (NSP) | 理解、分类 |
| Encoder-Decoder | T5 | 交叉注意力 | 序列到序列 | 翻译、摘要 |

BERT 的 MLM：随机掩码 15% 的 token，让模型预测被掩码的词。

## 模型规模

| 模型 | 参数量 |
|------|--------|
| GPT-1 | 117M |
| GPT-2 | 1.5B |
| GPT-3 | 175B |
| GPT-4 | ~1.7T* |
| LLaMA 3 70B | 70B |

(*估算值)。训练需要数千到数万个 GPU。**扩展定律 (Chinchilla)**：更大模型需要更多数据。

## 预训练过程

1. **数据收集**：网页文本、代码仓库、书籍、对话数据
2. **数据处理**：清洗去重、质量过滤、分词 (Tokenization)
3. **训练**：无监督的下一个 token 预测，大规模计算
4. **技巧**：混合精度训练、梯度累积、分布式训练

## 微调方法

| 方法 | 说明 |
|------|------|
| 指令微调 (SFT) | 在指令-回答数据上微调，提高指令遵循能力 |
| RLHF | 收集人类反馈 → 训练奖励模型 → PPO 优化，对齐人类偏好 |
| LoRA | 低秩适配，只训练少量参数，大幅降低微调成本 |

## 推理优化

- **量化**：INT8/INT4，减少内存和计算
- **蒸馏**：小模型学习大模型
- **推理框架**：vLLM、TensorRT-LLM、llama.cpp
- **批处理**：Continuous Batching、PagedAttention

## Tokenization

| 算法 | 特点 |
|------|------|
| BPE | 合并高频字节对，平衡词表和粒度 |
| WordPiece | 类似 BPE，谷歌系模型使用 |
| SentencePiece | 无监督分词，支持多种语言 |

词表大小：GPT-2 约 50K、GPT-3/4 约 100K、LLaMA 约 32K。

## 上下文长度

从 GPT-3 的 4K 发展到 Claude 2 的 100K、GPT-4 Turbo 的 128K、Gemini 1.5 的 1M+。

挑战：注意力复杂度 O(n²)、显存限制。解决方案：稀疏注意力、滑动窗口、线性注意力。

## 涌现能力与幻觉

**涌现能力**：规模超过阈值后出现的新能力（思维链推理、零样本学习、指令遵循、代码编写），小模型不具备。

**幻觉 (Hallucination)**：生成看似合理但错误的内容。原因：训练数据偏差、最大化概率的解码策略、知识边界不清晰。缓解方法：**RAG**、事实核查、Chain-of-Thought、提示词约束。

## 使用 Hugging Face

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

inputs = tokenizer("Once upon a time", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100,
                          temperature=0.7, do_sample=True)
print(tokenizer.decode(outputs[0]))
```

## 代码

讲解对应的示例代码见 `2_llm_fundamentals.py`。
