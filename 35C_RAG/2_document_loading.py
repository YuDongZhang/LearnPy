"""
2. 文档加载与切分 - 代码示例
演示各种文档加载器和切分策略。
"""

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
from langchain.schema import Document


# ============================================================
# 1. 文本加载器
# ============================================================
def demo_text_loader():
    """加载纯文本文件"""
    # 创建示例文件
    sample = "Python是一种高级编程语言。\n\n它由Guido van Rossum创建。\n\nPython以简洁著称。"
    with open("sample.txt", "w", encoding="utf-8") as f:
        f.write(sample)

    from langchain_community.document_loaders import TextLoader
    loader = TextLoader("sample.txt", encoding="utf-8")
    docs = loader.load()
    print(f"加载了 {len(docs)} 个文档")
    print(f"内容: {docs[0].page_content[:100]}")
    print(f"元数据: {docs[0].metadata}")


# ============================================================
# 2. 递归切分（最常用）
# ============================================================
def demo_recursive_split():
    """递归字符切分：按段落→句子→字符逐级切分"""
    text = """Python是一种广泛使用的高级编程语言。它由Guido van Rossum于1991年创建。

Python的设计哲学强调代码的可读性和简洁性。它支持多种编程范式，包括面向对象、函数式和过程式编程。

Python拥有丰富的标准库和第三方库生态系统。常用于Web开发、数据分析、人工智能、自动化脚本等领域。

Python的GIL（全局解释器锁）是CPython实现的一个特性，它限制了多线程的并行执行能力。"""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", " ", ""],
    )
    chunks = splitter.create_documents([text])

    print(f"原文: {len(text)} 字符 → {len(chunks)} 块")
    for i, chunk in enumerate(chunks):
        print(f"  块{i+1} ({len(chunk.page_content)}字符): {chunk.page_content[:50]}...")


# ============================================================
# 3. Markdown按标题切分
# ============================================================
def demo_markdown_split():
    """按Markdown标题切分"""
    md_text = """# Python基础
Python是高级编程语言，语法简洁。

## 变量和类型
Python是动态类型语言，不需要声明变量类型。

## 函数
使用def关键字定义函数。

# 高级特性
## 装饰器
装饰器用于修改函数行为。

## 生成器
使用yield关键字创建生成器。"""

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2")]
    )
    chunks = splitter.split_text(md_text)

    print(f"Markdown切分: {len(chunks)} 块")
    for chunk in chunks:
        print(f"  标题: {chunk.metadata} | 内容: {chunk.page_content[:40]}...")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 文本加载")
    print("=" * 60)
    demo_text_loader()

    print("\n" + "=" * 60)
    print("2. 递归切分")
    print("=" * 60)
    demo_recursive_split()

    print("\n" + "=" * 60)
    print("3. Markdown切分")
    print("=" * 60)
    demo_markdown_split()
