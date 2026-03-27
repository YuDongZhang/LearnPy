# 6. 主流LLM架构对比

## 三种架构

| 架构 | 代表模型 | 特点 |
|------|---------|------|
| Encoder-only | BERT | 双向注意力，适合理解任务 |
| Decoder-only | GPT, LLaMA | 因果注意力，适合生成任务 |
| Encoder-Decoder | T5, BART | 编码+解码，适合翻译/摘要 |

当前LLM主流是Decoder-only。

## 主流LLM架构细节

| 模型 | 参数 | 注意力 | 位置编码 | Norm | FFN | 特殊设计 |
|------|------|--------|---------|------|-----|---------|
| GPT-2 | 1.5B | MHA | Learned | Post-LN | GELU | - |
| LLaMA 2 | 7-70B | GQA | RoPE | RMSNorm | SwiGLU | - |
| LLaMA 3 | 8-70B | GQA | RoPE | RMSNorm | SwiGLU | 128K上下文 |
| Qwen2.5 | 0.5-72B | GQA | RoPE | RMSNorm | SwiGLU | 中文优化 |
| Mistral | 7B | GQA | RoPE | RMSNorm | SwiGLU | 滑动窗口 |
| Phi-3 | 3.8B | MHA | RoPE | RMSNorm | SwiGLU | 高质量数据 |
| DeepSeek V2 | 236B | MLA | RoPE | RMSNorm | DeepSeekMoE | MoE架构 |

## 现代LLM的标配

几乎所有2024+的LLM都采用：
- Decoder-only架构
- RoPE位置编码
- Pre-RMSNorm
- SwiGLU FFN
- GQA注意力

## MoE（混合专家）

DeepSeek V2、Mixtral等使用MoE：
- FFN层有多个"专家"网络
- 路由器选择Top-K个专家处理每个token
- 总参数量大，但每次推理只激活一部分
- 例如：236B总参数，每次只激活21B

## 长上下文技术

| 技术 | 说明 |
|------|------|
| RoPE外推 | NTK-aware scaling, YaRN |
| 滑动窗口 | 固定窗口大小 |
| 稀疏注意力 | 只关注部分token |
| Ring Attention | 分布式长序列 |
