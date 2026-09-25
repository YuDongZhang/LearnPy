# 5. 构建 RAG 链

> 这一篇回答一个问题：**前面 4 篇造出来的零件，怎么装成一台机器？**
>
> 主线一句话：
>
> ```
> RAG 链 = 一条「数据流水线」：数据在管道里被逐步改写，每一站换个形态
> ```
>
> ```
> 字符串 ──→ [Document] ──→ 字符串 ──→ PromptValue ──→ AIMessage ──→ 字符串
>  查询      检索到的文档    拼好的上下文     填好的模板      模型回复     最终答案
> ```
>
> 理解了这条形态变化的链路，LCEL 那些"`|`、字典、`RunnablePassthrough`"就不再是魔法。
>
> 本篇会用真实中间值把每一步拆开（第 2 节），实测 Prompt 约束的效果（第 3 节），并复盘一个**真实踩过的坑**——它在修复前让本节的对比结果完全错误（第 6 节）。
>
> 本文数字来自 `5_rag_chain.py` 的实跑输出，以及一组打印管道中间值的实测（脚本已删除，均可复现）。

---

## 0. 先看真实运行

```
1. RAG链
============================================================
问: Python的GIL是什么？
答: 根据参考资料，Python的GIL（全局解释器锁）限制了多线程并行。

问: FastAPI有什么特点？
答: 根据参考资料，FastAPI的特点包括：基于类型注解，自动生成API文档，性能优秀。

问: Go语言怎么样？
答: 我不确定

2. 带来源追溯
============================================================
问: Python异步编程怎么用？
答: Python 异步编程主要用 `asyncio` 库，配合 `async` / `await` 语法。
   [……一段带代码示例的长回答……]
来源:
  - async.md | asyncio提供异步编程，适合高并发IO。使用async/await语法。...
  - concurrency.md | Python的GIL限制了多线程并行。CPU密集型用multiprocessin...
```

> ⚠️ LLM 的回答**每次措辞都略有不同**（即使 `temperature=0`，服务端实现也不保证逐字节确定）。上面引用的是其中一次真实运行；**检索命中的文档、"Go语言怎么样？→我不确定"这个拒答、以及来源列表，都是稳定复现的**。第 7 篇的 `chat` 模式同理。

三行必须停下来看的地方：

1. **`Go语言怎么样？` → `我不确定`**。库里 5 条文档全是 Python 相关，模型没有硬编，**Prompt 里的"如果资料中没有相关信息，请说'我不确定'"生效了**。这是 RAG 防幻觉的第一道闸门，第 3 节会用量化数据说明它为什么生效。
2. **前两个答案都只有一句话**，第 3 个是长回答。同一套链、同样的 `k=2`，答案长度差了 20 倍——原因在检索质量，也在 Prompt 的松紧程度（第 4 节）。
3. **"来源"里出现了 `concurrency.md`**（GIL 那条），而问的是异步编程。检索器把 GIL 文档当成了第 2 相关——这其实是合理的（异步和多线程是同一类话题），但它也说明 **k=2 里几乎总有一条是"陪跑"的**。

---

## 1. 先搞懂 LCEL：`|` 到底做了什么

代码里这条链是本节的全部：

```python
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

`|` 看着像 Linux 管道，语义也确实是"把左边输出喂给右边"。它之所以能这么写，是因为 LangChain 给所有组件定了一个**统一接口 `Runnable`**：

| 方法 | 作用 |
|---|---|
| `invoke(x)` | 单条输入 → 单条输出 |
| `batch([x1, x2])` | 批量处理 |
| `stream(x)` | 流式输出 |
| `ainvoke / astream` | 异步版本 |

**只要一个对象实现了 `Runnable`，它就能用 `|` 串起来。** `|` 运算符在背后做的是 `RunnableSequence(left, right)`——所以：

```
a | b  ≡  RunnableSequence(a, b)  ≡  把 a 的输出作为 b 的输入
```

### 三个必须认识的"零件类型"

链里有三种写法，各自对应一个包装类：

| 你在链里写的东西 | 实际变成的类 | 语义 |
|---|---|---|
| `{"context": ..., "question": ...}` | `RunnableParallel` | **并行**执行每个 value，汇总成字典 |
| `RunnablePassthrough()` | `RunnablePassthrough` | **原样返回输入**（占位用） |
| `format_docs`（一个普通函数） | `RunnableLambda` | 把普通函数**自动包装**成 Runnable |

**这里有个容易困惑的点：`{"context": ..., "question": ...}` 为什么能放进管道？**

因为 `RunnableParallel` 的语义是：**把同一份输入，分别喂给每个 value，然后把结果装进字典。** 输入是用户的问题（字符串），于是：

```
输入 "Python的GIL是什么？"
      ├─→ retriever | format_docs  →  context: "检索到的文档拼成的字符串"
      └─→ RunnablePassthrough()    →  question: "Python的GIL是什么？"（原样）
                                     ↓
                        得到字典 {"context": ..., "question": ...}
