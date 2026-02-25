"""
BERT/GPT 使用指南
==============

介绍 BERT、GPT 等预训练模型的使用方法。
由于环境中未安装 transformers，以下为示例代码展示。
"""

print("=" * 60)
print("1. 预训练模型概述")
print("=" * 60)

print("""
预训练-微调范式:

  预训练阶段:
    • 在大规模语料上训练
    • 学习通用语言表示
    • 无监督任务: 语言模型、掩码预测

  微调阶段:
    • 在下游任务数据上微调
    • 少量数据就能取得好效果
    • 迁移学习

优势:
  ✓ 减少数据需求
  ✓ 效果好
  ✓ 可迁移
""")

print()
print("=" * 60)
print("2. BERT 简介")
print("=" * 60)

print("""
BERT (Bidirectional Encoder Representations from Transformers):

发布: 2018, Google
论文: "BERT: Pre-training of Deep Bidirectional Transformers"

核心特点:
  • 双向编码器
  • 掩码语言模型 (MLM)
  • 下一句预测 (NSP)

模型规模:
  • BERT-Base: 12层, 768维, 1.1亿参数
  • BERT-Large: 24层, 1024维, 3.4亿参数

应用场景:
  • 文本分类
  • 命名实体识别
  • 问答系统
  • 句子对关系
""")

print()
print("=" * 60)
print("3. GPT 简介")
print("=" * 60)

print("""
GPT (Generative Pre-training):

发布: 2018, OpenAI
发展: GPT-1 → GPT-2 → GPT-3 → GPT-4

核心特点:
  • 单向解码器 (从左到右)
  • 自回归语言模型
  • 零样本/少样本学习

GPT-3:
  • 1750亿参数
  • 强大的零样本能力
  • 可以写代码、对话、创作

ChatGPT:
  • 基于 GPT-3.5/GPT-4
  • RLHF 对齐人类
  • 对话式交互
""")

print()
print("=" * 60)
print("4. Hugging Face Transformers")
print("=" * 60)

print("""
最流行的 NLP 库:

  pip install transformers torch

常用 API:
  • pipeline: 快速使用模型
  • AutoModel: 自动加载模型
  • AutoTokenizer: 自动加载分词器

模型搜索:
  https://huggingface.co/models
""")

print()
print("=" * 60)
print("5. 使用 Pipeline")
print("=" * 60)

print('''
from transformers import pipeline

# 情感分析
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# 指定模型
classifier = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-chinanews-chinese")

# 文本生成
generator = pipeline("text-generation")
result = generator("Once upon a time", max_length=50, num_return_sequences=2)

# 问答系统
question_answerer = pipeline("question-answering")
result = question_answerer(
    question="What is AI?",
    context="Artificial intelligence is a field of computer science."
)

# 命名实体识别
ner = pipeline("ner", aggregation_strategy="simple")
result = ner("Elon Musk is the CEO of Tesla")

# 文本摘要
summarizer = pipeline("summarization")
result = summarizer("Long text to summarize...")

# 翻译
translator = pipeline("translation_en_to_fr")
result = translator("Hello world")
''')

print()
print("=" * 60)
print("6. 使用 BERT")
print("=" * 60)

print('''
from transformers import BertTokenizer, BertModel
import torch

# 加载模型和分词器
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# 中文模型
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")

# 编码文本
text = "I love natural language processing"
inputs = tokenizer(text, return_tensors="pt")

# 前向传播
with torch.no_grad():
    outputs = model(**inputs)

# 获取最后一层隐藏状态
last_hidden_state = outputs.last_hidden_state
# shape: (batch, seq_len, hidden_dim)

# 池化得到句子向量
pooled_output = outputs.pooler_output
# shape: (batch, hidden_dim)
''')

print()
print("=" * 60)
print("7. BERT 微调")
print("=" * 60)

print('''
from transformers import BertForSequenceClassification, Trainer, TrainingArguments

# 加载预训练模型用于分类
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# 训练参数
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

# 训练
trainer.train()

# 预测
predictions = trainer.predict(test_dataset)
preds = predictions.predictions.argmax(-1)
''')

print()
print("=" * 60)
print("8. 使用 GPT")
print("=" * 60)

print('''
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# 加载模型
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# 设置 pad token
tokenizer.pad_token = tokenizer.eos_token

# 文本生成
input_text = "Once upon a time"
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# 生成
output = model.generate(
    input_ids,
    max_length=100,
    num_return_sequences=1,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
)

generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)

# 中文模型
tokenizer = GPT2Tokenizer.from_pretrained("uer/gpt2-chinese")
model = GPT2LMHeadModel.from_pretrained("uer/gpt2-chinese")
''')

