"""
7. RAG实战 - 本地文档问答助手
支持加载本地文档，构建向量索引，交互式问答。
"""

import os
import sys
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    TextLoader, DirectoryLoader, UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


PERSIST_DIR = "./rag_db"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o"


# ============================================================
# 1. 索引构建
# ============================================================
def build_index(docs_dir: str):
    """加载文档目录，构建向量索引"""
    print(f"加载文档: {docs_dir}")

    # 加载txt和md文件
    loader = DirectoryLoader(
        docs_dir, glob="**/*.txt",
        loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
    )
    docs = loader.load()

    # 也加载md文件
    try:
        md_loader = DirectoryLoader(
            docs_dir, glob="**/*.md",
            loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
        )
        docs.extend(md_loader.load())
    except Exception:
        pass

    print(f"加载了 {len(docs)} 个文档")
    if not docs:
        print("未找到文档，请确认目录中有.txt或.md文件")
        return

    # 切分
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"切分为 {len(chunks)} 个块")

    # 向量化并持久化
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    print(f"索引已保存到 {PERSIST_DIR}")


# ============================================================
# 2. 问答
# ============================================================
def chat():
    """交互式RAG问答"""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    prompt = ChatPromptTemplate.from_template(
        "你是一个文档问答助手。基于以下参考资料回答问题。\n"
        "如果资料中没有相关信息，请说'文档中未找到相关信息'。\n"
        "回答后标注信息来源。\n\n"
        "参考资料:\n{context}\n\n问题: {question}"
    )

    def format_docs(docs):
        return "\n---\n".join(
            f"[来源: {d.metadata.get('source', '未知')}]\n{d.page_content}"
            for d in docs
        )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

    print("文档问答助手已启动（输入 exit 退出）")
    print("-" * 40)
    while True:
        q = input("\n你: ").strip()
        if q.lower() in ("exit", "quit", "q"):
            print("再见！")
            break
        if not q:
            continue
        answer = chain.invoke(q)
        print(f"\n助手: {answer}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  索引: python 7_rag_project.py --mode index --docs ./my_docs")
        print("  问答: python 7_rag_project.py --mode chat")
        sys.exit(1)

    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "chat"

    if mode == "index":
        docs_dir = sys.argv[sys.argv.index("--docs") + 1] if "--docs" in sys.argv else "./docs"
        build_index(docs_dir)
    elif mode == "chat":
        chat()