```

**`RunnablePassthrough` 的存在就是为了"把原始问题也带上"**——因为 `retriever` 用掉了输入去检索，模板里还需要问题原文本身。

---

## 2. 逐步拆解：用真实中间值走一遍

我把管道每个环节的真实输出都打印出来了（5 条文档的小库，`k=2`）。下面是最关键的一组。

### 案例 A：`Python的GIL是什么？`（命中）

```
输入: "Python的GIL是什么？"

[retriever] 返回 2 条 Document:
    [concurrency.md] Python的GIL限制了多线程并行。CPU密集型用multiprocessing。
    [generator.md]   生成器用yield产生值，惰性求值，适合大数据处理。        ← 噪音

[format_docs] 用 "\n" 拼接，得到 69 字符的字符串:
    "Python的GIL限制了多线程并行。CPU密集型用multiprocessing。
     生成器用yield产生值，惰性求值，适合大数据处理。"

[RunnableParallel] 组装字典:
    {"context": "Python的GIL限制了多线程并行。…生成器用yield…",
     "question": "Python的GIL是什么？"}

[prompt] 填充模板 → PromptValue（内部就是一段完整文本）:
    基于以下参考资料回答问题。如果资料中没有相关信息，请说'我不确定'。

    参考资料:
    Python的GIL限制了多线程并行。CPU密集型用multiprocessing。
    生成器用yield产生值，惰性求值，适合大数据处理。

    问题: Python的GIL是什么？

[llm] → AIMessage("根据参考资料，Python的GIL（全局解释器锁）限制了多线程并行。")

