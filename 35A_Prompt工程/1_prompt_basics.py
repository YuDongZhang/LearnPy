"""
1. Prompt基础 - 代码示例
演示Prompt的基本组成要素和不同写法的效果差异。
"""

from openai import OpenAI

client = OpenAI()  # 需要设置OPENAI_API_KEY环境变量
MODEL = "gpt-4o"


def chat(messages, temperature=0):
    """调用LLM"""
    response = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=temperature
    )
    return response.choices[0].message.content


# ============================================================
# 1. 差Prompt vs 好Prompt
# ============================================================
def demo_prompt_quality():
    """对比不同质量的Prompt"""
    print("--- 差的Prompt ---")
    result1 = chat([{"role": "user", "content": "写代码"}])
    print(result1[:200])

    print("\n--- 好的Prompt ---")
    result2 = chat([{"role": "user", "content":
        "用Python写一个快速排序函数，要求：\n"
        "1. 包含类型注解\n"
        "2. 添加docstring说明\n"
        "3. 处理空列表边界情况\n"
        "4. 只输出代码，不要解释"
    }])
    print(result2[:300])


# ============================================================
# 2. System Prompt的作用
# ============================================================
def demo_system_prompt():
    """演示System Prompt如何影响输出风格"""
    question = "什么是Python的GIL？"

    # 无System Prompt
    r1 = chat([{"role": "user", "content": question}])
    print(f"无角色设定:\n{r1[:150]}...\n")

    # 有System Prompt
    r2 = chat([
        {"role": "system", "content": "你是一个Python专家，用一句话简洁回答，不超过50字。"},
        {"role": "user", "content": question}
    ])
    print(f"有角色设定:\n{r2}")


# ============================================================
# 3. Temperature对比
# ============================================================
def demo_temperature():
    """对比不同temperature的输出"""
    prompt = [{"role": "user", "content": "用一句话描述Python"}]

    print("temperature=0（确定性）:")
    for i in range(3):
        print(f"  第{i+1}次: {chat(prompt, temperature=0)}")

    print("\ntemperature=1.0（高随机性）:")
    for i in range(3):
        print(f"  第{i+1}次: {chat(prompt, temperature=1.0)}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. Prompt质量对比")
    print("=" * 60)
    demo_prompt_quality()

    print("\n" + "=" * 60)
    print("2. System Prompt")
    print("=" * 60)
    demo_system_prompt()

    print("\n" + "=" * 60)
    print("3. Temperature对比")
    print("=" * 60)
    demo_temperature()
