# 7. GQA与MLA注意力

## 为什么需要改进MHA

标准多头注意力（MHA）每个Q头都有独立的K/V头，推理时KV Cache随头数线性增长：

```
KV Cache = 2 × num_layers × num_heads × head_dim × seq_len × 2bytes
```

128头模型（DeepSeek-V3量级），seq=4096时单层就要数百MB —— 长上下文的显存瓶颈全在这。

## 注意力变体演进

| 变体 | KV头数 | KV Cache | 质量 | 代表模型 |
|------|--------|---------|------|---------|
| MHA | =Q头数 | 最大 | 最好 | GPT-2, BERT |
| MQA | 1 | 最小 | 略降 | PaLM |
| GQA | 1~Q头数 | 中等 | 很好 | LLaMA 3, Qwen3, gpt-oss |
| MLA | 潜在向量 | 极小 | 最好 | DeepSeek V2/V3, Kimi K2, GLM |

## GQA：分组共享

思路：每 `num_heads / num_kv_heads` 个Q头共享一组KV头。

```
MHA:  32个Q头, 32个KV头  → cache 32组KV
GQA:  32个Q头,  8个KV头  → cache  8组KV   (省4倍)
MQA:  32个Q头,  1个KV头  → cache  1组KV   (GQA的特例)
```

实现上只改两处：
1. `W_K`/`W_V` 输出维度按KV头数算（参数量同步变省）
2. 计算前把KV头 `repeat_interleave` 到Q头数（真实框架用expand零拷贝）

GQA是2025-2026的事实标准：LLaMA 3、Qwen3、Mistral、gpt-oss全在用。

## MLA：低秩压缩（换个思路）

GQA靠"减少头数"省cache，MLA（DeepSeek V2首创）靠"压缩维度"：

```
GQA: cache K, V          （每token 2×num_heads×head_dim 维）
MLA: cache 潜在向量 c_kv  （每token d_latent + d_rope 维）
```

流程：

1. **压缩**：`c_kv = W_DKV · x`，把token压到低维（DeepSeek-V3: 512维）
2. **进cache的只有 c_kv**（外加RoPE用的k_rope）
3. **解压**：计算时 `K = W_UK · c_kv`，`V = W_UV · c_kv` 恢复每头的K/V

### 为什么要解耦RoPE

RoPE是对Q/K乘位置相关的旋转矩阵，而MLA的K是"压缩→解压"出来的：

```
RoPE(W_UK · c_kv) ≠ W_UK · RoPE(c_kv)   ← 旋转矩阵插不进低秩分解
```

所以位置信息单独走一条低维通路（`k_rope = W_KR · x`，所有头共享），
每头Query也拆成 [内容 | 位置] 两部分拼接计算。这是MLA设计里最巧妙的一步。

### 效果

按128头、head_dim=192（含RoPE）估算，每token每层cache：

| 方案 | 维度 | 占MHA比例 |
|------|------|-----------|
| MHA | 49152 | 100% |
| GQA (8 KV头) | 3072 | 6.3% |
| MQA | 384 | 0.8% |
| MLA | 576 | 1.2% |

注意：MQA的cache比MLA还小，但质量损失明显；MLA用低秩压缩在接近MHA的质量下
把cache压到1%左右。实际推理引擎还用"矩阵吸收"把W_UK吸收进Q，连解压都省掉。

> 2026动向：MLA已被Kimi K2、GLM-5等广泛采用；DeepSeek-V4改为沿序列维度的压缩，
> 配合1M上下文，cache进一步降到1/4 HBM占用。

## 代码

`7_gqa_and_mla.py`：GQA与MLA的完整实现（含增量解码一致性验证）、KV Cache对比表。
