"""
5. 构建RAG链 - 代码示例
演示用LangChain构建完整的RAG问答链。
"""

import os
from dotenv import load_dotenv

load_dotenv()

# 本机装了 TensorFlow，transformers 导入时会去探测它、并因 Keras 3 版本冲突报错。
# 这里只用 PyTorch 后端，所以在 import transformers 之前显式关掉 TF 探测。
os.environ.setdefault("USE_TF", "0")

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document, StrOutputParser
from langchain_core.runnables import RunnablePassthrough


LLM_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")


def get_embeddings():
    """本地中文 Embedding 模型（512维），首次运行会自动下载约 100MB"""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )


# ============================================================
# 准备向量数据库
# ============================================================
_DB = None


def build_db():
    """构建测试向量数据库（进程内只构建一次）

    注意：Chroma 的内存模式默认使用名为 "langchain" 的 collection，同一进程里
    再次调用 from_documents 会把文档**追加**进去而不是重建（实测 6 条 → 12 条）。
    所以这里缓存起来只构建一次，否则检索结果里会出现同一条文档的多份副本。
    """
    global _DB
    if _DB is None:
        docs = [
            Document(page_content="Python的GIL限制了多线程并行。CPU密集型用multiprocessing。", metadata={"source": "concurrency.md"}),
            Document(page_content="asyncio提供异步编程，适合高并发IO。使用async/await语法。", metadata={"source": "async.md"}),
            Document(page_content="装饰器用@符号应用，本质是高阶函数。常用于日志、缓存。", metadata={"source": "decorator.md"}),
            Document(page_content="生成器用yield产生值，惰性求值，适合大数据处理。", metadata={"source": "generator.md"}),
            Document(page_content="FastAPI基于类型注解，自动生成API文档，性能优秀。", metadata={"source": "web.md"}),
        ]
        _DB = Chroma.from_documents(docs, get_embeddings())
    return _DB


# ============================================================
# 1. LCEL方式构建RAG链（推荐）
# ============================================================
def demo_rag_chain():
    """用LCEL管道构建RAG链"""
    db = build_db()
    retriever = db.as_retriever(search_kwargs={"k": 2})
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    # RAG Prompt
    prompt = ChatPromptTemplate.from_template(
        "基于以下参考资料回答问题。如果资料中没有相关信息，请说'我不确定'。\n\n"
        "参考资料:\n{context}\n\n"
        "问题: {question}"
    )

    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)

    # 构建链
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 测试
    questions = ["Python的GIL是什么？", "FastAPI有什么特点？", "Go语言怎么样？"]
    for q in questions:
        answer = chain.invoke(q)
        print(f"问: {q}\n答: {answer}\n")


# ============================================================
# 2. 带来源追溯的RAG
# ============================================================
def demo_rag_with_sources():
    """返回答案的同时显示来源文档"""
    db = build_db()
    retriever = db.as_retriever(search_kwargs={"k": 2})
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    query = "Python异步编程怎么用？"
    docs = retriever.invoke(query)

    context = "\n".join(doc.page_content for doc in docs)
    prompt = f"基于以下资料回答：\n{context}\n\n问题：{query}"
    answer = llm.invoke(prompt).content

    print(f"问: {query}")
    print(f"答: {answer}")
    print(f"\n来源:")
    for doc in docs:
        print(f"  - {doc.metadata.get('source', '未知')} | {doc.page_content[:40]}...")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. RAG链")
    print("=" * 60)
    demo_rag_chain()

    print("\n" + "=" * 60)
    print("2. 带来源追溯")
    print("=" * 60)
    demo_rag_with_sources()
