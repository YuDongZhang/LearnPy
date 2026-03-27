# 3. Transformer Block

## Decoder Block结构

GPT类模型使用Decoder-only架构，每个Block包含：

```
输入
 ↓
LayerNorm (Pre-Norm)
 ↓
Causal Multi-Head Attention
 ↓
残差连接 (+)
 ↓
LayerNorm
 ↓
FFN (Feed-Forward Network)
 ↓
残差连接 (+)
 ↓
输出
```

## Pre-Norm vs Post-Norm

| 方式 | 公式 | 特点 |
|------|------|------|
| Post-Norm | x + Attn(LayerNorm(x)) ❌ | 原始Transformer，训练不稳定 |
| Pre-Norm | x + Attn(LayerNorm(x)) ✓ | 现代LLM标配，训练更稳定 |

## RMSNorm

LLaMA等模型用RMSNorm替代LayerNorm：
```
RMSNorm(x) = x / RMS(x) × γ
RMS(x) = √(mean(x²))
```
比LayerNorm少一个减均值的步骤，更快。

## FFN（前馈网络）

### 标准FFN
```
FFN(x) = W2 × GELU(W1 × x)
```

### SwiGLU FFN（LLaMA使用）
```
FFN(x) = W2 × (SiLU(W_gate × x) ⊙ (W_up × x))
```
多一个门控机制，效果更好，但参数多一个矩阵。

## 完整参数量

一个Transformer Block的参数：
- Attention: 4 × d² (Q, K, V, O)
- FFN: 3 × d × d_ff (gate, up, down) 或 2 × d × d_ff (标准)
- LayerNorm: 2 × d

总计约 12d²（标准）或 16d²（SwiGLU, d_ff ≈ 8/3 d）

## 堆叠

一个完整的LLM = Embedding + N个Block + LM Head
- 7B模型：约32层
- 13B模型：约40层
- 70B模型：约80层
