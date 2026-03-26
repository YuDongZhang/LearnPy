"""
3. Embedding与向量数据库 - 代码示例
演示Embedding生成和Chroma/FAISS的使用。
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document


# ============================================================
# 1. Embedding基础
# ============================================================
def demo_embedding():
    """生成Embedding并计算相似度"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    texts = ["Python是编程语言", "Java是编程语言", "今天天气很好"]
    vectors = embeddings.embed_documents(texts)

    print(f"向量维度: {len(vectors[0])}")

    # 计算余弦相似度
    import numpy as np
    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    print(f"Python vs Java: {cosine_sim(vectors[0], vectors[1]):.4f}")
    print(f"Python vs 天气: {cosine_sim(vectors[0], vectors[2]):.4f}")


# ============================================================
# 2. Chroma向量数据库
# ============================================================
def demo_chroma():
    """使用Chroma存储和检索"""
    docs = [
        Document(page_content="Python的装饰器用@符号应用", metadata={"source": "python.md"}),
        Document(page_content="GIL限制了多线程并行", metadata={"source": "python.md"}),
        Document(page_content="FastAPI是现代Web框架", metadata={"source": "web.md"}),
        Document(page_content="PyTorch用于深度学习", metadata={"source": "ai.md"}),
    ]

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 内存模式
    db = Chroma.from_documents(docs, embeddings)

    # 相似度检索
    results = db.similarity_search("什么是装饰器", k=2)
    print("Chroma检索:")
    for doc in results:
        print(f"  [{doc.metadata['source']}] {doc.page_content}")

    # 带分数检索
    results_with_score = db.similarity_search_with_score("深度学习框架", k=2)
    print("\n带分数检索:")
    for doc, score in results_with_score:
        print(f"  分数: {score:.4f} | {doc.page_content}")


# ============================================================
# 3. Chroma持久化
# ============================================================
def demo_chroma_persist():
    """Chroma持久化到磁盘"""
    docs = [Document(page_content="测试文档", metadata={"source": "test"})]
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 保存到磁盘
    db = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
    print("已保存到 ./chroma_db")

    # 从磁盘加载
    db2 = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    results = db2.similarity_search("测试", k=1)
    print(f"从磁盘加载并检索: {results[0].page_content}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. Embedding基础")
    print("=" * 60)
    demo_embedding()

    print("\n" + "=" * 60)
    print("2. Chroma向量数据库")
    print("=" * 60)
    demo_chroma()

    print("\n" + "=" * 60)
    print("3. Chroma持久化")
    print("=" * 60)
    demo_chroma_persist()
