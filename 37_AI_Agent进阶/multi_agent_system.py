"""
多Agent系统设计
==========

介绍多Agent系统的设计和协作模式。
"""

print("=" * 60)
print("1. 多Agent系统概述")
print("=" * 60)

print("多Agent系统:")
print("  - 多个Agent协同工作")
print("  - 角色分工明确")
print("  - 解决复杂任务")
print()
print("优势:")
print("  - 模块化设计")
print("  - 可扩展性强")
print("  - 专业分工")
print("  - 错误隔离")

print()
print("=" * 60)
print("2. Agent角色设计")
print("=" * 60)

print("2.1 角色类型")
print("  - 规划者(Planner): 分解任务")
print("  - 执行者(Executor): 具体执行")
print("  - 审核者(Reviewer): 检查结果")
print("  - 协调者(Coordinator): 协调流程")
print()
print("2.2 角色Prompt示例")
print('''
# 研究者Agent
RESEARCHER_PROMPT = """你是一个专业的研究员。
你的任务是:
1. 搜索相关信息
2. 分析和整理资料
3. 提供客观的研究报告

请用专业的态度完成研究任务。"""

# 写作者Agent
WRITER_PROMPT = """你是一个专业的技术作家。
你的任务是:
1. 根据研究资料撰写内容
2. 确保文章逻辑清晰
3. 使用通俗易懂的语言

请创作高质量的内容。"""

# 审核者Agent
REVIEWER_PROMPT = """你是一个严格的内容审核员。
你的任务是:
1. 检查内容的准确性
2. 指出逻辑问题
3. 提供改进建议

请客观公正地审核。"""
''')

print()
print("=" * 60)
print("3. 基础协作模式")
print("=" * 60)

print("3.1 串行协作")
print("  Agent1 -> Agent2 -> Agent3")
print("  任务按顺序执行，下游Agent使用上游输出")
print()
print("3.2 并行协作")
print("  /Agent1")
print("  Task -> Agent2")
print("  \\Agent3")
print("  多个Agent同时处理子任务")
print()
print("3.3 循环协作")
print("  Agent1 <-> Agent2")
print("  Agent之间反复交互直到达成共识")

print()
print("=" * 60)
print("4. 简单多Agent实现")
print("=" * 60)

print('''
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 研究Agent
research_tools = [
    Tool(name="搜索", func=lambda x: f"搜索: {x}", description="搜索")
]
researcher = initialize_agent(
    research_tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 写作Agent
write_tools = [
    Tool(name="写作", func=lambda x: f"已写作: {x}", description="写作")
]
writer = initialize_agent(
    write_tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 审核Agent
review_tools = [
    Tool(name="审核", func=lambda x: f"审核: {x}", description="审核")
]
reviewer = initialize_agent(
    review_tools, llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 协作流程
class MultiAgentWorkflow:
    def execute(self, topic):
        # 1. 研究
        research_result = researcher.run(f"研究: {topic}")

        # 2. 写作
        draft = writer.run(f"基于以下内容写作: {research_result}")

        # 3. 审核
        feedback = reviewer.run(f"审核以下内容: {draft}")

        return feedback

workflow = MultiAgentWorkflow()
result = workflow.execute("AI未来发展")
''')

print()
print("=" * 60)
print("5. Agent通信协议")
print("=" * 60)

print("5.1 消息格式")
print('''
class AgentMessage:
    def __init__(self, sender, receiver, content, msg_type="text"):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.type = msg_type
        self.timestamp = datetime.now()

# 消息示例
msg = AgentMessage(
    sender="researcher",
    receiver="writer",
    content="研究完成: AI有3个发展趋势...",
    msg_type="research_result"
)
''')

print()
print("5.2 通信机制")
print('''
class AgentCommunication:
    def __init__(self):
        self.message_queue = []

    def send(self, message):
        self.message_queue.append(message)

    def receive(self, agent_name):
        messages = [m for m in self.message_queue if m.receiver == agent_name]
        self.message_queue = [m for m in self.message_queue if m.receiver != agent_name]
        return messages
''')

print()
print("=" * 60)
print("6. 任务分配策略")
print("=" * 60)

