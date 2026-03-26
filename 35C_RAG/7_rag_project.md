# 7. RAG实战项目

## 项目：本地文档问答助手

### 功能
- 加载本地文档（TXT/PDF/Markdown）
- 自动切分和向量化
- 支持自然语言问答
- 显示答案来源
- 支持多轮对话

### 技术方案
- 向量数据库：Chroma（本地持久化）
- Embedding：OpenAI text-embedding-3-small
- LLM：GPT-4o
- 框架：LangChain

### 运行方式
```bash
# 索引文档
python 7_rag_project.py --mode index --docs ./my_docs

# 问答
python 7_rag_project.py --mode chat
```

### 扩展方向
- 支持更多文档格式（Word、Excel、网页）
- 加入混合检索（BM25 + 向量）
- 加入Rerank重排序
- 部署为Web服务
- 加入对话记忆
