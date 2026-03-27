"""
4. 模型评估与A/B测试 - 代码示例
演示回归测试和简单A/B测试框架。
"""

import random
import time
from dataclasses import dataclass


# ============================================================
# 1. 回归测试
# ============================================================
class RegressionTest:
    """LLM回归测试套件"""

    def __init__(self, model_fn):
        self.model_fn = model_fn
        self.cases = []
        self.results = []

    def add(self, question: str, expected_keywords: list[str]):
        self.cases.append({"question": question, "keywords": expected_keywords})

    def run(self):
        self.results = []
        for case in self.cases:
            answer = self.model_fn(case["question"])
            missing = [kw for kw in case["keywords"] if kw not in answer]
            passed = len(missing) == 0
            self.results.append({"question": case["question"], "passed": passed, "missing": missing})
            status = "✓" if passed else "✗"
            print(f"  {status} {case['question'][:40]}")

        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        print(f"\n通过: {passed}/{total} ({passed/total*100:.0f}%)")
        return passed == total


# ============================================================
# 2. A/B测试框架
# ============================================================
@dataclass
class ABResult:
    model: str
    score: float
    latency: float


class ABTest:
    """简单A/B测试"""

    def __init__(self, model_a_fn, model_b_fn, name_a="A", name_b="B"):
        self.model_a = model_a_fn
        self.model_b = model_b_fn
        self.name_a = name_a
        self.name_b = name_b
        self.results_a: list[ABResult] = []
        self.results_b: list[ABResult] = []

    def run(self, questions: list[str], score_fn=None):
        """运行A/B测试"""
        if score_fn is None:
            score_fn = lambda q, a: len(a) / 100  # 默认用长度打分

        for q in questions:
            # Model A
            start = time.time()
            ans_a = self.model_a(q)
            lat_a = time.time() - start
            self.results_a.append(ABResult(self.name_a, score_fn(q, ans_a), lat_a))

            # Model B
            start = time.time()
            ans_b = self.model_b(q)
            lat_b = time.time() - start
            self.results_b.append(ABResult(self.name_b, score_fn(q, ans_b), lat_b))

    def report(self):
        avg_a = sum(r.score for r in self.results_a) / len(self.results_a)
        avg_b = sum(r.score for r in self.results_b) / len(self.results_b)
        lat_a = sum(r.latency for r in self.results_a) / len(self.results_a)
        lat_b = sum(r.latency for r in self.results_b) / len(self.results_b)

        print(f"\nA/B测试结果 ({len(self.results_a)} 个样本):")
        print(f"  {self.name_a}: 平均分={avg_a:.3f}, 平均延迟={lat_a:.3f}s")
        print(f"  {self.name_b}: 平均分={avg_b:.3f}, 平均延迟={lat_b:.3f}s")
        winner = self.name_a if avg_a > avg_b else self.name_b
        print(f"  胜出: {winner}")


# ============================================================
# 演示
# ============================================================
def demo():
    # 模拟两个模型
    def model_old(q): return f"简短回答: {q[:10]}"
    def model_new(q): return f"详细回答: {q}。这是一个很好的问题，让我详细解释..."

    # 回归测试
    print("=" * 50)
    print("回归测试")
    print("=" * 50)
    test = RegressionTest(model_new)
    test.add("什么是Python？", ["Python", "回答"])
    test.add("装饰器怎么用？", ["装饰器", "回答"])
    test.run()

    # A/B测试
    print("\n" + "=" * 50)
    print("A/B测试")
    print("=" * 50)
    ab = ABTest(model_old, model_new, "旧模型", "新模型")
    ab.run(["什么是GIL？", "解释装饰器", "Python优势"])
    ab.report()


if __name__ == "__main__":
    demo()