print("6.1 静态分配")
print("  - 预先定义每个Agent的角色")
print("  - 固定的任务流程")
print()
print("6.2 动态分配")
print("  - 根据任务类型分配")
print("  - Agent能力评估")
print()
print("6.3 混合模式")
print("  - 基础流程固定")
print("  - 特殊任务动态分配")

print()
print("=" * 60)
print("7. 团队协作模式")
print("=" * 60)

print("7.1 角色扮演团队")
print('''
# AI团队模拟
TEAM_STRUCTURE = {
    "CEO": {"role": "决策", "agents": ["coordinator"]},
    "CTO": {"role": "技术", "agents": ["researcher", "coder"]},
    "CFO": {"role": "财务", "agents": ["analyst"]}
}

# 协作流程
def team_collaborate(task):
    coordinator = get_agent("coordinator")
    plan = coordinator.plan(task)

    for dept in plan["departments"]:
        execute_department_task(dept)

    return compile_results()
''')

print()
print("7.2 辩论/协商模式")
print('''
# 多Agent辩论
class DebateSystem:
    def __init__(self, topic):
        self.topic = topic
        self.agents = [ProAgent(), ConAgent(), Moderator()]

    def run_debate(self, rounds=3):
        for round in range(rounds):
            # 正方观点
            pro = self.agents[0].argue(self.topic)

            # 反方观点
            con = self.agents[1].argue(self.topic, opposing=pro)

            # 总结
            summary = self.agents[2].summarize(pro, con)

        return summary
''')

print()
print("=" * 60)
print("8. 共享上下文")
print("=" * 60)

print("8.1 共享内存")
print('''
from langchain.memory import ConversationBufferMemory
import json

class SharedContext:
    def __init__(self):
        self.context = {
            "task": None,
            "research": [],
            "drafts": [],
            "reviews": []
        }

    def add_research(self, agent_name, content):
        self.context["research"].append({
            "agent": agent_name,
            "content": content
        })

    def get_context(self):
        return json.dumps(self.context, ensure_ascii=False)

# 使用
shared = SharedContext()
shared.add_research("researcher", "AI发展趋势...")
''')

print()
print("8.2 知识共享")
print('''
# 共享知识库
class KnowledgeBase:
    def __init__(self):
        self.facts = {}
        self.agents_access = {}

    def add_fact(self, key, value, agents):
        self.facts[key] = value
        self.agents_access[key] = agents

    def get_fact(self, key, agent):
        if agent in self.agents_access.get(key, []):
            return self.facts.get(key)
        return None
''')

print()
print("=" * 60)
print("9. 冲突处理")
print("=" * 60)

print("9.1 投票机制")
print('''
def resolve_conflict(options):
    votes = {opt: 0 for opt in options}
    for agent in agents:
        votes[agent.vote(options)] += 1

    return max(votes, key=votes.get)
''')

print()
print("9.2 仲裁机制")
print('''
def resolve_with_arbitrator(issue):
    proposals = [agent.propose(issue) for agent in agents]

    # 仲裁者决定
    decision = arbitrator.judge(proposals)

    return decision
''')

print()
print("=" * 60)
print("10. 多Agent系统架构")
print("=" * 60)

print("架构图:")
print()
print("  +-----------+")
print("  |  用户输入  |")
print("  +-----+-----+")
print("        |")
print("  +-----+-----+")
print("  |  协调者   |")
print("  +-----+-----+")
print("        |")
print("  +-----+-----+")
print("  | 任务分发  |")
print("  +-----+-----+")
print("    |   |   |")
print("  +---+ +---+ +---+")
print("  |A1 | |A2 | |A3 |")
print("  +---+ +---+ +---+")
print("    \\   |   /")
print("     +-----+")
print("     |聚合|")
print("     +-----+")

print()
print("=" * 60)
print("11. 多Agent系统总结")
print("=" * 60)

print("多Agent系统要点:")
print()
print("* 协作模式:")
print("  - 串行、并行、循环")
print()
print("* 角色设计:")
print("  - 规划、执行、审核、协调")
print()
print("* 关键组件:")
print("  - 通信协议、任务分配、共享上下文")
print()
print("* 挑战:")
print("  - 通信开销、冲突处理、协同效率")
