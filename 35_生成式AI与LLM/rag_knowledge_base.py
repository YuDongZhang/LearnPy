"""
RAG知识库构建
============

介绍RAG（检索增强生成）技术的原理和实现。
"""

print("=" * 60)
print("1. RAG简介")
print("=" * 60)

print("""
RAG (Retrieval Augmented Generation):

定义:
  • 检索 + 生成的混合架构
  • 结合外部知识库
  • 解决LLM知识时效性问题

传统LLM问题:
  • 知识截止日期
  • 幻觉问题
  • 无法引用来源

RAG优势:
  • 实时知识
  • 减少幻觉
  • 可追溯来源
  • 成本效益高
""")

print()
print("=" * 60)
print("2. RAG工作流程")
print("=" * 60)

print("""
RAG流程:

1. 文档处理
   文档 -> 文本分割 -> 向量化 -> 存储

2. 用户查询
   用户问题 -> 向量化

3. 检索
   查询向量 -> 向量数据库 -> Top-K相关文档

4. 生成
   相关文档 + 问题 -> LLM -> 答案

5. 返回
   答案 + 引用来源
""")

print()
print("=" * 60)
print("3. 文本分割")
print("=" * 60)

print("""
3.1 分割策略

  • 固定大小分割
  • 按段落分割
  • 语义分割

3.2 分割参数

  • chunk_size: 块大小
  • chunk_overlap: 重叠大小
  • separators: 分隔符
""")

print('''
# LangChain文本分割
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\\n\\n", "\\n", "。", " ", ""]
)

texts = text_splitter.split_text(long_document)

for i, text in enumerate(texts):
    print(f"Chunk {i}: {text[:50]}...")
''')

print()
print("=" * 60)
print("4. 向量化")
print("=" * 60)

print("""
4.1 Embedding模型

  • OpenAI: text-embedding-3-small/large
  • Cohere
  • Hugging Face: sentence-transformers
  • 开源: BGE, M3E

4.2 选择标准

  • 语义理解能力
  • 向量维度
  • 推理速度
  • 成本
""")

print('''
from langchain_openai import OpenAIEmbeddings

# 初始化Embedding
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536
)

# 向量化文本
doc_embeddings = embeddings.embed_documents([
    "Python是一种高级编程语言",
    "Java是一种面向对象编程语言"
])

query_embedding = embeddings.embed_query("Python和Java的区别")

print(f"文档向量维度: {len(doc_embeddings[0])}")
print(f"查询向量维度: {len(query_embedding)}")
''')

print()
print("=" * 60)
print("5. 向量数据库")
print("=" * 60)

print("""
5.1 常见向量数据库

  • Pinecone: 云服务
  • Weaviate: 开源
  • Milvus: 开源
  • Chroma: 轻量
  • FAISS: Facebook

5.2 选择因素

  • 规模
  • 延迟
  • 成本
  • 易用性
""")

print('''
# 使用Chroma
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=texts,  # 分割后的文本
    embedding=OpenAIEmbeddings()
)

# 相似度检索
results = vectorstore.similarity_search(
    query="Python的特点",
    k=3  # 返回Top-3
)

for doc in results:
    print(f"内容: {doc.page_content[:100]}")
    print(f"来源: {doc.metadata.get('source')}")
    print()
''')

print()
print("=" * 60)
print("6. 完整RAG实现")
print("=" * 60)

print('''
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. 加载文档
loader = TextLoader("document.txt")
documents = loader.load()

# 2. 分割文本
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# 3. 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# 4. 创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. 创建问答链
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# 6. 问答
question = "文档中关于Python的描述是什么?"
result = qa_chain({"query": question})
print(result["result"])
''')

print()
print("=" * 60)
print("7. 高级检索技术")
print("=" * 60)

