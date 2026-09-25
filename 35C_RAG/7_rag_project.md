# 7. RAG 实战项目：本地文档问答助手

> 这一篇是收官：**把前 6 篇拆散的零件，装成一个真正能用的命令行工具。**
>
> 前面 6 篇都在回答"原理是什么"，这一篇要回答的是工程问题：
>
> ```
> 索引和问答为什么要分成两条命令？
> 索引写到磁盘之后，会有什么副作用？
> 一条「能跑」的问答链，离「能用」还差什么？
> ```
>
> 本篇的主线是一句反直觉的实测结论：
>
> ```
> index 模式和 chat 模式的总耗时几乎一样（10.0s vs 9.0s）。
> 因为它们的时间几乎都花在同一件事上——
> 加载 embedding 模型：8.99 秒，占 index 的 90%、chat 的 99.9%。
> ```
>
> 也就是说，**"离线/在线"这个划分，切开的不是"贵/便宜"，而是"跑几次"**。这个认识直接决定了生产环境该怎么部署。
>
> 本文数字全部来自 `7_rag_project.py` 的实跑输出，以及一组测量各阶段耗时的探针（脚本已删除，均可复现）。

---

## 0. 先看真实运行

**第一步，建索引（离线）：**

```bash
python 7_rag_project.py --mode index --docs ./my_docs
```

```
加载文档: ./my_docs
加载了 2 个文档
切分为 2 个块
索引已保存到 ./rag_db
```

**第二步，问答（在线）：**

```bash
python 7_rag_project.py --mode chat
```

```
文档问答助手已启动（输入 exit 退出）
----------------------------------------

你: Python并发有哪些方案？
助手: Python 的并发编程有三条路：多线程（threading）、多进程（multiprocessing）和异步 IO（asyncio）。
- 多线程受 GIL 限制，适合 IO 密集型任务；
- 多进程可绕过 GIL，真正并行，适合 CPU 密集型任务；
- asyncio 是单线程事件循环模型，适合高并发 IO 场景。

信息来源：my_docs\concurrency.txt

你: Chroma的score越大越相关吗？
助手: 不是。根据文档，Chroma 的 `similarity_search_with_score` 返回的是**距离**而不是相似度，分数越小代表越相关。

来源: my_docs\chroma.md

你: exit
再见！
```

> ⚠️ 两处诚实标注：① **LLM 的回答措辞每次运行都不同**（即使 `temperature=0`）；② 更值得注意的是，**连"来源"的格式也是模型自己挑的**——上面两次分别写成 `信息来源：`（全角冒号、无方括号）和 `来源:`（半角冒号），而 `format_docs` 拼进上下文的原文其实是 `[来源: xxx]`。**检索命中的文件、以及回答的内容依据，才是稳定复现的部分。**

三件值得注意的事：

1. **答案里带出了文件名（`my_docs\concurrency.txt` / `my_docs\chroma.md`），但它只是被模型"复述"出来的。** 来源信息是 `format_docs` 拼进上下文的，模型抄的时候**改了格式**（方括号没了、冒号时全角时半角）。**所以"来源"不能当程序保证**——真实来源要在代码里独立记录（第 5 节会说清这个区别）。
2. **第二条回答里出现了 `` `similarity_search_with_score` `` 这种带反引号的代码格式**——因为文档原文就是这么写的（`chroma.md` 里原句是"返回的是**距离**而不是相似度，所以分数越小代表越相关"）。**这是 RAG 在工作的直接证据**：答案的措辞和文档高度重合，而不是模型自己的话。
3. 两条查询，`k=3`，但**返回的都只有 2 条**——库里一共就 2 条。检索器不会报错，也不会凭空补足（第 4 节解释这个行为）。

---

## 1. 工程结构：为什么必须分成两条命令

### 不是"为了整齐"，是因为这两个阶段的触发频率差了几个数量级

```
        ┌──────────────── 离线：文档变了才跑 ────────────────┐
        │                                                   │
  my_docs/ ──加载──→ 切分 ──→ embedding ──→ ./rag_db/       │
  （你的语料）                                （向量+原文）  │
        │                                                   │
        └───────────────────────────────────────────────────┘
                                    ↑
                          --mode index （跑 1 次）

        ┌──────────────── 在线：每次提问都跑 ────────────────┐
        │                                                   │
  用户问题 ──→ embedding ──→ 检索 ./rag_db/ ──→ LLM ──→ 答案 │
        │                                                   │
        └───────────────────────────────────────────────────┘
                          --mode chat （跑 N 次）
```