[StrOutputParser] → 取 .content，得到纯字符串
```

**注意 `[generator.md] ← 噪音` 那一行。** `k=2` 时第二条检索结果（生成器）和 GIL 毫无关系，**上下文里有一半是废的**。但最终答案仍然正确——这说明 LLM 有一定的抗噪能力。

> 但**不能把抗噪当作设计依据**。第 2 篇讲过：喂进去的每一块都在消耗 LLM 的注意力预算。这次它扛住了，`k=10` 就未必。

### 四个查询的完整对照（真实数据）

| 查询 | Top-1（正确） | Top-2（陪跑） | 上下文长度 | LLM 的回答 |
|---|---|---|---|---|
| `Python的GIL是什么？` | concurrency.md | generator.md | 69 字符 | ✅ 正确 |
| `FastAPI有什么特点？` | web.md | async.md | 68 字符 | ✅ 正确 |
| `Python异步编程怎么用？` | async.md | concurrency.md | 81 字符 | ✅ 正确 |
| `Go语言怎么样？` | async.md | web.md | 68 字符 | ❌ **我不确定** |

**`Go语言怎么样？` 这一行是本篇的重点。** 库里根本没有 Go 相关内容，检索器仍然"尽职地"返回了 2 条（`async.md` 和 `web.md`）——**因为 `similarity_search` 永远会返回 k 条，它不负责判断"有没有"**（第 4 篇第 2 节的结论）。

所以"库里没有相关内容时不要瞎编"这件事，**只能靠 Prompt 约束来完成**。下一节就来量化它。

---

## 3. Prompt 约束：为什么"我不确定"真的生效了

### 那两行 prompt 是关键

```python
prompt = ChatPromptTemplate.from_template(
    "基于以下参考资料回答问题。如果资料中没有相关信息，请说'我不确定'。\n\n"
    "参考资料:\n{context}\n\n"
    "问题: {question}"
)
```

第一句是**约束**（只能用资料），第二句是**逃生出口**（没有就说不知道）。

**第二句才是真正的关键。** 如果只写"基于以下参考资料回答问题"，模型在资料不足时的选择是：

```
资料不足 → 模型要么硬编（幻觉），要么说"资料中没有提到"
```

而后者听起来像在推卸责任，模型未必愿意说。**明确给出一个"标准答案话术"（"我不确定"），模型才会照着说。** 这在业界被称为"允许弃权"（abstention），是防幻觉最便宜的手段。

### 用量化数据看它的边界

第 4 篇提出过一个"相对间隔"判据：`(score₂ − score₁)/score₁`。我把它和本节 4 个查询的真实结果并排：

| 查询 | Top-1 `score` | Top-2 `score` | **相对间隔** | LLM 的回答 |
|---|---|---|---|---|
| `FastAPI有什么特点？` | 0.5470 | 0.9320 | **70.4%** | ✅ 正确 |
| `Python的GIL是什么？` | 0.6421 | 0.9626 | **49.9%** | ✅ 正确 |
| `Python异步编程怎么用？` | 0.6157 | 0.7447 | **21.0%** | ✅ 正确 |
| **`Go语言怎么样？`** | 1.0583 | 1.0700 | **1.1%** | ❌ **我不确定** |

**这张表有两个独立的价值：**

**第一，它验证了第 4 篇的判据。** 这是**完全不同的一批文档、独立测出来**的数据：

```
命中查询的相对间隔:  21.0%  ~  70.4%
未命中查询的相对间隔:   1.1%
```

第 4 篇测出的是"命中 26.9%~41.7% / 未命中 2.9%"，本篇是"命中 21.0%~70.4% / 未命中 1.1%"。**中间始终隔着 10 倍以上的空档**，判据是稳的。

**第二，它揭示了一条（观测到的）联系：** 相对间隔最小的那个查询（1.1%），恰好就是 LLM 唯一拒答的那个。检索质量和生成质量之间确实有传导关系。

> ⚠️ **必须诚实标出的局限**：这里只有 4 个样本，**不足以证明因果关系**，只能说"观察到了相关性"。要下结论需要几十上百条标注数据 + 第 4 篇的评估指标。但作为**设阈值的起点**，这个信号已经很实用了。

### 顺带说明 `format_docs` 的作用

```python
def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)
```

它做的事很朴素——把 `[Document]` 列表拼成一个字符串。但这一步**不能省**：

```
[Document, Document]  ← 模板的 {context} 只能填字符串，塞不进对象
        ↓ format_docs
"文档1正文\n文档2正文"  ← 可以填进去了
```

**同时它也是"上下文工程"的落点。** 想加来源标注、加序号、加分隔符，全都在这里改（第 7 篇的版本就在每块前面加了 `[来源: xxx]`）。

---

## 4. 一个反直觉的观察：Prompt 没禁止模型用自己的知识

看第 0 节第 2 节的回答——它很长，**带代码示例，列了 4 个要点**。但检索到的上下文只有两句、共 81 个字符：

```
asyncio提供异步编程，适合高并发IO。使用async/await语法。
Python的GIL限制了多线程并行。CPU密集型用multiprocessing。
```

答案里出现的 `asyncio.run()`、`asyncio.gather()`、`async def` 定义要点、事件循环等内容，**都不在这两句话里**。它们是模型从**自己的参数知识**里补出来的。

注意：**这些补充内容本身是对的**，所以这不是"幻觉"。但它暴露了一个设计缺陷：

```
Prompt 写的是「基于以下参考资料回答问题」
         ↓
模型的解读是「参考资料是主要依据，但我可以补充我知道的」
         ↓
