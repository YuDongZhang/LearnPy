"""
4. AutoGen框架 - 代码示例
演示AutoGen的1对1对话和群聊模式。
"""

import autogen

# ============================================================
# LLM配置（替换为你的API Key）
# ============================================================
config_list = [
    {
        "model": "gpt-4o",
        "api_key": "your-api-key-here",  # 替换为真实Key
    }
]

llm_config = {"config_list": config_list}


# ============================================================
# 示例1: 1对1对话（助手 + 用户代理）
# ============================================================
def demo_basic_chat():
    """最基础的AutoGen用法：助手回答问题"""
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="你是一个Python专家，用简洁的中文回答问题。"
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        code_execution_config=False,  # 不执行代码
    )

    user_proxy.initiate_chat(
        assistant,
        message="Python的GIL是什么？对多线程有什么影响？"
    )


# ============================================================
# 示例2: 代码生成+执行
# ============================================================
def demo_code_execution():
    """助手生成代码，用户代理自动执行"""
    assistant = autogen.AssistantAgent(
        name="coder",
        llm_config=llm_config,
        system_message="你是一个Python程序员，用代码解决问题。"
    )

    user_proxy = autogen.UserProxyAgent(
        name="executor",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
        code_execution_config={"work_dir": "coding_output"},
    )

    user_proxy.initiate_chat(
        assistant,
        message="用Python生成斐波那契数列前20项并打印"
    )


# ============================================================
# 示例3: 群聊（研究员 + 写手 + 审核员）
# ============================================================
def demo_group_chat():
    """多Agent群聊协作"""
    researcher = autogen.AssistantAgent(
        name="researcher",
        llm_config=llm_config,
        system_message="你是研究员，负责提供事实和数据。回答要简洁。"
    )

    writer = autogen.AssistantAgent(
        name="writer",
        llm_config=llm_config,
        system_message="你是写手，负责把研究内容写成通俗易懂的文章。"
    )

    reviewer = autogen.AssistantAgent(
        name="reviewer",
        llm_config=llm_config,
        system_message="你是审核员，负责检查内容质量，指出问题。"
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, researcher, writer, reviewer],
        messages=[],
        max_round=6,
    )

    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
    )

    user_proxy.initiate_chat(
        manager,
        message="请协作完成一篇关于'LLM Agent发展趋势'的短文（200字左右）"
    )


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("示例1: 1对1对话")
    print("=" * 60)
    demo_basic_chat()

    # print("\n" + "=" * 60)
    # print("示例2: 代码生成+执行")
    # print("=" * 60)
    # demo_code_execution()

    # print("\n" + "=" * 60)
    # print("示例3: 群聊协作")
    # print("=" * 60)
    # demo_group_chat()