**把索引期和查询期分开，是 RAG 工程最基本的一条分界线**（第 1 篇讲过这个不对称）。理由是成本结构完全不同：

| | 索引期 | 查询期 |
|---|---|---|
| 触发频率 | 文档变更时，可能一天一次 | 每次用户提问 |
| 单次数据量 | **全库**（几万块都可能） | 1 个问题 |
| 用户是否在等 | 否（可以半夜跑） | **是（延迟直接决定体验）** |
| 能否失败重试 | 可以，重跑就行 | 不能，用户已经走了 |

### 但实测揭穿了一个常见误解："离线所以便宜，在线所以贵"

我把两个模式端到端计了时（同一个 2 篇文档的库）：

| 阶段 | index 模式 | chat 模式 |
|---|---|---|
| **embedding 模型实例化** | **8.99 秒** | **8.99 秒** |
| 加载文档 | 0.004 秒 | — |
| 切分 | 0.0002 秒 | — |
| 向量化 + 写盘（`from_documents`） | 1.01 秒 | — |
| 连库（`Chroma(persist_directory=...)`） | — | 0.009 秒 |
| **合计** | **≈ 10.0 秒** | **≈ 9.0 秒** |

```
index   ████████████████████████████████████████▏  10.0s
         └────── 8.99s 加载模型 ──────┘└1.01s┘

chat    ████████████████████████████████████▏       9.0s
         └────── 8.99s 加载模型 ──────┘└0.009s┘
```

**两个结论，都很实用：**

**第一，`chat` 模式的启动成本几乎等于 `index` 模式的全部成本。** 因为查询时也必须把问题编码成向量，而编码必须用**同一个模型**——所以 `get_embeddings()` 在 `chat()` 里也要调一次，8.99 秒一分不少。

> 这意味着：**如果你把它做成 Web 服务，绝不能在每次请求里调 `get_embeddings()`。** 一次请求等 9 秒，是不可接受的。正确做法是**在服务启动时初始化一次、全局复用**（"进程常驻"），或者把 embedding 拆成独立服务。

**第二，真正贵的不是"向量化"，是"加载模型"。** 向量化 2 块只用了 1.01 秒（含写盘），而**把模型从磁盘读进内存要 8.99 秒**。这个比例（≈9:1）会颠覆很多人的优化直觉——你优化切分策略、优化批大小，收益都在那 1 秒里；而**复用进程能一次性省掉 9 秒**。

> 顺带一个诚实的补充：8.99 秒是本机（CPU）从本地缓存加载 bge-small-zh 的耗时。**首次运行还要额外下载约 100MB**，那是分钟级。所以"第一次跑很慢"和"每次跑很慢"是两回事。

---

## 2. 索引模式：三步拆解

```python
def build_index(docs_dir: str):
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

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"切分为 {len(chunks)} 个块")

    embeddings = get_embeddings()
    db = Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    print(f"索引已保存到 {PERSIST_DIR}")
```

### 三个必须看懂的细节

**(1) `loader_kwargs={"encoding": "utf-8"}` 不是可选项，是 Windows 上的必需品。**

`TextLoader` 默认用系统编码（中文 Windows 上是 GBK）。我们的文档是 UTF-8，不加这一行就会：

```
UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position xxx
```

**这类报错很容易被误判成"文档坏了"，其实是编码声明缺失。**

**(2) 为什么写了两个 `DirectoryLoader` 而不是一个？**

因为 `glob` 一次只吃一种模式。想同时加载 `.txt` 和 `.md`，要么写 `glob="**/*.*"`（会把图片、`.py` 也吃进来），要么像这里分开写两遍再 `extend`。**这里的写法是显式、可控的**。

**(3) ⚠️ 诚实标注：`UnstructuredMarkdownLoader` 被 import 了，但没用上。**

来看第 19-21 行的导入：

```python
from langchain_community.document_loaders import (
    TextLoader, DirectoryLoader, UnstructuredMarkdownLoader,
)
```

