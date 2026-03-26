"""
5. Agent评估与测试 - 代码示例
演示Agent的自动化测试框架和效率评估。
"""

import time
from dataclasses import dataclass, field
from typing import Any


# ============================================================
# 1. 测试用例和测试套件
# ============================================================
@dataclass
class TestCase:
    """单个测试用例"""
    name: str
    input_text: str
    expected_keywords: list[str]  # 期望输出中包含的关键词
    max_time: float = 10.0       # 最大允许耗时(秒)


@dataclass
class TestResult:
    """测试结果"""
    name: str
    passed: bool
    output: str
    time_cost: float
    details: str = ""


class AgentTestSuite:
    """Agent测试套件"""

    def __init__(self, agent_fn):
        """
        agent_fn: 接收字符串输入、返回字符串输出的函数
                  例如 lambda q: agent.run(q)
        """
        self.agent_fn = agent_fn
        self.test_cases: list[TestCase] = []
        self.results: list[TestResult] = []

    def add(self, name: str, input_text: str, expected_keywords: list[str], max_time=10.0):
        self.test_cases.append(TestCase(name, input_text, expected_keywords, max_time))

    def run(self) -> list[TestResult]:
        self.results = []
        for tc in self.test_cases:
            result = self._run_one(tc)
            self.results.append(result)
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"  {status} | {tc.name} ({result.time_cost:.2f}s) {result.details}")
        return self.results

    def _run_one(self, tc: TestCase) -> TestResult:
        start = time.time()
        try:
            output = self.agent_fn(tc.input_text)
            elapsed = time.time() - start

            # 检查关键词
            missing = [kw for kw in tc.expected_keywords if kw.lower() not in output.lower()]
            keyword_ok = len(missing) == 0

            # 检查耗时
            time_ok = elapsed <= tc.max_time

            passed = keyword_ok and time_ok
            details = ""
            if missing:
                details += f"缺少关键词: {missing} "
            if not time_ok:
                details += f"超时({elapsed:.1f}s > {tc.max_time}s)"

            return TestResult(tc.name, passed, output, elapsed, details)

        except Exception as e:
            elapsed = time.time() - start
            return TestResult(tc.name, False, "", elapsed, f"异常: {e}")

    def report(self) -> dict:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{passed/total*100:.1f}%" if total else "N/A",
            "avg_time": f"{sum(r.time_cost for r in self.results)/total:.2f}s" if total else "N/A",
        }


# ============================================================
# 2. 效率追踪器
# ============================================================
class EfficiencyTracker:
    """追踪Agent执行效率"""

    def __init__(self):
        self.records = []

    def track(self, name: str, fn, *args, **kwargs):
        """执行函数并记录耗时"""
        start = time.time()
        result = fn(*args, **kwargs)
        elapsed = time.time() - start
        self.records.append({"name": name, "time": elapsed})
        return result

    def summary(self):
        if not self.records:
            return "无记录"
        total = sum(r["time"] for r in self.records)
        print(f"总耗时: {total:.2f}s | 共{len(self.records)}次调用")
        for r in self.records:
            print(f"  {r['name']}: {r['time']:.2f}s")


# ============================================================
# 演示
# ============================================================
def demo():
    # 模拟一个Agent函数
    def mock_agent(query: str) -> str:
        time.sleep(0.1)  # 模拟延迟
        if "排序" in query:
            return "快速排序是一种分治算法，平均时间复杂度O(nlogn)"
        elif "天气" in query:
            return "北京今天晴，25度"
        return f"关于'{query}'的回答..."

    # 创建测试套件
    suite = AgentTestSuite(mock_agent)
    suite.add("排序问题", "什么是快速排序？", ["快速排序", "算法"])
    suite.add("天气查询", "北京天气怎么样？", ["北京", "晴"])
    suite.add("未知问题", "量子计算是什么？", ["量子"])  # 会失败

    print("运行测试:")
    suite.run()
    print(f"\n测试报告: {suite.report()}")

    # 效率追踪
    print("\n效率追踪:")
    tracker = EfficiencyTracker()
    tracker.track("查询1", mock_agent, "快速排序")
    tracker.track("查询2", mock_agent, "北京天气")
    tracker.summary()


if __name__ == "__main__":
    demo()
