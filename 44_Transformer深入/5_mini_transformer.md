# 5. 从零搭建mini GPT

## 目标

用PyTorch从零实现一个mini GPT模型，包含：
- Token Embedding + Position Embedding
- N个Transformer Block（Causal Attention + FFN）
- LM Head（预测下一个token）

## 模型配置

```python
config = {
    "vocab_size": 1000,
    "d_model": 128,
    "num_heads": 4,
    "num_layers": 4,
    "d_ff": 512,
    "max_seq_len": 256,
    "dropout": 0.1,
}
```

这是一个很小的模型（约2M参数），用于学习理解架构。

## 组件

1. `CausalSelfAttention` — 因果多头注意力
2. `FeedForward` — 前馈网络
3. `TransformerBlock` — Attention + FFN + LayerNorm + 残差
4. `MiniGPT` — 完整模型

## 训练

用简单的文本数据训练，目标是预测下一个token（语言模型）：
```
输入: [今, 天, 天, 气]
标签: [天, 天, 气, 好]
损失: CrossEntropyLoss
```

## 运行

```bash
python 5_mini_transformer.py
```

会在简单数据上训练几个epoch，展示loss下降和文本生成效果。