但实际加载 `.md` 用的是 `TextLoader`。这是一个**遗留的不规范写法**——`UnstructuredMarkdownLoader` 会把 Markdown 解析成**结构化的元素**（标题、列表、代码块分开成不同 Document，带 `category` 元数据），这是第 2 篇讲过的"Markdown 切分"能力。本脚本为了简单，直接当纯文本读了，代价是**丢失了标题层级信息**。

**这不是 bug，但要心里有数**：如果你想让检索结果按"章节"组织，就该换上 `UnstructuredMarkdownLoader`（需要 `pip install unstructured markdown`）。

### 实测：这里的 `chunk_size=500` 其实一次都没生效

```
加载了 2 个文档
切分为 2 个块
```

**2 个文档 → 2 个块，一个都没被切开。** 因为两个文件都小于 `chunk_size=500`：

| 文件 | 字符数 | token 数 | 是否超过 500 字符 | 是否超过 512 token |
|---|---|---|---|---|
| `my_docs/concurrency.txt` | 397 | 293 | 否 | 否 |
| `my_docs/chroma.md` | 373 | 266 | 否 | 否 |

切分耗时 **0.0002 秒**——因为它实际上只是"原样复制一遍"。

**这是个很好的提醒**：`chunk_size` 只在文档**真的超长**时才起作用。第 2 篇做过大规模切分实验（4 块、5 块、膨胀率 1.50x），那些数字来自长文档；在短文档上，**切分器是个空转的组件**。

> 同时注意 token 列：293 和 266，都**远小于 bge 的 512 token 上限**，所以第 3 篇讲的"静默截断"在这里没有发生。**这就是"先量一量再选参数"的价值**——量完才发现参数根本不影响结果。

---

## 3. 持久化：`--mode index` 的真实陷阱

第 3 篇和第 5 篇都预告过这一点，这里给出完整说明。

### 实测：重复执行 index，库会一直长大

我从一个**干净的空库**开始，连续执行三次 index：

```
[5] 首次 from_documents 耗时 1.01s, count = 2
[9] 第 2 次 index 之后 count = 4
[9] 第 3 次 index 之后 count = 6
```

```
count  2 ──┐
           │  再跑一次 --mode index
       4 ──┤
           │  再跑一次 --mode index
       6 ──┘        文档没变，但库膨胀了 3 倍
```

**原因**（第 3 篇第 7 节已经解释过）：`Chroma.from_documents` 的语义是"**往 collection 里写入**"，不是"清空重建"。LangChain 默认的 collection 名是 `"langchain"`，而 `persist_directory="./rag_db"` 决定库文件的位置。**同名 collection 已存在时，文档被追加。**

### 后果：Top-K 名额被自己的副本吃掉

库从 2 条变成 6 条（3 份副本）之后，同一个查询的结果：

```
[10] 库被写脏之后，同一个查询返回：
      my_docs\concurrency.txt | Python 的并发编程有三条路：多线程（threa
      my_docs\concurrency.txt | Python 的并发编程有三条路：多线程（threa   ← 同一份！
      my_docs\chroma.md       | # Chroma 使用要点  Chroma 是一个轻
      唯一内容数 = 2  返回条数 = 3
```

**`k=3` 的 3 个名额，有 2 个被同一份文档的副本占掉了。**

这个后果在**小库上还不算致命**（内容确实相关，只是浪费名额），但在**大库上会毁掉检索质量**：

```
假设你有一万条文档，某次更新后跑了两遍 index → 库里两万条
再查一个冷门问题 → k=5 的结果里可能有 4 条是同一条文档的副本
                              ↑ 唯一信息量 = 2 条，而且可能不包含答案
```

**更隐蔽的是**：向量库不会报任何错，检索也能正常返回结果，**你只会觉得"检索质量莫名其妙变差了"**。

### 三种规避方法

| 方法 | 写法 | 适用 |
|---|---|---|
| **① 索引前先清空目录**（最简单） | 删掉整个 `./rag_db` 再跑 | 全量重建的场景，本文推荐 |
| **② 先删 collection 再写** | `db.delete_collection()` 或用 `Chroma(...)` 连上后删 | 想保留库文件结构 |
| **③ 用带版本/时间戳的 collection 名** | `collection_name=f"docs_{hash}"` | 需要保留历史版本、可回滚 |

