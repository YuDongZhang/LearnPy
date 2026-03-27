# 3. Tokenizer设计

## 什么是Tokenizer

将文本切分为token（子词单元），是LLM的"眼睛"。

```
"我喜欢Python编程" → ["我", "喜欢", "Python", "编", "程"]
```

## 主流算法

| 算法 | 说明 | 使用模型 |
|------|------|---------|
| BPE | 字节对编码，最常用 | GPT, LLaMA |
| WordPiece | 类似BPE，Google出品 | BERT |
| Unigram | 概率模型 | T5, ALBERT |
| SentencePiece | 语言无关的BPE/Unigram | LLaMA, Qwen |

## BPE原理

1. 从字符级开始
2. 统计相邻字符对的频率
3. 合并最高频的字符对为新token
4. 重复直到达到目标词表大小

```
初始: ['l', 'o', 'w', 'e', 'r']
合并1: 'l'+'o' → 'lo'  → ['lo', 'w', 'e', 'r']
合并2: 'lo'+'w' → 'low' → ['low', 'e', 'r']
...
```

## 词表大小

| 模型 | 词表大小 |
|------|---------|
| GPT-2 | 50,257 |
| LLaMA 2 | 32,000 |
| LLaMA 3 | 128,256 |
| Qwen2.5 | 152,064 |

词表越大：
- 优势：编码效率高（同样文本用更少token）
- 劣势：Embedding层参数更多

## 特殊Token

| Token | 作用 |
|-------|------|
| BOS | 序列开始 |
| EOS | 序列结束 |
| PAD | 填充 |
| UNK | 未知token |
| 对话模板token | `<|im_start|>`, `<|im_end|>` 等 |
