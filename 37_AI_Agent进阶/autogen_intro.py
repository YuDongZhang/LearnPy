"""
AutoGen入门
==========

介绍Microsoft AutoGen框架的使用。
"""

print("=" * 60)
print("1. AutoGen概述")
print("=" * 60)

print("AutoGen:")
print("  - Microsoft推出的多Agent框架")
print("  - 简化多Agent系统构建")
print("  - 支持自定义Agent")
print("  - 灵活的对话模式")
print()
print("核心特性:")
print("  - 自动化Agent协作")
print("  - 人类参与工作流")
print("  - 代码生成执行")
print("  - 可扩展性强")

print()
print("=" * 60)
print("2. 安装")
print("=" * 60)

print("pip install pyautogen")
print()
print("或从源码安装:")
print("pip install git+https://github.com/microsoft/autogen.git")

print()
print("=" * 60)
print("3. 基础示例")
print("=" * 60)

print('''
import autogen

# 1. 配置LLM
config_list = [
    {
        "model": "gpt-4",
        "api_key": "your-api-key"
    }
]

# 2. 创建AssistantAgent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)

# 3. 创建UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10
)

# 4. 开始对话
user_proxy.initiate_chat(
    assistant,
    message="写一个Python快速排序算法"
)
''')

print()
print("=" * 60)
print("4. Agent类型")
print("=" * 60)

print("4.1 AssistantAgent")
print('''
# AI助手Agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="你是一个专业的Python开发者。"
)
''')

print()
print("4.2 UserProxyAgent")
print('''
# 用户代理Agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",  # 模式选项
    # NEVER: 不需要人类输入
    # TERMINATE: 需要时请求输入
    # ALWAYS: 总是请求人类输入
    max_consecutive_auto_reply=10
)
''')

print()
print("4.3 GroupChat")
print('''
# 群聊Agent
groupchat = autogen.GroupChat(
    agents=[assistant1, assistant2, user_proxy],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)
''')

print()
print("=" * 60)
print("5. 多Agent对话")
print("=" * 60)

print('''
import autogen

# 配置
config_list = [{"model": "gpt-4", "api_key": "..."}]

# 创建多个Agent
writer = autogen.AssistantAgent(
    name="writer",
    llm_config={"config_list": config_list},
    system_message="你是一个专业作家，擅长技术文章。"
)

reviewer = autogen.AssistantAgent(
    name="reviewer",
    llm_config={"config_list": config_list},
    system_message="你是一个严格的审稿人。"
)

user_proxy = autogen.UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)

# 1对1对话
user_proxy.initiate_chat(
    writer,
    message="写一篇关于AI的文章"
)

# 群聊
groupchat = autogen.GroupChat(
    agents=[writer, reviewer, user_proxy],
    messages=[],
    max_round=5
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

user_proxy.initiate_chat(
    manager,
    message="写一篇文章并审核"
)
''')

print()
print("=" * 60)
print("6. 代码执行")
print("=" * 60)

print("6.1 内置代码执行")
print('''
# UserProxyAgent自动执行代码
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"}
)

# Agent可以执行代码
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)

# 执行代码
user_proxy.initiate_chat(
    assistant,
    message="""请完成以下任务:
1. 创建一个列表 [1,2,3,4,5]
2. 计算平方和
3. 打印结果"""
)
''')

print()
print("6.2 自定义代码执行")
print('''
# 使用Docker执行
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={
        "executor": "docker",  # 使用Docker
        "image": "python:3.10",
        "work_dir": "coding"
    }
)
''')

print()
print("=" * 60)
print("7. 人类参与")
print("=" * 60)

print("7.1 请求人类输入")
print('''
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE"  # 需要时请求输入
)

# 当需要时会暂停等待人类输入
user_proxy.initiate_chat(
    assistant,
    message="继续还是停止?"
)
''')

print()
print("7.2 条件人类介入")
print('''
def should_terminate(self, messages):
    last_msg = messages[-1]
    if "完成" in last_msg["content"]:
        return True
    return False

user_proxy.register_reply(
    autogen.Agent,
    reply_func=should_terminate
)
''')