**① 的具体做法**（在 `build_index` 开头加两行）：

```python
import shutil
shutil.rmtree(PERSIST_DIR, ignore_errors=True)   # 清掉旧库，保证"重建"语义
```

> **为什么我把 ① 列为推荐？** 因为 `--mode index` 的语义应该是"**重建索引**"。而 `from_documents` 的语义是"追加"。**语义不匹配就是坑的来源。** 要么改代码匹配语义（① ②），要么给出一个能区分批次的名字（③）。**不要什么都不做。**

**通用的调试动作**（第 5 篇也强调过）：**检索结果反常时，第一件事是数库里有几条。**

```python
print(db._collection.count())
```

---

## 4. 问答模式：交互循环逐行拆解

```python
def chat():
    embeddings = get_embeddings()
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
```

### 逐块说明

**① 连库时必须传 `embedding_function`（第 3 篇讲过）**

```python
db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
```

**库里存的是向量，不是文本的"意思"。** 查询时要用**同一个模型**把问题编码到**同一个坐标系**。换模型 = 换坐标系，检索结果会完全错乱。

**② 为什么检索器选 `mmr` 而不是默认的 `similarity`？**

第 4 篇的核心结论：默认相似度检索会返回**一堆互相雷同**的结果（都挤在语义最热的那个点上）。`mmr` 在"相关"和"多样"之间做权衡，实测能把冗余的第二条换掉。

```python
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
```

**③ `k=3`，但库只有 2 条 → 实测返回 2 条**

```
[7] Q: Python并发有哪些方案？   MMR耗时 20ms  返回 2 条
```

**检索器不会报错，也不会凭空补足。** 这和第 5 篇讲的 `Go语言怎么样？` 是同一类行为的另一面：

```
库里有 5 条，问库外的问题 → 照样返回 2 条（尽力而返）
库里有 2 条，要 3 条       → 返回 2 条（有多少给多少）
```

**`similarity_search` 从不判断"够不够"，它只负责"按距离排序取前 k 个"。** 判断"有没有相关内容"是**你的 Prompt 要负责的事**（下面第 ⑤ 条）。

**④ `temperature=0` 是 RAG 场景的默认选择**

RAG 要的是"**忠实复述资料**"，不是"创意发挥"。温度越高，模型越倾向于"用漂亮的说法改写"，而改写就意味着**偏离原文**。**在事实问答场景，`temperature=0` 是基线，不是可调项。**

**⑤ Prompt 里的三句话，各有分工**

| 句子 | 作用 |
|---|---|
| `你是一个文档问答助手。基于以下参考资料回答问题。` | 限定回答依据（**约束**） |
| `如果资料中没有相关信息，请说'文档中未找到相关信息'。` | 给出**标准弃权话术**（第 5 篇讲过：明确给出话术，模型才会用） |
| `回答后标注信息来源。` | 让模型复述 `format_docs` 拼进去的 `[来源: ...]` |

**第二句是防幻觉的关键，第三句是让来源"可见"的关键。**

**⑥ 交互循环本身很朴素，但有两个细节**

```python
q = input("\n你: ").strip()
if q.lower() in ("exit", "quit", "q"):    # 大小写不敏感 + 三种退出写法
    ...
if not q:                                  # 空行直接跳过，不送给 LLM
    continue
```

**`if not q: continue` 这一行是在省钱**——空回车不该触发一次 API 调用。

> ⚠️ **这段循环有一个能力缺口：它没有多轮记忆。** 每轮 `chain.invoke(q)` 都是**孤立的**——问"它怎么用？"里的"它"没有任何指代对象。第 7 节会把这个列进"离能用还差什么"。

---

## 5. 来源追溯是怎么实现的

**这是本文和前面几篇最不同的一处工程细节。**

第 5 篇里，来源是**在链外单独打印**的：

```python
docs = retriever.invoke(query)   # 直接拿 Document 读 metadata
```

本篇的做法是**把来源拼进上下文**，让答案自己带上它：

```python
def format_docs(docs):
    return "\n---\n".join(
        f"[来源: {d.metadata.get('source', '未知')}]\n{d.page_content}"
        for d in docs
    )
```

拼出来的 `context` 长这样：

