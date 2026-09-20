# 5. RAG 知识库构建

## 为什么需要 RAG

传统 LLM 的问题：知识有截止日期、存在幻觉、无法引用来源。

**RAG (Retrieval Augmented Generation)** 是检索 + 生成的混合架构，结合外部知识库：

| 优势 | 说明 |
|------|------|
| 实时知识 | 检索最新文档，不受训练截止日期限制 |
| 减少幻觉 | 基于检索到的内容回答 |
| 可追溯来源 | 答案可附带引用 |
| 成本效益高 | 无需重新训练模型 |

## 工作流程

```
1. 文档处理:   文档 -> 文本分割 -> 向量化 -> 存储
2. 用户查询:   用户问题 -> 向量化
3. 检索:       查询向量 -> 向量数据库 -> Top-K相关文档
4. 生成:       相关文档 + 问题 -> LLM -> 答案
5. 返回:       答案 + 引用来源
```

## 文本分割

分割策略：固定大小分割、按段落分割、语义分割。

关键参数：`chunk_size`（块大小）、`chunk_overlap`（重叠大小）、`separators`（分隔符）。

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", " ", ""]
)
texts = text_splitter.split_text(long_document)
```

## 向量化 (Embedding)

常用 Embedding 模型：OpenAI text-embedding-3-small/large、Cohere、sentence-transformers、开源 BGE/M3E。选择标准：语义理解能力、向量维度、推理速度、成本。

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)

doc_embeddings = embeddings.embed_documents([
    "Python是一种高级编程语言",
    "Java是一种面向对象编程语言"
])
query_embedding = embeddings.embed_query("Python和Java的区别")
```

## 向量数据库

| 数据库 | 特点 |
|--------|------|
| Pinecone | 云服务 |
| Weaviate | 开源 |
| Milvus | 开源 |
| Chroma | 轻量 |
| FAISS | Facebook 出品 |

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=texts, embedding=OpenAIEmbeddings()
)

results = vectorstore.similarity_search(query="Python的特点", k=3)
for doc in results:
    print(f"内容: {doc.page_content[:100]}")
    print(f"来源: {doc.metadata.get('source')}")
```

## 完整 RAG 实现

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. 加载文档 -> 2. 分割 -> 3. 向量存储
documents = TextLoader("document.txt").load()
texts = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50).split_documents(documents)
vectorstore = Chroma.from_documents(texts, OpenAIEmbeddings())

# 4. 检索器 -> 5. 问答链
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
    chain_type="stuff", retriever=retriever
)

# 6. 问答
result = qa_chain({"query": "文档中关于Python的描述是什么?"})
print(result["result"])
```

LangChain 表达式 (LCEL) 版本：

```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)
response = rag_chain.invoke("什么是Python?")
```

Prompt 要求模型只基于上下文回答，找不到答案时如实说明。

## 高级检索技术

| 技术 | 说明 |
|------|------|
| 混合检索 | 向量检索 + 关键词检索 (BM25)，互补优势 |
| 重排序 | Cross-Encoder 重排，更精确的相关性 |
| 查询改写 | 同义词扩展、分解复杂查询 |
| 元数据过滤 | 按时间/来源/类型过滤 |

## RAG 优化方向

- **分块优化**：调整块大小、增加重叠、滑动窗口
- **Embedding 优化**：选择合适模型、微调 Embedding
- **检索优化**：多路检索、递归检索、Parent Document
- **生成优化**：Context 压缩、Citations、Chain of Note

## 文档处理

PDF 处理：`PyPDFLoader("document.pdf")` 加载并分割，再走相同的分块流程。多模态 RAG：图像用 CLIP / 多模态 Embedding、表格结构化提取、视频帧提取 + 音频转录。

## 评估 RAG

- **检索指标**：Precision@K、Recall@K、MRR、NDCG
- **生成指标**：答案相关性、答案准确率、引用准确率
- **工具**：RAGAs、ARES、LangSmith

## 架构变体

| 变体 | 特点 |
|------|------|
| Self-RAG | 自适应检索、按需检索、反思机制 |
| Agentic RAG | 多步推理、工具使用、迭代优化 |
| Graph RAG | 知识图谱、关系推理 |
| SQL RAG | 数据库集成、结构化查询 |

## 生产环境部署

架构：前端界面 + API (FastAPI/Flask) + 索引服务（定时更新）+ 向量数据库 + LLM 服务。

优化：缓存策略、异步处理、限流、监控。安全：访问控制、数据加密、审计日志。

应用场景：企业知识库、客服系统、文档问答、产品搜索。

## 代码

讲解对应的示例代码见 `5_rag_knowledge_base.py`。
