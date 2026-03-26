"""
6. RAG优化 - 代码示例
演示查询改写、多查询检索、上下文压缩等优化技巧。
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document, StrOutputParser


llm = ChatOpenAI(model="gpt-4o", temperature=0)


def build_db():
    docs = [
        Document(page_content="Python的GIL限制多线程并行，CPU密集型任务用multiprocessing。"),
        Document(page_content="asyncio是Python的异步编程库，使用async/await语法。"),
        Document(page_content="threading模块适合IO密集型任务，线程在等待IO时释放GIL。"),
        Document(page_content="concurrent.futures提供线程池和进程池的高级接口。"),
        Document(page_content="装饰器是修改函数行为的语法糖，用@符号应用。"),
    ]
    return Chroma.from_documents(docs, OpenAIEmbeddings(model="text-embedding-3-small"))


# ============================================================
# 1. 查询改写
# ============================================================
def demo_query_rewrite():
    """用LLM改写用户查询，提高检索命中率"""
    db = build_db()

    original = "python怎么搞并发"
    rewrite_prompt = ChatPromptTemplate.from_template(
        "将以下口语化的问题改写为更精确的技术查询（只输出改写后的查询）：\n{query}"
    )
    chain = rewrite_prompt | llm | StrOutputParser()
    rewritten = chain.invoke({"query": original})

    print(f"原始查询: {original}")
    print(f"改写后: {rewritten}")

    # 对比检索结果
    r1 = db.similarity_search(original, k=2)
    r2 = db.similarity_search(rewritten, k=2)
    print(f"\n原始检索: {[d.page_content[:30] for d in r1]}")
    print(f"改写检索: {[d.page_content[:30] for d in r2]}")


# ============================================================
# 2. 多查询检索
# ============================================================
def demo_multi_query():
    """将一个问题拆成多个角度查询"""
    db = build_db()

    question = "Python并发编程有哪些方案？"
    expand_prompt = ChatPromptTemplate.from_template(
        "将以下问题从3个不同角度改写，每行一个查询：\n{question}"
    )
    chain = expand_prompt | llm | StrOutputParser()
    queries = chain.invoke({"question": question}).strip().split("\n")

    print(f"原始问题: {question}")
    print(f"扩展查询:")

    all_docs = []
    for q in queries[:3]:
        q = q.strip()
        if not q:
            continue
        results = db.similarity_search(q, k=2)
        all_docs.extend(results)
        print(f"  {q} → {len(results)} 个结果")

    # 去重
    unique = {doc.page_content: doc for doc in all_docs}
    print(f"\n合并去重: {len(all_docs)} → {len(unique)} 个文档")


# ============================================================
# 3. HyDE（假设文档嵌入）
# ============================================================
def demo_hyde():
    """先生成假设答案，用假设答案做检索"""
    db = build_db()

    question = "Python怎么做异步编程？"

    # 生成假设答案
    hyde_prompt = ChatPromptTemplate.from_template(
        "请简要回答以下问题（不需要完全准确）：\n{question}"
    )
    chain = hyde_prompt | llm | StrOutputParser()
    hypothetical = chain.invoke({"question": question})

    print(f"问题: {question}")
    print(f"假设答案: {hypothetical[:80]}...")

    # 用假设答案检索（通常比原始问题检索效果好）
    r1 = db.similarity_search(question, k=2)
    r2 = db.similarity_search(hypothetical, k=2)
    print(f"\n原始检索: {[d.page_content[:30] for d in r1]}")
    print(f"HyDE检索: {[d.page_content[:30] for d in r2]}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 查询改写")
    print("=" * 60)
    demo_query_rewrite()

    print("\n" + "=" * 60)
    print("2. 多查询检索")
    print("=" * 60)
    demo_multi_query()

    print("\n" + "=" * 60)
    print("3. HyDE")
    print("=" * 60)
    demo_hyde()