而 RAG 的初衷是「只根据外部知识回答，因为外部知识才是权威的、最新的」
```

**风险在于：当模型的参数知识和你的知识库冲突时，它会选哪个？** 如果 Prompt 没写清楚，答案是不确定的——而你的知识库（公司规章、最新接口文档）**恰恰是更权威的那个**，这才需要 RAG。

### 更严格的写法

```python
prompt = ChatPromptTemplate.from_template(
    "你是文档问答助手。**只**依据下方参考资料回答，"
    "不要使用参考资料之外的任何知识。\n"
    "如果参考资料不足以回答，请直接说'文档中未找到相关信息'。\n"
    "回答中每一处结论都要能对应到参考资料里的一句话。\n\n"
    "参考资料:\n{context}\n\n问题: {question}"
)
```

**关键词是"只"、"不要使用……之外的任何知识"、"每一处结论都要对应"。** 这类约束在不同模型上效果差别很大，**必须实测**（换 Prompt 后重跑第 4 篇的评估）。

> 第 7 篇的实战项目用的就是更严格的版本，并额外要求"回答后标注信息来源"。

---

## 5. 来源追溯：为什么这不是"锦上添花"

`demo_rag_with_sources` 做了一件小事：把检索到的文档也打印出来。

```
来源:
  - async.md | asyncio提供异步编程，适合高并发IO。使用async/await语法。...
  - concurrency.md | Python的GIL限制了多线程并行。CPU密集型用multiprocessin...
```

**为什么必须做？** 回到第 1 篇那个案例：`Python的GIL是什么？` 时 Top-1 排错了（装饰器排第 1，余弦只差 0.0075）。**如果只打印最终答案，你永远发现不了检索已经接近失效。**

```
不打印来源：            打印来源：
  用户：答案对不对？       用户：答案对不对？
  你：感觉还行…           你：检索的第 1 名是谁？
  用户：为什么这么答？      → 一眼看出排序错误
  你：不知道 🤷           → 能定位到是哪一块文档导致的
```

**三个层次的价值：**

| 层次 | 作用 | 面向谁 |
|---|---|---|
| 调试 | 看检索对不对、噪音多不多 | 开发者 |
| 可信 | 用户可以自己去核对原文 | 终端用户 |
| 合规 | 金融/医疗/法律场景常要求答案可追溯 | 审计 |

**实现方式**：`metadata` 字段（第 2 篇讲过，它不参与向量检索，专门用来存来源）。代码里这一行就是全部：

```python
docs = retriever.invoke(query)   # 直接在链外拿到 Document，就能读到 metadata
```

注意 `demo_rag_with_sources` 是**手写流程**（自己 invoke retriever、自己拼 prompt），而 `demo_rag_chain` 用的是 LCEL 管道。**前者更容易加来源，后者更简洁可读**——第 7 篇的实战项目用 LCEL + 在 `format_docs` 里把来源拼进上下文，两者兼顾。

---

## 6. 复盘一个真实踩过的坑：Chroma collection 累积

这一节记录一个**真实发生过的错误**，因为它的后果比想象中隐蔽。

### 现象

修复前，`demo_rag_with_sources` 打印的来源是这样的：

```
来源:
  - async.md | asyncio提供异步编程，适合高并发IO。使用async/await语法。...
  - async.md | asyncio提供异步编程，适合高并发IO。使用async/await语法。...
                ↑ 两条完全一样！
```

### 根因

`demo_rag_chain` 和 `demo_rag_with_sources` 各自调用了一次 `build_db()`。而 Chroma 的内存模式默认使用名为 `"langchain"` 的 collection，**`from_documents` 的行为是"追加"，不是"重建"**（第 3 篇第 7 节实测过：6 条 → 12 条）。

于是第二个 demo 检索时，库里 5 条文档各有一份副本，`k=2` 返回了**同一条内容的两个副本**。

### 后果有多严重

同源的 `6_rag_optimization.py` 里，后果直接毁掉了实验结论：

```
（修复前）
原始检索: ['asyncio是Python的异步编程库…', 'asyncio是Python的异步编程库…']
HyDE检索: ['asyncio是Python的异步编程库…', 'asyncio是Python的异步编程库…']
合并去重: 6 → 1 个文档        ← 3 路查询召回的全是同一条的副本
```

**"多查询检索"和"HyDE"的对比实验完全失效**——你以为是两个不同方法的效果差异，实际上看到的是同一个重复 bug。

### 修复

```python
_DB = None

def build_db():
    """构建测试向量数据库（进程内只构建一次）"""
    global _DB
    if _DB is None:
        docs = [...]
        _DB = Chroma.from_documents(docs, get_embeddings())
    return _DB