print()
print("=" * 60)
print("9. 使用 RoBERTa")
print("=" * 60)

print('''
from transformers import RobertaTokenizer, RobertaModel

# RoBERTa - BERT 的改进版
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaModel.from_pretrained("roberta-base")

# 使用方式类似 BERT
text = "I love NLP"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

# 微调进行情感分析
from transformers import RobertaForSequenceClassification

model = RobertaForSequenceClassification.from_pretrained(
    "roberta-base",
    num_labels=2
)
''')

print()
print("=" * 60)
print("10. 中文预训练模型")
print("=" * 60)

print('''
# 中文 BERT
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")

text = "我爱自然语言处理"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

# 中文 RoBERTa
from transformers import RobertaTokenizer, RobertaModel

tokenizer = BertTokenizer.from_pretrained("hfl/chinese-roberta-wwm-ext")
model = BertModel.from_pretrained("hfl/chinese-roberta-wwm-ext")

# 哈工大 RoBERTa-wwm-ext
# 效果很好, 强烈推荐!

# 中文 ELECTRA
from transformers import ElectraTokenizer, ElectraModel

tokenizer = ElectraTokenizer.from_pretrained("hfl/chinese-electra-180g-base-discriminator")
model = ElectraModel.from_pretrained("hfl/chinese-electra-180g-base-discriminator")

# 中文 ALBERT
from transformers import AlbertTokenizer, AlbertModel

tokenizer = AlbertTokenizer.from_pretrained("voidful/albert_chinese_base")
model = AlbertModel.from_pretrained("voidful/albert_chinese_base")
''')

print()
print("=" * 60)
print("11. 特征提取")
print("=" * 60)

print('''
from transformers import AutoTokenizer, AutoModel
import torch

# 使用 BERT 提取词向量
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # CLS 向量 (句子表示)
    cls_embedding = outputs.pooler_output
    # 词向量
    word_embeddings = outputs.last_hidden_state
    return cls_embedding, word_embeddings

# 句子相似度
import torch.nn.functional as F

def similarity(text1, text2):
    emb1, _ = get_embeddings(text1)
    emb2, _ = get_embeddings(text2)
    # 余弦相似度
    cos_sim = F.cosine_similarity(emb1, emb2)
    return cos_sim.item()

print(similarity("I love cats", "I like kittens"))
print(similarity("I love cats", "Python is great"))
''')

print()
print("=" * 60)
print("12. 模型部署")
print("=" * 60)

print('''
# 12.1 保存模型
model.save_pretrained("./my_model")
tokenizer.save_pretrained("./my_model")

# 12.2 加载模型
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("./my_model")
tokenizer = AutoTokenizer.from_pretrained("./my_model")

# 12.3 导出 ONNX
from transformers import AutoModelForSequenceClassification
import torch.onnx

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
dummy_input = tokenizer("Hello", return_tensors="pt")

torch.onnx.export(
    model,
    (dummy_input["input_ids"],),
    "model.onnx",
    input_names=["input_ids"],
    output_names=["logits"],
    dynamic_axes={"input_ids": {0: "batch_size"}, "logits": {0: "batch_size"}}
)

# 12.4 使用 ONNX Runtime
import onnxruntime as ort

ort_session = ort.InferenceSession("model.onnx")
outputs = ort_session.run(None, {"input_ids": dummy_input["input_ids"].numpy()})
''')

print()
print("=" * 60)
print("13. 大语言模型使用")
print("=" * 60)

print('''
# 使用 OpenAI API (需要 API Key)
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is deep learning?"}
    ]
)

print(response.choices[0].message.content)

# 使用 GPT-4
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Explain neural networks"}
    ]
)

# 使用 Hugging Face Inference API
from transformers import pipeline

generator = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf")
''')

print()
print("=" * 60)
print("14. 实战: 情感分析")
print("=" * 60)

print('''
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# 方式1: 使用预训练 pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("This movie is amazing!")
print(result)

# 方式2: 使用自定义模型
model_name = "uer/roberta-base-finetuned-chinanews-chinese"
classifier = pipeline("sentiment-analysis", model=model_name)
result = classifier("这个产品很好用")
print(result)

# 方式3: 完整微调流程
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer

# 加载数据
dataset = load_dataset("imdb", split="train[:1000]")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

dataset = dataset.map(tokenize, batched=True)

# 加载模型
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# 训练
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,
    per_device_train_batch_size=16,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()
''')
