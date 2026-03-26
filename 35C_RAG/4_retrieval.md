# 4. 检索策略

## 基础检索

最简单的方式：向量相似度检索Top-K。

```python
results = vectorstore.similarity_search(query, k=4)
```

## 进阶检索策略

### MMR（最大边际相关性）
在相关性和多样性之间取平衡，避免检索到重复内容：
```python
results = vectorstore.max_marginal_relevance_search(query, k=4, fetch_k=20)
```

### 带分数过滤
只返回相似度超过阈值的结果：
```python
results = vectorstore.similarity_search_with_score(query, k=4)
# 过滤低分结果
filtered = [(doc, score) for doc, score in results if score > 0.7]
```

### 混合检索
结合关键词搜索（BM25）和向量搜索：
- 关键词搜索：精确匹配，适合专有名词
- 向量搜索：语义匹配，适合自然语言
- 混合：两者结合，效果最好

### 多查询检索
用LLM将原始问题改写为多个不同角度的查询，分别检索后合并去重。

### 上下文压缩
检索后用LLM对文档进行压缩，只保留与问题相关的部分。

## 检索参数调优

| 参数 | 说明 | 建议 |
|------|------|------|
| k（返回数量） | 返回多少个文档 | 3-5，太多会引入噪音 |
| chunk_size | 文档块大小 | 500-1000字符 |
| chunk_overlap | 重叠大小 | chunk_size的10-20% |
| score_threshold | 相似度阈值 | 根据实际调整 |

## 检索质量评估

- 命中率（Hit Rate）：正确答案是否在检索结果中
- MRR（Mean Reciprocal Rank）：正确答案的排名
- 人工抽检：随机抽样检查检索质量
