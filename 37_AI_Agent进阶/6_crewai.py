"""
6. CrewAI框架 - 代码示例
演示CrewAI的角色扮演多Agent协作。
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)


# ============================================================
# 示例1: 基础团队（研究员 + 写手）
# ============================================================
def demo_basic_crew():
    """两人团队：研究员调研 → 写手撰写"""

    # 定义Agent（角色 + 目标 + 背景）
    researcher = Agent(
        role="高级AI研究员",
        goal="发现关于指定主题的最新趋势和关键信息",
        backstory="你是一位有10年经验的AI领域研究员，擅长快速定位核心信息。",
        llm=llm,
        verbose=True,
    )

    writer = Agent(
        role="技术博客作家",
        goal="将研究内容写成通俗易懂的技术文章",
        backstory="你是一位技术博客作家，擅长把复杂概念用简单语言解释清楚。",
        llm=llm,
        verbose=True,
    )

    # 定义Task
    research_task = Task(
        description="调研'LLM Agent的最新发展趋势'，列出3个关键趋势和简要说明。",
        expected_output="包含3个关键趋势的研究报告，每个趋势有标题和2-3句说明。",
        agent=researcher,
    )

    write_task = Task(
        description="基于研究报告，写一篇200字左右的技术博客文章。",
        expected_output="一篇结构清晰、通俗易懂的短文。",
        agent=writer,
    )

    # 组建Crew并执行
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,  # 顺序执行
        verbose=True,
    )

    result = crew.kickoff()
    print(f"\n最终输出:\n{result}")


# ============================================================
# 示例2: 三人团队（研究员 + 写手 + 审核员）
# ============================================================
def demo_review_crew():
    """三人团队：研究 → 写作 → 审核"""

    researcher = Agent(
        role="研究员",
        goal="收集准确的技术信息",
        backstory="资深技术研究员，注重数据和事实。",
        llm=llm,
    )

    writer = Agent(
        role="写手",
        goal="写出高质量的技术内容",
        backstory="经验丰富的技术作家。",
        llm=llm,
    )

    reviewer = Agent(
        role="审核员",
        goal="确保内容准确、完整、高质量",
        backstory="严格的内容审核专家，善于发现问题。",
        llm=llm,
    )

    tasks = [
        Task(
            description="调研Python异步编程的核心概念和最佳实践。",
            expected_output="包含核心概念和3条最佳实践的研究报告。",
            agent=researcher,
        ),
        Task(
            description="基于研究报告写一篇教程文章。",
            expected_output="一篇结构清晰的教程短文。",
            agent=writer,
        ),
        Task(
            description="审核文章，检查准确性和完整性，给出评分和改进建议。",
            expected_output="审核报告：评分(1-10)、问题列表、改进建议。",
            agent=reviewer,
        ),
    ]

    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    print(f"\n审核结果:\n{result}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("示例1: 基础两人团队")
    print("=" * 60)
    demo_basic_crew()

    # print("\n" + "=" * 60)
    # print("示例2: 三人审核团队")
    # print("=" * 60)
    # demo_review_crew()
