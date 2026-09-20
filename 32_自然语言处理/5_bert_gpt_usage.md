# 5. BERT与GPT使用

## 预训练-微调范式

```
预训练: 在大规模语料上训练，学习通用语言表示（无监督）
微调:   在下游任务数据上微调（少量数据即可取得好效果）
```

优势：减少数据需求、效果好、可迁移。

## BERT vs GPT

| 方面 | BERT | GPT |
|------|------|-----|
| 发布 | 2018, Google | 2018, OpenAI |
| 结构 | 双向编码器 | 单向解码器（从左到右） |
| 预训练 | 掩码语言模型 (MLM) + 下一句预测 (NSP) | 自回归语言模型 |
| 擅长 | 分类、NER、问答 | 文本生成 |
| 规模 | Base: 1.1亿参数 / Large: 3.4亿 | GPT-3: 1750亿参数 |

ChatGPT 基于 GPT-3.5/GPT-4，通过 RLHF 对齐人类偏好，支持对话式交互。

## Hugging Face Transformers

最流行的 NLP 库：

```bash
pip install transformers torch
```

三大 API：`pipeline`（快速使用）、`AutoModel`（自动加载模型）、`AutoTokenizer`（自动加载分词器）。

## Pipeline快速上手

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

generator = pipeline("text-generation")
generator("Once upon a time", max_length=50)

ner = pipeline("ner", aggregation_strategy="simple")
ner("Elon Musk is the CEO of Tesla")
```

支持的任务：情感分析、文本生成、问答、命名实体识别、摘要、翻译等。

## 使用BERT

```python
from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")

inputs = tokenizer("我爱自然语言处理", return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

last_hidden_state = outputs.last_hidden_state  # (batch, seq_len, hidden_dim)
pooled_output = outputs.pooler_output          # (batch, hidden_dim) 句向量
```

## BERT微调

```python
from transformers import BertForSequenceClassification, Trainer, TrainingArguments

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=2
)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(model=model, args=training_args,
                  train_dataset=train_dataset, eval_dataset=eval_dataset)
trainer.train()
```

## 使用GPT生成文本

```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

input_ids = tokenizer.encode("Once upon a time", return_tensors="pt")
output = model.generate(
    input_ids,
    max_length=100,
    temperature=0.7,   # 越低越确定
    top_k=50,
    top_p=0.95,
)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

## 中文预训练模型

| 模型 | 名称 |
|------|------|
| 中文 BERT | `bert-base-chinese` |
| 中文 RoBERTa | `hfl/chinese-roberta-wwm-ext`（效果很好，推荐） |
| 中文 ELECTRA | `hfl/chinese-electra-180g-base-discriminator` |
| 中文 ALBERT | `voidful/albert_chinese_base` |
| 中文 GPT | `uer/gpt2-chinese` |

## 特征提取与句子相似度

```python
import torch.nn.functional as F

def similarity(text1, text2):
    emb1, _ = get_embeddings(text1)   # BERT pooler_output
    emb2, _ = get_embeddings(text2)
    return F.cosine_similarity(emb1, emb2).item()

similarity("I love cats", "I like kittens")    # 高
similarity("I love cats", "Python is great")   # 低
```

## 模型部署

```python
# 保存 / 加载
model.save_pretrained("./my_model")
model = AutoModel.from_pretrained("./my_model")

# 导出 ONNX 加速推理
torch.onnx.export(model, (dummy_input["input_ids"],), "model.onnx", ...)
```

## 大语言模型API

```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is deep learning?"}]
)
print(response.choices[0].message.content)
```

## 代码

讲解对应的示例代码见 `5_bert_gpt_usage.py`。
