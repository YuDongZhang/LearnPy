"""
5. 成本控制 - 代码示例
演示Token用量追踪、模型路由、用量限制。
"""

from dataclasses import dataclass, field
from datetime import date
from openai import OpenAI


# ============================================================
# 1. Token用量追踪器
# ============================================================
@dataclass
class UsageRecord:
    user: str
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    date: str


class UsageTracker:
    """追踪每个用户的Token用量和费用"""

    PRICING = {
        "gpt-4o": {"input": 2.5 / 1_000_000, "output": 10.0 / 1_000_000},
        "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.6 / 1_000_000},
        "qwen2.5:7b": {"input": 0, "output": 0},  # 本地模型免费
    }

    def __init__(self):
        self.records: list[UsageRecord] = []
        self.daily_limits: dict[str, int] = {}  # user -> max_tokens/day

    def record(self, user: str, model: str, input_tokens: int, output_tokens: int):
        pricing = self.PRICING.get(model, {"input": 0, "output": 0})
        cost = input_tokens * pricing["input"] + output_tokens * pricing["output"]
        self.records.append(UsageRecord(user, model, input_tokens, output_tokens, cost, str(date.today())))

    def get_daily_usage(self, user: str) -> dict:
        today = str(date.today())
        user_records = [r for r in self.records if r.user == user and r.date == today]
        return {
            "total_tokens": sum(r.input_tokens + r.output_tokens for r in user_records),
            "total_cost": sum(r.cost for r in user_records),
            "requests": len(user_records),
        }

    def check_limit(self, user: str) -> bool:
        limit = self.daily_limits.get(user, 100_000)
        usage = self.get_daily_usage(user)
        return usage["total_tokens"] < limit


# ============================================================
# 2. 模型路由（按复杂度选模型）
# ============================================================
class ModelRouter:
    """根据任务复杂度自动选择模型"""

    def route(self, message: str) -> str:
        # 简单规则：短问题用小模型，长问题/复杂问题用大模型
        if len(message) < 50 and "?" in message or "？" in message:
            return "gpt-4o-mini"  # 简单问答
        elif any(kw in message for kw in ["代码", "编程", "算法", "code"]):
            return "gpt-4o"  # 编程任务
        else:
            return "gpt-4o-mini"  # 默认小模型


# ============================================================
# 演示
# ============================================================
def demo():
    tracker = UsageTracker()
    router = ModelRouter()

    # 模拟几次调用
    queries = [
        ("user1", "什么是GIL？"),
        ("user1", "写一个复杂的Python装饰器，支持参数、缓存和日志功能"),
        ("user2", "Python怎么读文件？"),
    ]

    for user, query in queries:
        model = router.route(query)
        # 模拟Token数
        input_tokens = len(query) * 2
        output_tokens = 200
        tracker.record(user, model, input_tokens, output_tokens)
        print(f"  [{user}] {query[:30]}... → {model}")

    # 查看用量
    for user in ["user1", "user2"]:
        usage = tracker.get_daily_usage(user)
        print(f"\n{user} 今日用量: {usage}")


if __name__ == "__main__":
    demo()
