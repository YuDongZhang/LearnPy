# 第35C章：RAG（检索增强生成）

> 这一章只讲一件事：**怎么让 LLM 从"闭卷考试"变成"开卷考试"**。
>
> 但它和常见的 RAG 教程有两个区别：
>
> **第一，每一篇的主线是"为什么"，不是"是什么"。** 7 篇连起来是一条完整的推导链：
>
> ```
> 1 为什么要 RAG   → 2 文档怎么进来  → 3 意思怎么变成向量 → 4 怎么找得准
>                                                                  ↓
>                        7 装成工具  ←  6 优化值不值  ←  5 怎么串成链
> ```
>
> **第二，本章所有数字都来自真实运行**，不是估计值。包括"三个热门优化技巧在本例中收益为零、延迟涨 400 倍"这种不好看但真实的结论。**跑不出来的数字，本文会明说是手工设计或未实测。**
>
> 阅读环境：Python + langchain 0.3.30、chromadb 1.5.9、sentence-transformers 5.1.2；Embedding 用本地 `BAAI/bge-small-zh-v1.5`（512 维），LLM 走任意 OpenAI 兼容端点。

---

## 本章目标

- 理解 RAG 的两阶段结构（**离线索引期** vs **在线查询期**），以及为什么两者的延迟要求完全不同
- 掌握文档加载与切分的真实后果（切分器什么时候是"空转"的、overlap 的膨胀率是多少）
- 建立对 Embedding 的几何直觉，并**亲手验证** Chroma 的 `score` 到底是距离还是相似度
- 学会用相对判据判断"库里到底有没有相关内容"，而不是拍一个绝对阈值
- 看懂 LCEL 管道（`|`、dict、`RunnablePassthrough`）背后发生了什么数据形态变化
- 知道常用优化技巧（查询改写 / 多查询 / HyDE）**在什么情况下无效、代价是多少**

---

## 章节目录

| 编号 | 讲解(md) | 代码(py) | 这一篇回答的问题 |
|------|----------|----------|------------------|
| 1 | [1_rag_overview.md](1_rag_overview.md) | 1_rag_overview.py | RAG 到底解决了什么问题？为什么检索会"答错第一名"？ |
| 2 | [2_document_loading.md](2_document_loading.md) | 2_document_loading.py | 文档怎么进来？切分粒度怎么定？中文为什么比英文"贵"？ |
| 3 | [3_embedding.md](3_embedding.md) | 3_embedding.py | "意思像不像"怎么变成"几何上近不近"？`score` 是距离还是相似度？ |
| 4 | [4_retrieval.md](4_retrieval.md) | 4_retrieval.py | 召回和排序怎么分工？MMR / BM25 / RRF 分别在解决什么？ |
| 5 | [5_rag_chain.md](5_rag_chain.md) | 5_rag_chain.py | LCEL 的 `\|` 到底做了什么？Prompt 约束为什么真的能防幻觉？ |
| 6 | [6_rag_optimization.md](6_rag_optimization.md) | 6_rag_optimization.py | 那些"高级技巧"值不值得上？代价是多少？ |
| 7 | [7_rag_project.md](7_rag_project.md) | 7_rag_project.py | 怎么装成一个能用的工具？离"能用"还差什么？ |

**建议按顺序读。** 后续篇章会直接引用前面的实测数字（例如第 5、7 篇都在用第 4 篇提出的"相对间隔"判据，并且是**在不同的库上独立复测**的）。

---

## 环境准备

### 1. 安装依赖

```bash
pip install langchain langchain-openai langchain-community
pip install langchain-huggingface sentence-transformers
pip install chromadb faiss-cpu
pip install python-dotenv pypdf tiktoken
```

| 包 | 为什么需要 |
|---|---|
| `langchain` / `langchain-openai` / `langchain-community` | 链、LLM、向量库、文档加载器 |
| `langchain-huggingface` + `sentence-transformers` | **本地方案**：跑 bge 中文 Embedding，不需要 API Key |
| `chromadb` | 向量数据库（本章主力，零配置） |
| `faiss-cpu` | 另一款向量库（第 3 篇做过选型对比） |
| `python-dotenv` | 从 `.env` 读配置 |
| `tiktoken` / `pypdf` | 数 token / 加载 PDF |

> 实测可用版本：langchain 0.3.30 + langchain-core 0.3.86 + langchain-openai 0.3.35 + chromadb 1.5.9 + langchain-huggingface 0.3.1 + sentence-transformers 5.1.2 + transformers 4.57.6 + torch 2.8.0+cpu。**LangChain 生态版本漂移很快，遇到 `ImportError` 或行为差异，先怀疑版本。**

### 2. 配置 `.env`

在**仓库根目录**（即 `LearnPy/.env`）建一个文件：

