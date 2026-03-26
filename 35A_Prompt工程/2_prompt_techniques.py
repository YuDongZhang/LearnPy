"""
2. 核心提示词技巧 - 代码示例
演示Zero-shot、Few-shot、Chain-of-Thought等技巧。
"""

from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


def chat(messages, temperature=0):
    response = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=temperature
    )
    return response.choices[0].message.content


# ============================================================
# 1. Zero-shot vs Few-shot
# ============================================================
def demo_zero_vs_few_shot():
    """对比零样本和少样本"""
    # Zero-shot
    r1 = chat([{"role": "user", "content":
        "判断以下评论的情感（正面/负面）：\n这个手机电池太差了，半天就没电"}])
    print(f"Zero-shot: {r1}")

    # Few-shot
    r2 = chat([{"role": "user", "content":
        "判断评论情感：\n"
        "评论：质量很好 → 正面\n"
        "评论：发货太慢 → 负面\n"
        "评论：性价比不错 → 正面\n"
        "评论：这个手机电池太差了，半天就没电 →"}])
    print(f"Few-shot: {r2}")


# ============================================================
# 2. Chain-of-Thought（思维链）
# ============================================================
def demo_cot():
    """对比直接回答和思维链推理"""
    problem = "一个水池有两个水管，A管每小时注水3吨，B管每小时排水1吨。水池容量20吨，从空池开始，多久能注满？"

    # 直接回答
    r1 = chat([{"role": "user", "content": problem}])
    print(f"直接回答:\n{r1}\n")

    # CoT
    r2 = chat([{"role": "user", "content": f"{problem}\n\n请一步步思考："}])
    print(f"思维链:\n{r2}")


# ============================================================
# 3. 角色扮演
# ============================================================
def demo_role_play():
    """不同角色产生不同风格的回答"""
    question = "如何提高Python代码性能？"

    roles = [
        ("初级开发者", "你是一个刚学Python半年的初级开发者"),
        ("资深架构师", "你是一个有15年经验的Python架构师，曾优化过日活千万的系统"),
    ]
    for name, role in roles:
        r = chat([
            {"role": "system", "content": f"{role}。用你的经验水平回答。"},
            {"role": "user", "content": question}
        ])
        print(f"[{name}]:\n{r[:200]}...\n")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. Zero-shot vs Few-shot")
    print("=" * 60)
    demo_zero_vs_few_shot()

    print("\n" + "=" * 60)
    print("2. Chain-of-Thought")
    print("=" * 60)
    demo_cot()

    print("\n" + "=" * 60)
    print("3. 角色扮演")
    print("=" * 60)
    demo_role_play()
