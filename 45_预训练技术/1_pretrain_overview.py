"""
1. 预训练概述 - 代码示例
演示Next Token Prediction的训练目标。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def demo_next_token_prediction():
    """演示语言模型的训练目标：预测下一个token"""
    vocab = {"今": 0, "天": 1, "气": 2, "很": 3, "好": 4, "。": 5}
    inv_vocab = {v: k for k, v in vocab.items()}

    # 输入序列
    text = "今天天气很好。"
    tokens = [vocab[c] for c in text]
    print(f"原文: {text}")
    print(f"Token IDs: {tokens}")

    # 训练目标：输入前N个token，预测第N+1个
    input_ids = torch.tensor([tokens[:-1]])   # [今天天气很好]
    labels = torch.tensor([tokens[1:]])       # [天天气很好。]

    print(f"\n训练样本:")
    for i in range(len(tokens) - 1):
        inp = "".join(inv_vocab[t] for t in tokens[:i+1])
        lbl = inv_vocab[tokens[i+1]]
        print(f"  输入: '{inp}' → 预测: '{lbl}'")

    # 模拟一个简单模型
    model = nn.Embedding(len(vocab), 32)
    head = nn.Linear(32, len(vocab))

    logits = head(model(input_ids))  # (1, seq_len, vocab_size)
    loss = F.cross_entropy(logits.view(-1, len(vocab)), labels.view(-1))
    print(f"\n损失: {loss.item():.4f}")
    print(f"（随机初始化，理论最优loss = -ln(1/{len(vocab)}) = {-torch.log(torch.tensor(1/len(vocab))):.4f}）")
