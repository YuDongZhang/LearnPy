# 4. KV Cache推理优化

## 自回归生成的问题

GPT生成文本是逐token的：
```
输入: "今天天气" → 生成 "很"
输入: "今天天气很" → 生成 "好"
输入: "今天天气很好" → 生成 "。"
```

每次生成新token都要重新计算所有token的Attention，大量重复计算。

## KV Cache原理

观察：之前token的K和V不会变，只有新token的K和V是新的。

解决：缓存之前所有token的K和V，每次只计算新token的Q、K、V。

```
第1步: 计算所有token的K,V → 缓存
第2步: 只计算新token的Q,K,V → 新K,V追加到缓存 → 用Q和全部K,V算Attention
第3步: 同上
...
```

## 显存占用

KV Cache的显存：
```
KV Cache = 2 × num_layers × num_heads × head_dim × seq_len × batch_size × 2bytes(fp16)
```

7B模型，序列长度4096：
- KV Cache ≈ 2 × 32 × 32 × 128 × 4096 × 2 ≈ 2GB

这就是为什么长序列推理需要大量显存。

## 优化技术

### GQA（Grouped Query Attention）
多个Q头共享一组K/V头，减少KV Cache大小。
- LLaMA 2 70B、Qwen2.5使用
- 例如：32个Q头，8个KV头 → KV Cache减少4倍

### MQA（Multi-Query Attention）
所有Q头共享同一组K/V → KV Cache最小，但质量略降。

### 滑动窗口注意力
只关注最近N个token，KV Cache固定大小。
- Mistral使用

### PagedAttention
vLLM的核心技术，像操作系统管理内存一样管理KV Cache：
- 按需分配，避免浪费
- 支持更大的batch size
- 大幅提升吞吐量

## 对比

| 技术 | KV Cache大小 | 质量 | 使用模型 |
|------|-------------|------|---------|
| MHA | 最大 | 最好 | GPT-2 |
| GQA | 中等 | 很好 | LLaMA 2, Qwen |
| MQA | 最小 | 好 | PaLM |
| 滑动窗口 | 固定 | 好 | Mistral |
