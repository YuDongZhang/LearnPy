"""
5. Prompt工程实战 - 智能代码审查助手
综合运用：角色设定 + Few-shot + JSON输出 + Pydantic校验
"""

import json
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
MODEL = "gpt-4o"


# ============================================================
# 1. 定义输出结构
# ============================================================
class Issue(BaseModel):
    severity: str       # high / medium / low
    category: str       # security / performance / readability / best_practice
    line: str           # 相关代码行
    description: str    # 问题描述
    suggestion: str     # 改进建议


class ReviewResult(BaseModel):
    overall_score: int  # 1-10
    issues: list[Issue]
    summary: str


# ============================================================
# 2. 代码审查Prompt
# ============================================================
SYSTEM_PROMPT = """你是一个资深Python代码审查专家，有15年经验。

审查维度：
1. 安全性（SQL注入、敏感信息泄露等）
2. 性能（算法效率、资源使用）
3. 可读性（命名、注释、结构）
4. 最佳实践（Python惯用写法、PEP8）

输出要求：严格按JSON格式输出，包含以下字段：
{
  "overall_score": 1-10的评分,
  "issues": [{"severity":"high/medium/low", "category":"分类", "line":"相关代码", "description":"问题", "suggestion":"建议"}],
  "summary": "一句话总结"
}"""


# ============================================================
# 3. 审查函数
# ============================================================
def review_code(code: str) -> ReviewResult:
    """审查Python代码，返回结构化结果"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请审查以下代码：\n```python\n{code}\n```"}
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    raw = json.loads(response.choices[0].message.content)
    return ReviewResult(**raw)


# ============================================================
# 4. 测试
# ============================================================
def demo():
    test_code = '''
import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE name = '{username}'"
    result = conn.execute(query).fetchone()
    conn.close()
    return result

def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result

PASSWORD = "admin123"
'''

    print("提交代码审查...\n")
    result = review_code(test_code)

    print(f"总评分: {result.overall_score}/10")
    print(f"总结: {result.summary}\n")
    print(f"发现 {len(result.issues)} 个问题:")
    for i, issue in enumerate(result.issues, 1):
        print(f"\n  [{issue.severity.upper()}] {issue.category}")
        print(f"  代码: {issue.line}")
        print(f"  问题: {issue.description}")
        print(f"  建议: {issue.suggestion}")


if __name__ == "__main__":
    demo()
