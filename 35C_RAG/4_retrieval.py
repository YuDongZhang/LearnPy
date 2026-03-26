"""
4. 检索策略 - 代码示例
演示不同的检索方式：相似度、MMR、带分数过滤。
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document


def build_db():
    """构建测试向量数据库"""
    docs = [
        Document(page_content="Python的GIL限制了多线程并行执行，CPU密集型任务建议用多进程。"),
        Document(page_content="Python的多线程适合IO密集型任务，如网络请求和文件读写。"),
        Document(page_content="Python的asyncio提供了异步编程支持，适合高并发IO操作。"),
        Document(page_content="Python的装饰器是修改函数行为的语法糖，使用@符号。"),
        Document(page_content="Python的生成器使用yield关键字，惰性产生值，节省内存。"),
        Document(page_content="multiprocessing模块可以绑过GIL限制，实现真正的并行计算。"),
    ]
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_documents(docs, embeddings)


# ============================================================
# 1. 基础相似度检索
# ============================================================
def demo_similarity(db):
    query = "Python多线程有什么限制？"
    results = db.similarity_search(query, k=3)
    print(f"查询: {query}")
    for i, doc in enumerate(results):
        print(f"  [{i+1}] {doc.page_content}")


# ============================================================
# 2. MMR检索（平衡相关性和多样性）
# ============================================================
def demo_mmr(db):
    query = "Python的并发编程"
    results = db.max_marginal_relevance_search(query, k=3, fetch_k=6)
    print(f"MMR查询: {query}")
    for i, doc in enumerate(results):
        print(f"  [{i+1}] {doc.page_content}")


# ============================================================
# 3. 带分数过滤
# ============================================================
def demo_score_filter(db):
    query = "装饰器怎么用"
    results = db.similarity_search_with_score(query, k=4)
    print(f"带分数查询: {query}")
    for doc, score in results:
        status = "✓" if score < 0.5 else "✗"
        print(f"  {status} 分数: {score:.4f} | {doc.page_content[:40]}...")


# ============================================================
# 4. 转为Retriever
# ============================================================
def demo_retriever(db):
    """将向量数据库转为Retriever，方便接入RAG链"""
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 6}
    )
    results = retriever.invoke("Python并发")
    print(f"Retriever结果: {len(results)} 个文档")
    for doc in results:
        print(f"  {doc.page_content[:50]}...")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    db = build_db()

    print("=" * 60)
    print("1. 基础相似度检索")
    print("=" * 60)
    demo_similarity(db)

    print("\n" + "=" * 60)
    print("2. MMR检索")
    print("=" * 60)
    demo_mmr(db)

    print("\n" + "=" * 60)
    print("3. 带分数过滤")
    print("=" * 60)
    demo_score_filter(db)

    print("\n" + "=" * 60)
    print("4. Retriever")
    print("=" * 60)
    demo_retriever(db)
