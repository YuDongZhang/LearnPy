# 5. 构建RAG链

## RAG链的组成

```
用户问题 → Retriever检索 → 拼接Prompt → LLM生成 → 回答
```

## Prompt模板

RAG的Prompt需要包含检索到的上下文：
```
基于以下参考资料回答问题。如果资料中没有相关信息，请说"我不确定"。

参考资料：
{context}

问题：{question}
```

## LangChain实现

LangChain提供了多种构建RAG链的方式：

### RetrievalQA（简单版）
一行代码搞定，适合快速原型。

### LCEL自定义链（灵活版）
用管道符组合各组件，完全可控。

### ConversationalRetrievalChain（对话版）
支持多轮对话，自动处理对话历史。

## 来源追溯

好的RAG系统应该告诉用户答案来自哪个文档：
- 返回source_documents
- 在回答中标注引用来源
- 提供文档链接

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 回答不准确 | 检索到的文档不相关 | 优化切分和Embedding |
| 回答太泛 | 上下文太多太杂 | 减少k值，加分数过滤 |
| 幻觉 | LLM没有遵循上下文 | 强化Prompt约束 |
| 回答不完整 | 相关信息被切分到不同块 | 增加chunk_overlap |
