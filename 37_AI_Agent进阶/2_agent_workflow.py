"""
2. Agent工作流 - 代码示例
演示顺序、条件、循环三种工作流模式。
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ============================================================
# 示例1: 顺序工作流（LCEL管道）
# ============================================================
def demo_sequential():
    """用LCEL构建 摘要 → 翻译 的顺序工作流"""
    summarize = ChatPromptTemplate.from_template("用3句话总结以下内容:\n{text}")
    translate = ChatPromptTemplate.from_template("把以下中文翻译成英文:\n{text}")

    # 摘要链
    summary_chain = summarize | llm | StrOutputParser()
    # 翻译链（需要把上一步输出包装成dict）
    translate_chain = translate | llm | StrOutputParser()

    text = "Python是一种广泛使用的高级编程语言，以其简洁的语法和丰富的库生态著称。"
    summary = summary_chain.invoke({"text": text})
    print(f"摘要: {summary}")

    translation = translate_chain.invoke({"text": summary})
    print(f"翻译: {translation}")


# ============================================================
# 示例2: 条件工作流
# ============================================================
def demo_conditional():
    """根据任务类型选择不同处理路径"""

    def classify_task(task: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "判断以下任务属于哪个类型，只回答一个词(research/coding/writing):\n{task}"
        )
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"task": task}).strip().lower()

    def handle_research(task):
        return f"[研究路径] 正在搜索'{task}'的相关资料..."

    def handle_coding(task):
        return f"[编程路径] 正在生成'{task}'的代码..."

    def handle_writing(task):
        return f"[写作路径] 正在撰写'{task}'的内容..."

    handlers = {
        "research": handle_research,
        "coding": handle_coding,
        "writing": handle_writing,
    }

    # 测试不同类型的任务
    tasks = [
        "调研一下目前主流的向量数据库",
        "写一个快速排序算法",
        "写一篇关于AI的博客文章",
    ]
    for task in tasks:
        task_type = classify_task(task)
        handler = handlers.get(task_type, handle_research)
        result = handler(task)
        print(f"任务: {task}\n类型: {task_type}\n结果: {result}\n")


# ============================================================
# 示例3: 循环工作流（迭代改进）
# ============================================================
def demo_iterative():
    """生成 → 检查 → 不满意则反馈重来"""

    generate_prompt = ChatPromptTemplate.from_template(
        "写一个关于'{topic}'的一段话（50字左右）。{feedback}"
    )
    check_prompt = ChatPromptTemplate.from_template(
        "评价以下内容质量，回答'通过'或'不通过，原因:...':\n{content}"
    )

    generate_chain = generate_prompt | llm | StrOutputParser()
    check_chain = check_prompt | llm | StrOutputParser()

    topic = "Python的优势"
    feedback = ""
    max_iterations = 3

    for i in range(max_iterations):
        print(f"\n--- 第{i+1}轮 ---")
        content = generate_chain.invoke({"topic": topic, "feedback": feedback})
        print(f"生成: {content}")

        check = check_chain.invoke({"content": content})
        print(f"检查: {check}")

        if "通过" in check and "不通过" not in check:
            print("✓ 质量通过")
            break
        else:
            feedback = f"\n上次的反馈: {check}，请改进。"
            print("✗ 需要改进，继续迭代...")
    else:
        print(f"达到最大迭代次数({max_iterations})，使用最后版本")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("示例1: 顺序工作流")
    print("=" * 60)
    demo_sequential()

    print("\n" + "=" * 60)
    print("示例2: 条件工作流")
    print("=" * 60)
    demo_conditional()

    print("\n" + "=" * 60)
    print("示例3: 循环工作流")
    print("=" * 60)
    demo_iterative()