print()
print("=" * 60)
print("8. 自定义Agent")
print("=" * 60)

print("8.1 继承Agent")
print('''
class MyAgent(autogen.AssistantAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_attr = "value"

    def generate_reply(self, messages):
        # 自定义回复逻辑
        return super().generate_reply(messages)

my_agent = MyAgent(
    name="my_agent",
    llm_config={"config_list": config_list}
)
''')

print()
print("8.2 自定义转换函数")
print('''
def custom_converter(agent, messages):
    # 消息转换
    for msg in messages:
        msg["content"] = msg["content"].upper()
    return messages

assistant = autogen.AssistantAgent(
    name="assistant",
    message_converter=custom_converter
)
''')

print()
print("=" * 60)
print("9. 工作流模式")
print("=" * 60)

print("9.1 两阶段对话")
print('''
# 阶段1: 研究
researcher = autogen.AssistantAgent(
    name="researcher",
    llm_config={"config_list": config_list},
    system_message="你负责研究任务。"
)

# 阶段2: 写作
writer = autogen.AssistantAgent(
    name="writer",
    llm_config={"config_list": config_list},
    system_message="你负责写作。"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER"
)

# 执行
user_proxy.initiate_chat(researcher, message="研究AI趋势")
user_proxy.initiate_chat(writer, message="基于研究写作")
''')

print()
print("9.2 循环优化")
print('''
# 写作-审核循环
for i in range(3):
    # 写作
    user_proxy.initiate_chat(writer, message=f"第{i+1}次写作")

    # 审核
    user_proxy.initiate_chat(reviewer, message="审核以上内容")
''')

print()
print("=" * 60)
print("10. 高级功能")
print("=" * 60)

print("10.1 消息过滤")
print('''
# 过滤特定消息
def filter_messages(messages):
    return [m for m in messages if m["role"] != "system"]

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    message_filter=filter_messages
)
''')

print()
print("10.2 缓存")
print('''
# 启用响应缓存
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "cache": {
            "cache_seed": 42  # 固定种子
        }
    }
)
''')

print()
print("10.3 日志记录")
print('''
import logging

logging.basicConfig(level=logging.INFO)

# AutoGen会自动记录对话
# 可通过配置自定义日志
''')

print()
print("=" * 60)
print("11. AutoGen vs LangChain")
print("=" * 60)

print("| 特性 | AutoGen | LangChain |")
print("|------|---------|-----------|")
print("| 多Agent | 原生支持 | 需要额外配置 |")
print("| 代码执行 | 内置 | 需工具 |")
print("| 人类交互 | 简单 | 较复杂 |")
print("| 学习曲线 | 中等 | 较低 |")
print("| 灵活性 | 高 | 很高 |")

print()
print("=" * 60)
print("12. AutoGen最佳实践")
print("=" * 60)

print("1. Agent设计")
print("  - 角色清晰")
print("  - 指令简洁")
print("  - 避免冲突")
print()
print("2. 对话管理")
print("  - 设置max_round防止无限循环")
print("  - 适当使用human_input_mode")
print()
print("3. 代码执行")
print("  - 使用沙箱环境")
print("  - 限制执行时间")
print("  - 清理临时文件")
print()
print("4. 错误处理")
print("  - try-except包装")
print("  - 设置fallback")

print()
print("=" * 60)
print("13. AutoGen总结")
print("=" * 60)

print("AutoGen要点:")
print()
print("* 核心特性:")
print("  - 多Agent对话")
print("  - 代码生成执行")
print("  - 人类交互")
print("  - 灵活工作流")
print()
print("* 适用场景:")
print("  - 多Agent协作项目")
print("  - 需要代码执行的任务")
print("  - 人类参与的工作流")
print()
print("* 优势:")
print("  - 简化多Agent开发")
print("  - 内置代码执行")
print("  - 丰富的示例")