```
[来源: my_docs\concurrency.txt]
Python 的并发编程有三条路：多线程（threading）、多进程（multiprocessing）和异步 IO（asyncio）。
---
[来源: my_docs\chroma.md]
# Chroma 使用要点
Chroma 是一个轻量的嵌入式向量数据库……
```

**两种方案怎么选？**

| 方案 | 优点 | 缺点 |
|---|---|---|
| **链外打印 metadata**（第 5 篇） | 来源**绝对可靠**（`metadata` 是程序写的，模型改不了） | 只出现在日志里，用户看不到 |
| **拼进上下文**（本篇） | 用户直接看到来源；模型还能在句子里引用 | 来源**可能被模型忽略或写错** |

**注意这里的取舍：拼进上下文之后，"来源"变成了模型要复述的内容——它可能漏掉，甚至写错。** 我们的实测正好抓到了这一点：上下文里明明是 `[来源: my_docs\concurrency.txt]`，模型复述出来却变成了 `信息来源：my_docs\concurrency.txt`（另一次是 `[来源: ...]` 原样）。**文件名对上了，格式被模型改了**——这正说明它是模型的配合，不是程序保证。

> **生产环境的做法是"两个都要"**：用 `format_docs` 把来源喂给模型（让答案可读），同时**在代码里独立记录真实的 retrieval 结果**（供审计、评估、排错）。**不要把事实性信息交给模型去保证。**

---

## 6. 用第 4、5 篇的判据检验这个项目

第 4 篇提出过"相对间隔"判据：`(score₂ − score₁)/score₁`。这是**第三次**在不同的库上验证它：

| 查询 | Top-1 `score` | Top-2 `score` | **相对间隔** | 检索到的来源 | 是否命中 |
|---|---|---|---|---|---|
| `Python并发有哪些方案？` | 0.5104 | 1.0229 | **100.4%** | concurrency.txt | ✅ |
| `Chroma的score越大越相关吗？` | 0.8234 | 1.2544 | **52.3%** | chroma.md | ✅ |
| `红烧肉怎么做？`（无关） | 1.4925 | 1.5055 | **0.9%** | chroma.md | ❌ |

**三次独立验证的合并结论：**

```
           md4（5 条文档）  md5（5 条文档）  md7（2 条文档）
命中查询      26.9%~41.7%      21.0%~70.4%      52.3%~100.4%
无关查询          2.9%             1.1%             0.9%
                    └────────── 始终隔着 10 倍以上空档 ──────────┘
```

**三套不同的文档、三种不同的查询，空档一直存在。** 这个判据（"相对间隔 < 10% 就认为库里没有相关内容"）可以放心当作**设阈值的起点**。

同时注意最后一行：**`红烧肉怎么做？` 的绝对分数是 1.49，比命中查询的 0.51 高了 3 倍。** 这再次印证第 3 篇的结论——**绝对阈值（比如"score > 0.7 才算命中"）在小库上完全失效**，只有**相对间隔**才有判别力。

> ⚠️ 仍然要诚实标注局限：这里每个数据集只有 3~5 个样本，**不足以证明因果关系，只能说观察到了稳定的相关性**。要做严肃评估，需要几十上百条标注数据 + Hit Rate / MRR / Recall@k。

---

## 7. 这个项目离"能用"还差什么

它现在能跑通全流程，但作为一个**产品**还缺 6 样东西。按**优先级**排：

| 缺口 | 现象 | 怎么补 | 优先级 |
|---|---|---|---|
| **索引重建语义错误** | 重复跑 index 库就膨胀（第 3 节实测 2→4→6） | `shutil.rmtree(PERSIST_DIR)` 或 `delete_collection()` | 🔴 **最高**（会静默损害质量） |
| **没有评估集** | 改任何参数都是"感觉变好了"（第 6 篇的核心） | 攒 20~100 条问答对 + Hit Rate/MRR | 🔴 **最高**（没有它，其他优化都是瞎猜） |
| **没有多轮对话** | 追问"它怎么用？"无法指代 | 把历史 + 重写后的问题一起送进 chain | 🟡 高（影响可用性） |
| **文档更新无感知** | 改了 `my_docs` 必须手动重跑 index | 记录文件 mtime/hash，变了才重建 | 🟡 高（运维问题） |
| **单进程、无并发** | 每个请求等 9 秒（第 1 节的模型加载） | 服务化 + 进程常驻 embedding 模型 | 🟡 高（上生产必须） |
| **无流式输出** | 答案要等 LLM 全部生成完才出现 | 把 `invoke` 换成 `stream`（第 5 篇讲过 `Runnable` 有 `stream`） | 🟢 中（体验问题） |

