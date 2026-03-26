"""
1. RAG概述 - 代码示例
用最少代码演示RAG的完整流程：加载→切分→向量化→检索→生成。
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


# ============================================================
# 最简RAG示例（10行核心代码）
# ============================================================
def demo_minimal_rag():
    """最简单的RAG：从几段文本中检索并回答"""

    # 1. 准备文档
    docs = [
        Document(page_content="Python是一种高级编程语言，由Guido van Rossum于1991年创建。Python以简洁的语法著称。"),
        Document(page_content="Python的GIL（全局解释器锁）限制了多线程的并行执行。CPU密集型任务建议使用多进程。"),
        Document(page_content="Python的装饰器是一种修改函数行为的语法糖，使用@符号应用。常用于日志、缓存、权限控制。"),
        Document(page_content="FastAPI是一个现代Python Web框架，基于类型注解，性能接近Node.js和Go。"),
        Document(page_content="PyTorch是Meta开发的深度学习框架，以动态计算图和Pythonic的API著称。"),
    ]

    # 2. 切分（这里文档已经很短，演示用）
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_documents(docs)
    print(f"文档数: {len(docs)} → 切分后: {len(chunks)} 块")

    # 3. 向量化 + 存入Chroma
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(chunks, embeddings)
    print("向量数据库构建完成")

    # 4. 检索
    query = "Python的GIL是什么？"
    results = vectorstore.similarity_search(query, k=2)
    print(f"\n查询: {query}")
    print(f"检索到 {len(results)} 个相关文档:")
    for i, doc in enumerate(results):
        print(f"  [{i+1}] {doc.page_content[:80]}...")

    # 5. 生成回答
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    context = "\n".join([doc.page_content for doc in results])
    prompt = f"基于以下资料回答问题。如果资料中没有相关信息，请说'不确定'。\n\n资料:\n{context}\n\n问题: {query}"

    answer = llm.invoke(prompt)
    print(f"\n回答: {answer.content}")


if __name__ == "__main__":
    demo_minimal_rag()