```
# LLM：任意 OpenAI 兼容端点都行（示例为火山引擎 Ark）
OPENAI_API_KEY=你的key
OPENAI_BASE_URL=你的兼容端点
OPENAI_MODEL=你的模型名

# Embedding：本地模型，不需要 API Key
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5

# HuggingFace 国内镜像：直连 huggingface.co 会超时
HF_ENDPOINT=https://hf-mirror.com
```

所有脚本都在**最前面**调用 `load_dotenv()`（在 `import` 之前），所以 `HF_ENDPOINT` 能在 `huggingface_hub` 初始化前生效。**不要把它挪到 import 之后**，否则镜像配置会失效，表现为反复的连接超时重试。

### 3. 两个已经踩过的坑

| 现象 | 原因 | 处理 |
|---|---|---|
| 首次运行卡在 `huggingface.co` 连接超时、反复重试 5 次 | 直连 huggingface.co 不通 | `.env` 加 `HF_ENDPOINT=https://hf-mirror.com`（模型约 100MB，只需下载一次） |
| `ValueError: Your currently installed version of Keras is Keras 3...` | `transformers` 会自动探测本机的 TensorFlow，并撞上 Keras 3 的版本约束 | 脚本里在 `import transformers` **之前**加 `os.environ.setdefault("USE_TF", "0")`。**不要为此卸载 TensorFlow**——那会破坏你用其他章节的 TF 环境 |

---

## 三条全章通用的结论

这三条在多个篇章里被**独立复测**过，值得单独记住。

### ① 绝对分数阈值在向量检索里基本失效

```
问"Python的GIL是什么？"，5 条文档的余弦相似度全落在 [0.5759, 0.6616]，极差只有 0.0857
而且 Top-1 竟然是"装饰器"，GIL 排第二 —— 两者只差 0.0075
```

**所以"score > 0.7 才算命中"这类写法是错的**，而且方向可能是反的——Chroma 默认返回的是**距离（越小越近）**，不是相似度。详见第 1、3 篇。

### ② 用"相对间隔"判断库里有没有相关内容

```
相对间隔 = (score₂ − score₁) / score₁
```

三套完全不同的文档、三种不同的查询，独立测出来的空档一直存在：

| 数据来源 | 命中查询 | 无关查询 |
|---|---|---|
| 第 4 篇（5 条文档） | 26.9% ~ 41.7% | **2.9%** |
| 第 5 篇（5 条文档） | 21.0% ~ 70.4% | **1.1%** |
| 第 7 篇（2 条文档） | 52.3% ~ 100.4% | **0.9%** |

**>20% 大概率命中，<10% 基本可以认为库里没有相关内容。** 这个判据可以当作**设阈值的起点**（不是定论——样本量不够下因果结论）。

### ③ 优化技巧要按"代价"排序，而不是按"热度"排序

第 6 篇实测（同一批文档、同一个问题）：

| 方案 | 端到端耗时 | 检索结果 | 相对成本 |
|---|---|---|---|
| 纯向量检索 | **0.01 秒** | asyncio, GIL | 1× |
| 查询改写 + 检索 | **3.14 秒** | 完全相同 | **314×** |
| HyDE + 检索 | **4.09 秒** | 完全相同 | **409×** |

**延迟涨了几百倍，检索结果一个字符都没变。** 所以正确的顺序永远是：

```
先建评估集 → 测出基线 → 找到瓶颈 → 再挑技巧 → 重测，只留有效的
```

---

## 学完能回答这些问题，就说明学懂了

1. RAG 的索引期和查询期，哪一侧对延迟敏感？为什么？
2. 中文文档按字符数切分有什么问题？（提示：中文约 1.12 字符/token，英文约 4.19，差 3.7 倍）
3. `chunk_overlap` 从 0 加到 30，输出一个字符都没变；那它什么时候才生效？代价是多少？
4. 为什么"cos 相似度"和"欧氏距离"在向量**归一化之后**是等价的？写出推导。
5. `similarity_search_with_score` 返回的分数，`l2` 空间和 `cosine` 空间分别是什么公式？
6. 一个查询召回的结果互相雷同，该用 MMR / BM25 / RRF 里的哪一个？为什么？
7. `RunnablePassthrough()` 在链里删掉会怎样？
8. 库里明明没有相关内容，检索器为什么还是返回了 k 条？怎么让模型不要硬编？
9. 为什么"查询改写"有时会让检索结果**变差**？
10. 一个 RAG 系统要上线，最先该补的两件事是什么？（第 7 篇第 7 节）

---

## 章节导航

[上一章：大模型微调](../35B_大模型微调/README.md) | [下一章：LLM Agent](../36_LLM_Agent/README.md)