print("""
7.1 混合检索

  • 向量检索 + 关键词检索
  • BM25算法
  • 互补优势

7.2 重排序

  • Cross-Encoder重排
  • 更精确的相关性

7.3 查询改写

  • 同义词扩展
  • 分解复杂查询

7.4 元数据过滤

  • 按时间过滤
  • 按来源过滤
  • 按类型过滤
""")

print()
print("=" * 60)
print("8. RAG优化")
print("=" * 60)

print("""
8.1 分块优化

  • 调整块大小
  • 增加重叠
  • 滑动窗口

8.2 Embedding优化

  • 选择合适模型
  • 微调Embedding

8.3 检索优化

  • 多路检索
  • 递归检索
  • Parent Document

8.4 生成优化

  • Context压缩
  •  Citations
  • Chain of Note
""")

print()
print("=" * 60)
print("9. PDF文档处理")
print("=" * 60)

print('''
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 加载PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load_and_split()

# 分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

texts = text_splitter.split_documents(pages)

print(f"总页数: {len(pages)}")
print(f"总文本块: {len(texts)}")
''')

print()
print("=" * 60)
print("10. 多模态RAG")
print("=" * 60)

print("""
10.1 图像处理

  • 使用多模态Embedding
  • CLIP模型
  • 图像描述生成

10.2 表格处理

  • 表格检测
  • 结构化提取
  • 问答

10.3 视频处理

  • 帧提取
  • 音频转录
  • 时间索引
""")

print()
print("=" * 60)
print("11. 评估RAG")
print("=" * 60)

print("""
11.1 检索指标

  • Precision@K
  • Recall@K
  • MRR (Mean Reciprocal Rank)
  • NDCG

11.2 生成指标

  • 答案相关性
  • 答案准确率
  • 引用准确率

11.3 工具

  • RAGAs
  • ARES
  • LangSmith
""")

print()
print("=" * 60)
print("12. RAG架构变体")
print("=" * 60)

print("""
12.1 Self-RAG

  • 自适应检索
  • 按需检索
  • 反思机制

12.2 Agentic RAG

  • 多步推理
  • 工具使用
  • 迭代优化

12.3 Graph RAG

  • 知识图谱
  • 关系推理
  • 结构化知识

12.4 SQL RAG

  • 数据库集成
  • 结构化查询
  • 动态数据
""")

print()
print("=" * 60)
print("13. 生产环境部署")
print("=" * 60)

print("""
13.1 架构

  • 前端: 用户界面
  • API: FastAPI/Flask
  • 索引服务: 定时更新
  • 向量数据库
  • LLM服务

13.2 优化

  • 缓存策略
  • 异步处理
  • 限流
  • 监控

13.3 安全

  • 访问控制
  • 数据加密
  • 审计日志
""")

print()
print("=" * 60)
print("14. LangChain实现")
print("=" * 60)

print('''
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1. 加载向量存储
vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

# 2. 创建检索器
retriever = vectorstore.as_retriever()

# 3. 定义Prompt
template = """基于以下上下文回答问题。如果无法从上下文中找到答案，请如实说明。

上下文:
{context}

问题: {question}

回答:"""

prompt = PromptTemplate.from_template(template)

# 4. 创建链
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

def format_docs(docs):
    return "\\n\\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 5. 使用
response = rag_chain.invoke("什么是Python?")
print(response.content)
''')

print()
print("=" * 60)
print("15. RAG总结")
print("""
RAG技术要点:

✓ 核心流程:
  • 文档处理
  • 文本分割
  • 向量化
  • 向量存储
  • 检索
  • 生成

✓ 关键技术:
  • Embedding模型
  • 向量数据库
  • 文本分割策略
  • 检索优化

✓ 优化方向:
  • 混合检索
  • 重排序
  • 查询改写
  • 分块优化

✓ 应用场景:
  • 企业知识库
  • 客服系统
  • 文档问答
  • 产品搜索

✓ 工具:
  • LangChain
  • LlamaIndex
  • 向量数据库
""")
