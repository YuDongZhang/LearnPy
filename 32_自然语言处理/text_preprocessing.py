"""
文本预处理技术
============

介绍 NLP 中的文本预处理技术，包括分词、词向量化等。
"""

print("=" * 60)
print("1. 文本预处理概述")
print("=" * 60)

print("""
文本预处理是 NLP 的第一步，包括:

• 数据清洗: 去除噪声
• 分词: 切分文本
• 去停用词: 去除常见词
• 词形还原: 还原为词根
• 词性标注: 标注词性
• 命名实体识别: 识别人名地名

预处理质量直接影响模型效果!
""")

print()
print("=" * 60)
print("2. 字符串基本操作")
print("=" * 60)

print("""
# Python 字符串操作

text = "  Hello, World!  "

# 大小写
text.upper()      # "  HELLO, WORLD!  "
text.lower()      # "  hello, world!  "

# 去除空白
text.strip()      # "Hello, World!"
text.lstrip()     # "Hello, World!  "
text.rstrip()     # "  Hello, World!"

# 分割
text.split()      # ['Hello,', 'World!']

# 替换
text.replace("World", "Python")  # "  Hello, Python!  "

# 格式化
name = "Alice"
age = 25
f"My name is {name}, age {age}"
# "My name is Alice, age 25"
""")

print()
print("=" * 60)
print("3. 英文分词")
print("=" * 60)

print("""
3.1 简单分词 - split()

text = "I love natural language processing"
words = text.split()
# ['I', 'love', 'natural', 'language', 'processing']

3.2 正则表达式分词

import re

# 按单词分词
tokens = re.findall(r"\\w+", text)

# 按句子分词
sentences = re.split(r"[.!?]+", text)

3.3 NLTK 分词

import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize, sent_tokenize

words = word_tokenize(text)
# ['I', 'love', 'natural', 'language', 'processing']

sentences = sent_tokenize(text)

3.4 spaCy 分词

import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp(text)
tokens = [token.text for token in doc]
""")

print()
print("=" * 60)
print("4. 中文分词")
print("=" * 60)

print("""
4.1 jieba 分词

import jieba

text = "我爱自然语言处理"

# 精确模式
words = jieba.lcut(text)
# ['我', '爱', '自然语言', '处理']

# 全模式
words = jieba.lcut(text, cut_all=True)
# ['我', '爱', '自然', '自然语言', '语言', '处理']

# 搜索引擎模式
words = jieba.lcut_for_search(text)
# ['我', '爱', '自然', '语言', '自然语言', '处理']

4.2 添加自定义词典

jieba.load_userdict("dict.txt")
# 格式: 词语 词频 词性

4.3 pkuseg 分词

import pkuseg
seg = pkuseg.pkuseg()
words = seg.cut(text)

4.4 thulac 分词

import thulac
thu = thulac.thulac(seg_only=True)
words = thu.cut(text)
""")

print()
print("=" * 60)
print("5. 词形处理")
print("=" * 60)

print("""
5.1 词干提取 (Stemming)

from nltk.stem import PorterStemmer, LancasterStemmer

stemmer = PorterStemmer()
words = ["running", "ran", "runs", "runner"]

stemmed = [stemmer.stem(w) for w in words]
# ['run', 'ran', 'run', 'runner']

5.2 词形还原 (Lemmatization)

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
words = ["running", "ran", "better"]

lemmatized = [lemmatizer.lemmatize(w) for w in words]
# ['running', 'ran', 'better']

# 指定词性
lemmatizer.lemmatize("running", pos="v")  # 'run'

5.3 词性标注

from nltk import pos_tag

words = ["I", "love", "Python"]
tagged = pos_tag(words)
# [('I', 'PRP'), ('love', 'VBP'), ('Python', 'NNP')]
""")

print()
print("=" * 60)
print("6. 去停用词")
print("=" * 60)

print("""
6.1 英文停用词

from nltk.corpus import stopwords

# 下载停用词
nltk.download('stopwords')

# 获取停用词列表
stop_words = set(stopwords.words('english'))

# 过滤
words = ["I", "love", "natural", "language", "processing"]
filtered = [w for w in words if w.lower() not in stop_words]
# ['love', 'natural', 'language', 'processing']

6.2 自定义停用词

custom_stop_words = {"the", "a", "an", "is", "are"}
stop_words = set(stopwords.words('english')) | custom_stop_words

6.3 中文停用词

# 常用中文停用词
chinese_stopwords = set([
    '的', '了', '在', '是', '我', '有', '和', '就',
    '不', '人', '都', '一', '一个', '上', '也', '很',
    '到', '说', '要', '去', '你', '会', '着', '没有'
])

words = ['我', '爱', '自然语言', '处理']
filtered = [w for w in words if w not in chinese_stopwords]
# ['爱', '自然语言', '处理']
""")

print()
print("=" * 60)
print("7. 词向量化")
print("=" * 60)

