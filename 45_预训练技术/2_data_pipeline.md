# 2. 数据收集与清洗

## 预训练数据来源

| 来源 | 说明 | 示例 |
|------|------|------|
| 网页 | Common Crawl爬取 | 数万亿token |
| 书籍 | 电子书 | Books3, Gutenberg |
| 代码 | GitHub | The Stack, StarCoder |
| 论文 | 学术论文 | ArXiv, S2ORC |
| 百科 | Wikipedia | 多语言 |
| 对话 | 社交媒体 | Reddit, StackOverflow |

## 数据清洗流程

```
原始数据 → 去重 → 语言过滤 → 质量过滤 → 敏感信息过滤 → 混合比例 → 最终数据
```

### 去重
- 精确去重：hash去重
- 模糊去重：MinHash + LSH
- 文档级和段落级都要去重

### 质量过滤
- 困惑度过滤（用小模型打分）
- 规则过滤（长度、特殊字符比例）
- 分类器过滤（训练质量分类器）

### 敏感信息
- 个人信息（姓名、电话、邮箱）
- 有害内容
- 版权内容

## 数据混合比例

不同来源的数据按比例混合：
```
网页: 60%
代码: 15%
书籍: 10%
论文: 5%
百科: 5%
对话: 5%
```
比例对模型能力有很大影响。

## 开源数据集

| 数据集 | 大小 | 说明 |
|--------|------|------|
| RedPajama | 1.2T tokens | LLaMA训练数据复现 |
| The Pile | 800GB | EleutherAI |
| FineWeb | 15T tokens | HuggingFace |
| SlimPajama | 627B tokens | 清洗版RedPajama |
