"""
NLP 实战：情感分析项目
==================

使用多种方法实现情感分析项目。
由于环境中未安装 PyTorch/transformers，以下为示例代码展示。
"""

print("=" * 60)
print("1. 项目概述")
print("=" * 60)

print("""
项目: 情感分析 (Sentiment Analysis)

任务: 判断文本的情感倾向
  • 二分类: 正面 / 负面
  • 多分类: 正面 / 中性 / 负面

数据集:
  • 英文: IMDb, SST-2, YELP
  • 中文: ChnSentiCorp, JD

应用场景:
  • 舆情监控
  • 产品评价分析
  • 客服质量检测
""")

print()
print("=" * 60)
print("2. 数据探索")
print("=" * 60)

print("""
# 加载数据
import pandas as pd

# 英文数据
from datasets import load_dataset
dataset = load_dataset("imdb")

train_data = dataset["train"]
test_data = dataset["test"]

print(f"训练集大小: {len(train_data)}")
print(f"测试集大小: {len(test_data)}")

# 查看数据
print(train_data[0])
# {'text': 'I love this movie!', 'label': 1}

# 标签分布
labels = [example["label"] for example in train_data]
print(f"正面: {labels.count(1)}, 负面: {labels.count(0)}")

# 中文数据
# 数据格式: 评论, 标签
# 1: 正面, 0: 负面
""")

print()
print("=" * 60)
print("3. 方法对比")
print("=" * 60)

print("""
3.1 传统机器学习方法

  • 词袋模型 + SVM/朴素贝叶斯
  • TF-IDF + 逻辑回归
  • 优点: 快速, 可解释
  • 缺点: 效果一般

3.2 深度学习方法

  • LSTM/CNN 文本分类
  • 优点: 效果较好
  • 缺点: 需要训练

3.3 预训练模型

  • BERT/RoBERTa 微调
  • 优点: 效果最好
  • 缺点: 计算资源要求高

3.4 大语言模型

  • GPT/ChatGPT 零样本
  • 优点: 无需训练
  • 缺点: API 成本
""")

print()
print("=" * 60)
print("4. 方法一: TF-IDF + 逻辑回归")
print("=" * 60)

print('''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. 特征提取
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

# 2. 训练模型
model = LogisticRegression(max_iter=1000)
model.fit(X_train, train_labels)

# 3. 评估
predictions = model.predict(X_test)
accuracy = accuracy_score(test_labels, predictions)
print(f"准确率: {accuracy:.2%}")

# 4. 预测
def predict_sentiment(text):
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]
    return "Positive" if pred == 1 else "Negative", prob

text = "I love this movie!"
sentiment, prob = predict_sentiment(text)
print(f"文本: {text}")
print(f"情感: {sentiment}, 置信度: {prob.max():.2%}")
''')

print()
print("=" * 60)
print("5. 方法二: LSTM 文本分类")
print("=" * 60)

print('''
import torch
import torch.nn as nn

# 1. 定义模型
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, _) = self.lstm(embedded)
        # 双向: 拼接最后隐藏状态
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        hidden = self.dropout(hidden)
        return self.fc(hidden)

# 2. 数据处理
from torch.utils.data import Dataset, DataLoader

class TextDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len=128):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx][:self.max_len]
        indices = [self.vocab.get(w, 1) for w in text.split()]
        indices += [0] * (self.max_len - len(indices))
        return torch.tensor(indices), torch.tensor(self.labels[idx])

# 3. 训练
model = LSTMClassifier(vocab_size=10000, embed_dim=128, hidden_dim=128, num_classes=2)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练循环...
''')

print()
print("=" * 60)
print("6. 方法三: BERT 微调")
print("=" * 60)

print('''
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch

# 1. 加载预训练模型
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# 2. 预处理数据
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=256
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 3. 训练参数
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# 4. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# 5. 训练
trainer.train()

# 6. 评估
results = trainer.evaluate()
print(results)
''')

print()
print("=" * 60)
print("7. 方法四: Transformers Pipeline")
print("=" * 60)

