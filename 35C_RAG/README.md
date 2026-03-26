# 第35C章：RAG（检索增强生成）

## 本章目标

- 理解RAG的原理和应用场景
- 掌握文档加载、切分、Embedding的完整流程
- 学会使用向量数据库（Chroma、FAISS）
- 构建完整的RAG问答系统
- 掌握RAG的优化技巧

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 内容 |
|------|----------|----------|------|
| 1 | 1_rag_overview.md | 1_rag_overview.py | RAG概述与原理 |
| 2 | 2_document_loading.md | 2_document_loading.py | 文档加载与切分 |
| 3 | 3_embedding.md | 3_embedding.py | Embedding与向量数据库 |
| 4 | 4_retrieval.md | 4_retrieval.py | 检索策略 |
| 5 | 5_rag_chain.md | 5_rag_chain.py | 构建RAG链 |
| 6 | 6_rag_optimization.md | 6_rag_optimization.py | RAG优化技巧 |
| 7 | 7_rag_project.md | 7_rag_project.py | RAG实战项目 |

## 前置知识

- Python基础
- 生成式AI与LLM（第35章）

## 安装依赖

```bash
pip install langchain langchain-openai langchain-community
pip install chromadb faiss-cpu
pip install pypdf docx2txt tiktoken
```

## 章节导航

[上一章：大模型微调](../35B_大模型微调/README.md) | [下一章：LLM Agent](../36_LLM_Agent/README.md)
