# 6. NLP实战：情感分析

## 项目概述

**任务**：判断文本的情感倾向（二分类：正面/负面；或多分类：正面/中性/负面）。

- 数据集：英文 IMDb、SST-2、YELP；中文 ChnSentiCorp、京东评论
- 应用场景：舆情监控、产品评价分析、客服质量检测

## 方法对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| TF-IDF + 传统机器学习 | 快速、可解释 | 效果一般 |
| LSTM/CNN 深度学习 | 效果较好 | 需要训练 |
| BERT/RoBERTa 微调 | 效果最好 | 计算资源要求高 |
| GPT/ChatGPT 零样本 | 无需训练 | API 成本 |

## 方法一：TF-IDF + 逻辑回归

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

vectorizer = TfidfVectorizer(max_features=10000,
                             ngram_range=(1, 2), stop_words="english")
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, train_labels)

def predict_sentiment(text):
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0]
    return "Positive" if pred == 1 else "Negative", prob.max()
```

## 方法二：LSTM文本分类

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim,
                            batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, _) = self.lstm(embedded)
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.fc(self.dropout(hidden))
```

## 方法三：BERT微调

```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=2
)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length",
                     truncation=True, max_length=256)

tokenized = dataset.map(tokenize_function, batched=True)
trainer = Trainer(model=model, args=training_args,
                  train_dataset=tokenized["train"])
trainer.train()
```

## 方法四：Pipeline直接预测

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# 中文模型
classifier = pipeline("sentiment-analysis",
                      model="uer/roberta-base-finetuned-chinanews-chinese")
classifier("这个手机很好用，拍照很清晰")
```

## 方法五：ChatGPT API

```python
def analyze_sentiment_with_chatgpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a sentiment analyzer. Respond with POSITIVE, NEGATIVE, or NEUTRAL."},
            {"role": "user", "content": f"Analyze sentiment: {text}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content
```

## 模型性能对比

IMDb 数据集上的大致水平：

| 方法 | 准确率 | 训练时间 | 资源需求 |
|------|--------|----------|----------|
| TF-IDF + LR | ~88% | 快 | 低 |
| LSTM | ~90% | 中 | 中 |
| CNN | ~91% | 中 | 中 |
| BERT | ~93% | 慢 | 高 |
| RoBERTa | ~94% | 慢 | 高 |
| GPT-3 | ~95% | 无需训练 | API |

选择建议：快速原型用 TF-IDF + LR；平衡效果和成本用 LSTM/CNN；最高精度用 BERT/RoBERTa；不想训练用 GPT API。

## 进阶技巧

- 数据增强：回译、同义词替换、随机插入/删除
- 集成学习：多模型投票、权重集成
- 域适应：在相关领域数据上继续预训练
- 知识蒸馏：大模型教小模型

## 项目总结

1. 数据探索：了解数据分布和特点
2. 多种方法：从简单到复杂逐步尝试
3. 模型选择：根据资源和精度需求权衡
4. 评估：准确率、F1、混淆矩阵
5. 部署：Flask API / ONNX

下一步：多类别情感、Aspect-level 情感分析、对话情感分析、多模态情感分析。

## 代码

讲解对应的示例代码见 `6_nlp_project.py`。