```
一个常见的错误顺序：
   先追求"高级"（Rerank、HyDE、多查询）
   却让"索引重建"和"评估集"这两件最基础的事缺着
                        ↑ 第 6 篇实测过：这些高级技巧在本例中收益为零、代价 400 倍
```

**最后一条想说的是**：这 6 项里没有一项是"高级技巧"。它们全是**工程基本功**。而第 6 篇的实测数据说明——**基本功没做好时，高级技巧往往是在给不存在的收益付费。**

---

## 8. 一个必须知道的警告

运行 `--mode chat` 时，会打印这样一行：

```
LangChainDeprecationWarning: The class `Chroma` was deprecated in LangChain 0.2.9
and will be removed in 1.0. An updated version of the class exists in the
langchain-chroma package and should be used instead.
```

**这不是错误，是迁移提示。** `langchain_community.vectorstores.Chroma` 在 0.2.9 之后被标记为废弃，官方把 Chroma 集成拆成了独立的 `langchain-chroma` 包：

```python
# 未来写法（需要 pip install langchain-chroma）
from langchain_chroma import Chroma
```

**本脚本（以及前面 6 篇）用的都是旧写法**，功能完全一样，只是包的位置变了。要迁移的话，就是换一个 import 路径，代码逻辑一行都不用改。

> **顺带说一个真实的版本兼容教训**：本教程实测通过的版本组合是 langchain 0.3.30 + langchain-community + chromadb 1.5.9 + langchain-huggingface 0.3.1 + sentence-transformers 5.1.2。**LangChain 生态的版本漂移很快，遇到 `ImportError` 或行为差异时，先怀疑版本，再看代码。**

---

## 代码

`7_rag_project.py` 按功能分三块：

| 代码位置 | 做什么 | 对应本文 | 实测输出 |
|---|---|---|---|
| `build_index()` | 加载 → 切分 → 向量化 → 持久化 | 第 2、3 节 | 2 文档 → 2 块；`count = 2` |
| `chat()` | 连库 → retriever → chain → 交互循环 | 第 4、5 节 | 两条查询都带 `[来源: ...]` |
| `__main__` | 解析 `--mode` / `--docs` | 第 1 节 | `--mode index` / `--mode chat` |

**运行前置：根目录 `.env` 必须有这两个值**（Embedding 走本地模型，不需要 API Key；`OPENAI_*` 是你自己的 LLM）：

```
OPENAI_API_KEY=你的key
OPENAI_BASE_URL=你的兼容端点
OPENAI_MODEL=你的模型名
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
HF_ENDPOINT=https://hf-mirror.com      # 直连 huggingface.co 超时的话加这行
```

**还要准备 `my_docs/` 目录。** 本文实测用的是两个文件：`concurrency.txt`（397 字符 / 293 token，讲 Python 并发三种方案）和 `chroma.md`（373 字符 / 266 token，讲 Chroma 的距离度量与持久化）。**建议照着同一模式准备你自己的三个文件，让"命中"和"未命中"都能复现。**

**建议动手改三个地方，亲眼确认本文的结论：**

1. **把 `k=3` 改成 `k=50`**，观察返回条数**仍然是 2**（库里只有 2 条）——验证"检索器有多少给多少，且从不报错"。
2. **连续执行两次 `--mode index`**，然后打印 `db._collection.count()`，看它从 2 变成 4 —— 复现第 3 节的膨胀陷阱，再自己加上 `shutil.rmtree(PERSIST_DIR, ignore_errors=True)` 验证修复。
3. **在 `chat()` 开头加一行计时**，量出 `get_embeddings()` 的耗时（本文实测 8.99 秒）——亲自确认"启动成本的大头在哪里"：

```python
import time
t0 = time.perf_counter()
embeddings = get_embeddings()
print(f"加载 embedding 模型: {time.perf_counter() - t0:.2f}s")
```

```bash
python 7_rag_project.py --mode index --docs ./my_docs
python 7_rag_project.py --mode chat
```