print('''
from transformers import pipeline

# 使用预训练的情感分析模型
classifier = pipeline("sentiment-analysis")

# 英文
result = classifier("I love this product!")
print(result)
# [{'label': 'POSITIVE', 'score': 0.9998}]

# 中文
classifier = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-chinanews-chinese")
result = classifier("这个手机很好用，拍照很清晰")
print(result)

# 使用更精确的模型
classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
result = classifier("Just landed in LA! So excited!")
print(result)

# 批量预测
texts = ["Great movie!", "Terrible experience", "It's okay"]
results = classifier(texts)
for text, result in zip(texts, results):
    print(f"{text}: {result['label']} ({result['score']:.2%})")
''')

print()
print("=" * 60)
print("8. 方法五: ChatGPT API")
print("=" * 60)

print('''
import openai

openai.api_key = "your-api-key"

def analyze_sentiment_with_chatgpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a sentiment analyzer. Respond with POSITIVE, NEGATIVE, or NEUTRAL."
            },
            {"role": "user", "content": f"Analyze sentiment: {text}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content

# 测试
texts = [
    "I absolutely love this product! Best purchase ever!",
    "This is the worst experience I've ever had.",
    "The product is okay, nothing special."
]

for text in texts:
    sentiment = analyze_sentiment_with_chatgpt(text)
    print(f"Text: {text}")
    print(f"Sentiment: {sentiment}")
    print()
''')

print()
print("=" * 60)
print("9. 完整项目代码")
print("=" * 60)

print('''
# 完整情感分析项目

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. 数据准备
data = pd.read_csv("sentiment_data.csv")
X = data["text"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. 特征工程
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words="english",
    min_df=2
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 3. 模型训练
model = LogisticRegression(max_iter=1000, C=1.0)
model.fit(X_train_tfidf, y_train)

# 4. 评估
y_pred = model.predict(X_test_tfidf)
print("准确率:", accuracy_score(y_test, y_pred))
print("\\n分类报告:")
print(classification_report(y_test, y_pred, target_names=["Negative", "Positive"]))

# 5. 预测函数
def predict(text):
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]
    sentiment = "Positive" if pred == 1 else "Negative"
    return sentiment, prob[pred]

# 6. 测试
test_texts = [
    "I love this product!",
    "Terrible quality, not recommended",
    "Average product, nothing special"
]

for text in test_texts:
    sentiment, prob = predict(text)
    print(f"Text: {text}")
    print(f"Sentiment: {sentiment} ({prob:.2%})")
    print()
''')

print()
print("=" * 60)
print("10. 模型对比")
print("=" * 60)

print("""
模型性能对比 (IMDb 数据集):

| 方法           | 准确率  | 训练时间 | 资源需求 |
|---------------|---------|----------|----------|
| TF-IDF + LR   | ~88%    | 快       | 低       |
| LSTM          | ~90%    | 中       | 中       |
| CNN           | ~91%    | 中       | 中       |
| BERT          | ~93%    | 慢       | 高       |
| RoBERTa       | ~94%    | 慢       | 高       |
| GPT-3         | ~95%    | 无需训练 | API      |

选择建议:
  • 快速原型: TF-IDF + LR
  • 平衡效果和成本: LSTM/CNN
  • 最高精度: BERT/RoBERTa
  • 无需训练: GPT API
""")

print()
print("=" * 60)
print("11. 进阶技巧")
print("=" * 60)

print("""
11.1 数据增强

  • 回译: 翻译成其他语言再翻译回来
  • 同义词替换
  • 随机插入/删除

11.2 集成学习

  • 多个模型投票
  • 权重集成

11.3 域适应

  • 在相关领域数据上预训练
  • 领域自适应微调

11.4 自蒸馏

  • 大模型教小模型
  • 知识蒸馏
""")

print()
print("=" * 60)
print("12. 项目总结")
print("=" * 60)

print("""
情感分析项目要点:

✓ 1. 数据探索 - 了解数据分布和特点
✓ 2. 多种方法 - 从简单到复杂
✓ 3. 模型选择 - 根据资源和精度需求
✓ 4. 评估指标 - 准确率、F1、混淆矩阵
✓ 5. 部署上线 - Flask API / ONNX

下一步可以尝试:
  • 多类别情感 (正面/中性/负面)
  • Aspect-level 情感分析
  • 对话情感分析
  • 多模态情感分析

推荐学习资源:
  • Hugging Face 文档
  • 斯坦福 CS224n
  • Kaggle 情感分析竞赛
""")