print("""
7.1 词袋模型 (Bag of Words)

from sklearn.feature_extraction.text import CountVectorizer

corpus = [
    "I love natural language processing",
    "Natural language processing is great",
    "I love machine learning"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

print(vectorizer.get_feature_names_out())
# ['great', 'is', 'learning', 'love', 'machine', 'natural', 'processing']

print(X.toarray())
# [[0 0 0 1 0 1 1]
#  [1 1 0 0 0 1 1]
#  [0 0 1 1 1 0 0]]

7.2 TF-IDF

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

print(X.toarray())

7.3 Hashing Vectorizer

from sklearn.feature_extraction.text import HashingVectorizer

vectorizer = HashingVectorizer(n_features=1000)
X = vectorizer.fit_transform(corpus)
""")

print()
print("=" * 60)
print("8. 词嵌入")
print("=" * 60)

print("""
8.1 Word2Vec

from gensim.models import Word2Vec

sentences = [
    ["I", "love", "natural", "language", "processing"],
    ["I", "love", "machine", "learning"],
    ["Deep", "learning", "is", "great"]
]

# 训练模型
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# 获取词向量
vector = model.wv["love"]

# 找相似词
similar = model.wv.most_similar("learning")
# [('great', 0.12), ('natural', 0.08), ...]

# 词向量运算
result = model.wv.most_similar(positive=["king"], negative=["man"])
# queen, royalty...

8.2 GloVe

# 需要下载预训练向量
# https://nlp.stanford.edu/projects/glovec

8.3 FastText

from gensim.models import FastText

model = FastText(sentences, vector_size=100, window=5, min_count=1)
""")

print()
print("=" * 60)
print("9. 文本规范化")
print("=" * 60)

print("""
9.1 处理数字

import re

text = "I have 5 apples and 10 oranges"

# 将数字替换为标记
text = re.sub(r"\\d+", "NUM", text)
# "I have NUM apples and NUM oranges"

9.2 处理 URL 和邮箱

text = "Visit https://example.com or email test@test.com"

text = re.sub(r"http\\S+|www\\.\\S+", "URL", text)
text = re.sub(r"\\S+@\\S+", "EMAIL", text)

9.3 处理特殊字符

# 只保留字母数字和空格
text = re.sub(r"[^a-zA-Z0-9\\s]", "", text)

# 去除多余空格
text = re.sub(r"\\s+", " ", text).strip()

9.4 处理大小写

# 全部小写
text = text.lower()

# 首字母大写
text = text.title()
""")

print()
print("=" * 60)
print("10. 数据增强")
print("="  * 60)

print("""
10.1 回译法 (Back Translation)

# 翻译成其他语言再翻译回来
# 需要翻译 API

10.2 同义词替换

from nltk.corpus import wordnet

def synonym_replacement(text, n=1):
    words = text.split()
    for _ in range(n):
        word = random.choice(words)
        synonyms = wordnet.synsets(word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            words = [synonym if w == word else w for w in words]
    return " ".join(words)

10.3 随机插入

def random_insertion(text, n=1):
    words = text.split()
    for _ in range(n):
        word = random.choice(words)
        synonyms = wordnet.synsets(word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, synonym)
    return " ".join(words)

10.4 随机交换

def random_swap(text, n=1):
    words = text.split()
    for _ in range(n):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]
    return " ".join(words)
""")

print()
print("=" * 60)
print("11. 完整预处理流程")
print("=" * 60)

print("""
import re
import jieba
from collections import Counter

def preprocess_text(text):
    # 1. 转小写
    text = text.lower()

    # 2. 去除 URL
    text = re.sub(r"http\\S+|www\\.\\S+", "", text)

    # 3. 去除特殊字符
    text = re.sub(r"[^a-zA-Z0-9\\s]", " ", text)

    # 4. 去除多余空格
    text = re.sub(r"\\s+", " ", text).strip()

    # 5. 分词
    # 中文
    # words = jieba.lcut(text)

    # 英文
    words = text.split()

    # 6. 去停用词
    # stop_words = set(stopwords.words('english'))
    # words = [w for w in words if w not in stop_words]

    return words

# 示例
text = "Visit https://example.com! I love  AI and Machine Learning."
result = preprocess_text(text)
print(result)
# ['visit', 'i', 'love', 'ai', 'and', 'machine', 'learning']
""")

print()
print("=" * 60)
print("12. 使用 transformers 分词器")
print("=" * 60)

print("""
from transformers import BertTokenizer, AutoTokenizer

# 使用 BERT 分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

text = "I love natural language processing"

# 分词
tokens = tokenizer.tokenize(text)
# ['i', 'love', 'natural', 'language', 'processing']

# 编码
encoded = tokenizer.encode(text)
# [101, 1045, 2293, 3018, 2653, 6365, 102]

# 解码
decoded = tokenizer.decode(encoded)

# 中文分词
tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese')
text = "我爱自然语言处理"
tokens = tokenizer.tokenize(text)
# ['我', '爱', '自', '然', '语', '言', '处', '理']

# 批量编码
sentences = ["I love NLP", "Deep learning is great"]
encoded = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")

# Attention Mask
# attention_mask = encoded["attention_mask"]
""")
