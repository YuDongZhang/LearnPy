# 2. 文本预处理

## 为什么需要预处理

文本预处理是 NLP 的第一步，预处理质量直接影响模型效果：

- 数据清洗：去除噪声
- 分词：切分文本
- 去停用词：去除常见词
- 词形还原：还原为词根
- 词性标注：标注词性
- 命名实体识别：识别人名地名

## 字符串基本操作

```python
text = "  Hello, World!  "

text.strip()    # "Hello, World!"     去除两端空白
text.lower()    # "  hello, world!  " 转小写
text.split()    # ['Hello,', 'World!']
text.replace("World", "Python")
```

## 英文分词

| 方法 | 示例 |
|------|------|
| `split()` | 最简单，按空格切分 |
| 正则表达式 | `re.findall(r"\w+", text)` |
| NLTK | `word_tokenize` / `sent_tokenize`，能处理标点 |
| spaCy | 工业级，附带词性等标注 |

```python
import nltk
from nltk.tokenize import word_tokenize

words = word_tokenize("I love natural language processing")
# ['I', 'love', 'natural', 'language', 'processing']
```

## 中文分词

中文没有空格分隔，需要专门工具。最常用的是 jieba：

```python
import jieba

text = "我爱自然语言处理"

jieba.lcut(text)                # 精确模式
# ['我', '爱', '自然语言', '处理']

jieba.lcut(text, cut_all=True)  # 全模式
# ['我', '爱', '自然', '自然语言', '语言', '处理']

jieba.lcut_for_search(text)     # 搜索引擎模式
# ['我', '爱', '自然', '语言', '自然语言', '处理']
```

| 模式 | 特点 | 适用场景 |
|------|------|---------|
| 精确模式 | 最精确切分 | 文本分析 |
| 全模式 | 扫出所有可能的词 | 不推荐，存在歧义 |
| 搜索引擎模式 | 在精确模式基础上再切长词 | 搜索引擎建索引 |

自定义词典：`jieba.load_userdict("dict.txt")`（格式：词语 词频 词性）。其他工具：pkuseg、thulac。

## 词形处理

**词干提取 (Stemming)**：粗暴截断，可能得到非词。

```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
[stemmer.stem(w) for w in ["running", "ran", "runs", "runner"]]
# ['run', 'ran', 'run', 'runner']
```

**词形还原 (Lemmatization)**：借助词典还原为词根，更准确。

```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("running", pos="v")  # 'run'
```

## 去停用词

停用词是 "the"、"的" 这类高频无实际意义的词。

```python
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
words = ["I", "love", "natural", "language", "processing"]
filtered = [w for w in words if w.lower() not in stop_words]
# ['love', 'natural', 'language', 'processing']
```

中文停用词需要自己维护列表（的、了、在、是、我、有...）。

## 词向量化

**词袋模型 (Bag of Words)**：统计词频，忽略语序。

```python
from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    "I love natural language processing",
    "I love machine learning",
]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
```

**TF-IDF**：词频 × 逆文档频率，降低常见词权重，突出有区分度的词。

```python
from sklearn.feature_extraction.text import TfidfVectorizer

X = TfidfVectorizer().fit_transform(corpus)
```

## 词嵌入

Word2Vec 把词训练成密集向量，可以计算相似度：

```python
from gensim.models import Word2Vec

model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

vector = model.wv["love"]                  # 词向量
model.wv.most_similar("learning")          # 相似词
model.wv.most_similar(positive=["king"], negative=["man"])  # 词向量运算
```

其他：GloVe（斯坦福预训练向量）、FastText（支持子词，能处理未登录词）。

## 文本规范化

```python
import re

text = "I have 5 apples"
re.sub(r"\d+", "NUM", text)             # 数字 → NUM
re.sub(r"http\S+|www\.\S+", "URL", text)  # URL → URL
re.sub(r"[^a-zA-Z0-9\s]", "", text)     # 去特殊字符
re.sub(r"\s+", " ", text).strip()       # 去多余空格
```

## 数据增强

| 方法 | 说明 |
|------|------|
| 回译 | 翻译成其他语言再翻译回来 |
| 同义词替换 | 用 WordNet 同义词替换词 |
| 随机插入 | 随机位置插入同义词 |
| 随机交换 | 随机交换两个词的位置 |

## Transformers 分词器

现代预训练模型使用子词(subword)分词：

```python
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
tokens = tokenizer.tokenize("我爱自然语言处理")
# ['我', '爱', '自', '然', '语', '言', '处', '理']

encoded = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
```

## 代码

讲解对应的示例代码见 `2_text_preprocessing.py`。