```

**用模块级缓存，保证进程内只构建一次。** 修复后 `5_rag_chain.py` 的输出变成：

```
来源:
  - async.md | asyncio提供异步编程，适合高并发IO。使用async/await语法。...
  - concurrency.md | Python的GIL限制了多线程并行。CPU密集型用multiprocessin...
```

两条不同的文档了。`6_rag_optimization.py` 的"合并去重"也从 `6 → 1` 变成 `6 → 2`（另一次运行是 `6 → 3`——这个数随 LLM 生成的子查询波动，关键是不再是同一条的副本了）。

### 从这件事该学到什么

| 教训 | 说明 |
|---|---|
| **向量库的写入是"追加"语义** | `from_documents` ≠ 重建。要重建必须先删 collection |
| **脚本的"可重复运行"是个陷阱** | 每次都调的 `build_db()` 每次都在污染数据库；持久化模式更危险（跨进程累积） |
| **异常的检索结果先查库里有几条** | `db._collection.count()` 是最该先看的一行调试代码 |
| **对比实验必须保证对照组条件相同** | 本次两个方法检索的是同一个被污染的库，结论本身就不可能成立 |

> **对第 7 篇的提醒**：`7_rag_project.py` 的 `--mode index` 是**持久化**写入。重复执行会让 `./rag_db` 不断膨胀。第 7 篇会说明规避方法。

---

## 7. 曾经的主流写法（了解即可）

旧教程里常见三个"一行搞定"的封装。它们都是 `Runnable`，仍能用 `|`，但**已不推荐**：

| 写法 | 问题 |
|---|---|
| `RetrievalQA.from_chain_type(...)` | 早期封装，`chain_type` 参数（stuff/map_reduce/refine）把逻辑藏在字符串里，难调试 |
| `ConversationalRetrievalChain` | 老式多轮对话，历史处理方式是黑盒 |
| `create_retrieval_chain` + `create_stuff_documents_chain` | 官方新封装，比 LCEL 更"标准"，但中间步骤更难插桩 |

**本教程坚持用 LCEL 的原因**：每一个中间值都能单独取出来看（本文第 2 节的表格就是这么打出来的）。

```
LCEL 写法:            旧封装:
  chain.invoke(q)        qa_chain.invoke({"query": q})
  ↑                     ↑
  想插桩？拆开链就行      想插桩？改内部源码…
  retriever.invoke(q)   ✗ 拿不到中间值
  format_docs(docs)
```

第 6 篇的查询改写 / HyDE / 多路召回，全都是"在链的某个位置插一步"，**用 LCEL 做这件事是自然顺手，用旧封装则是和框架打架**。

---

## 代码

`5_rag_chain.py` 分两节：

| 代码位置 | 做什么 | 对应本文 |
|---|---|---|
| `build_db` + 缓存 | 5 条带 `metadata` 的文档 | 第 6 节（**这就是修复后的版本**） |
| `demo_rag_chain` | LCEL 管道 + 3 个问题 | 第 1、2、3 节 |
| `demo_rag_with_sources` | 手写流程 + 打印来源 | 第 4、5 节 |

**链的核心就是这 4 行：**

```python
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

**建议动手改三处**，验证本文的结论：

1. **把 `k` 从 2 改成 5**（库里有 5 条，等于全量），看噪音块如何淹没答案、答案是否还准确——验证第 2 节"抗噪有极限"。
2. **把 Prompt 里"如果资料中没有相关信息，请说'我不确定'"删掉**，再问 `Go语言怎么样？`，看模型是否开始硬编——验证第 3 节"逃生出口"的必要性。
3. **把 Prompt 换成第 4 节那段严格版本**，看 `Python异步编程怎么用？` 的答案是否显著变短（不再补充自己的知识）——验证第 4 节的观察。

想自己打印中间值的话，链可以"半拆开"用：

```python
docs = retriever.invoke("Python的GIL是什么？")
print("检索到:", [(d.metadata["source"], d.page_content) for d in docs])
print("上下文:", format_docs(docs))
```

运行前 `.env` 需要 `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`（本节要调 LLM）和 `EMBEDDING_MODEL`（本地模型，无需 Key）。

```bash
python 5_rag_chain.py
```