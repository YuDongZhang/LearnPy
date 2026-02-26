"""
Agent评估与测试
==========

介绍如何评估和测试Agent系统的性能。
"""

print("=" * 60)
print("1. Agent评估概述")
print("=" * 60)

print("为什么需要评估Agent?")
print("  - Agent行为难以预测")
print("  - 需要量化性能指标")
print("  - 便于优化和改进")
print("  - 生产环境可靠性")
print()
print("评估挑战:")
print("  - 任务多样性")
print("  - 结果主观性")
print("  - 长流程复杂性")
print("  - 工具调用准确性")

print()
print("=" * 60)
print("2. 评估维度")
print("=" * 60)

print("| 维度 | 说明 | 指标 |")
print("|------|------|------|")
print("| 任务完成度 | 是否完成目标 | 成功率、完成率 |")
print("| 准确性 | 结果是否正确 | 准确率、F1分数 |")
print("| 效率 | 资源使用情况 | 调用次数、耗时 |")
print("| 稳定性 | 结果一致性 | 方差、成功率 |")
print("| 安全性 | 是否有害输出 | 安全评分 |")

print()
print("=" * 60)
print("3. 任务完成度评估")
print("=" * 60)

print('''
# 任务完成度评估
class TaskCompletionEvaluator:
    def __init__(self):
        self.results = []

    def evaluate(self, task, expected_output, actual_output):
        # 1. 精确匹配
        exact_match = expected_output == actual_output

        # 2. 语义相似度
        semantic_score = self.semantic_similarity(expected_output, actual_output)

        # 3. 包含关键信息
        contains_key_info = self.check_key_info(expected_output, actual_output)

        result = {
            "task": task,
            "exact_match": exact_match,
            "semantic_score": semantic_score,
            "contains_key_info": contains_key_info,
            "overall": (exact_match + semantic_score + contains_key_info) / 3
        }

        self.results.append(result)
        return result

    def semantic_similarity(self, text1, text2):
        # 使用嵌入模型计算语义相似度
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()

        emb1 = embeddings.embed_query(text1)
        emb2 = embeddings.embed_query(text2)

        # 余弦相似度
        import numpy as np
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return similarity

    def check_key_info(self, expected, actual):
        # 检查是否包含关键信息
        key_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())
        overlap = len(key_words & actual_words) / len(key_words)
        return overlap

    def get_report(self):
        if not self.results:
            return "无评估数据"

        avg_score = sum(r["overall"] for r in self.results) / len(self.results)
        return {
            "total_tasks": len(self.results),
            "average_score": avg_score,
            "exact_match_rate": sum(r["exact_match"] for r in self.results) / len(self.results)
        }
''')

print()
print("=" * 60)
print("4. 工具调用评估")
print("=" * 60)

print('''
# 工具调用评估
class ToolUsageEvaluator:
    def __init__(self):
        self.tool_calls = []

    def record_tool_call(self, tool_name, input_params, output, expected_output=None):
        self.tool_calls.append({
            "tool": tool_name,
            "input": input_params,
            "output": output,
            "expected": expected_output,
            "timestamp": datetime.now()
        })

    def evaluate_tool_selection(self, task, selected_tools, optimal_tools):
        # 评估工具选择是否正确
        correct_selection = set(selected_tools) == set(optimal_tools)
        precision = len(set(selected_tools) & set(optimal_tools)) / len(selected_tools) if selected_tools else 0
        recall = len(set(selected_tools) & set(optimal_tools)) / len(optimal_tools) if optimal_tools else 0

        return {
            "correct_selection": correct_selection,
            "precision": precision,
            "recall": recall,
            "f1_score": 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        }

    def evaluate_tool_efficiency(self):
        # 评估工具使用效率
        total_calls = len(self.tool_calls)
        unique_tools = len(set(call["tool"] for call in self.tool_calls))

        return {
            "total_calls": total_calls,
            "unique_tools": unique_tools,
            "redundancy_rate": 1 - unique_tools / total_calls if total_calls > 0 else 0
        }

    def get_tool_statistics(self):
        from collections import Counter
        tool_counts = Counter(call["tool"] for call in self.tool_calls)
        return dict(tool_counts)
''')

print()
print("=" * 60)
print("5. 效率评估")
print("=" * 60)

print('''
import time
from dataclasses import dataclass
from typing import List

@dataclass
class EfficiencyMetrics:
    total_time: float
    llm_calls: int
    tool_calls: int
    tokens_used: int
    cost_estimate: float

class EfficiencyEvaluator:
    def __init__(self):
        self.metrics = []

    def start_session(self):
        self.session_start = time.time()
        self.session_metrics = {
            "llm_calls": 0,
            "tool_calls": 0,
            "tokens_used": 0
        }

    def end_session(self):
        total_time = time.time() - self.session_start

        metrics = EfficiencyMetrics(
            total_time=total_time,
            llm_calls=self.session_metrics["llm_calls"],
            tool_calls=self.session_metrics["tool_calls"],
            tokens_used=self.session_metrics["tokens_used"],
            cost_estimate=self.estimate_cost()
        )

        self.metrics.append(metrics)
        return metrics

    def estimate_cost(self):
        # 估算成本 (基于OpenAI定价)
        token_cost = self.session_metrics["tokens_used"] * 0.002 / 1000  # GPT-4 pricing
        return token_cost

    def get_average_metrics(self):
        if not self.metrics:
            return None

        return {
            "avg_time": sum(m.total_time for m in self.metrics) / len(self.metrics),
            "avg_llm_calls": sum(m.llm_calls for m in self.metrics) / len(self.metrics),
            "avg_tool_calls": sum(m.tool_calls for m in self.metrics) / len(self.metrics),
            "avg_cost": sum(m.cost_estimate for m in self.metrics) / len(self.metrics)
        }
''')

print()
print("=" * 60)
print("6. 人工评估")
print("=" * 60)

print('''
# 人工评估框架
class HumanEvaluation:
    def __init__(self):
        self.evaluations = []

    def collect_human_feedback(self, task, agent_output, criteria=None):
        """收集人工反馈"""
        if criteria is None:
            criteria = {
                "准确性": "结果是否正确? (1-5)",
                "完整性": "是否包含所有必要信息? (1-5)",
                "清晰度": "表达是否清晰易懂? (1-5)",
                "有用性": "对用户是否有帮助? (1-5)"
            }

        print(f"\\n任务: {task}")
        print(f"Agent输出: {agent_output}")
        print("\\n请评分:")

        scores = {}
        for criterion, description in criteria.items():
            while True:
                try:
                    score = int(input(f"{criterion} {description}: "))
                    if 1 <= score <= 5:
                        scores[criterion] = score
                        break
                    else:
                        print("请输入1-5之间的数字")
                except ValueError:
                    print("请输入有效数字")

        feedback = input("其他反馈 (可选): ")

        evaluation = {
            "task": task,
            "output": agent_output,
            "scores": scores,
            "average_score": sum(scores.values()) / len(scores),
            "feedback": feedback,
            "timestamp": datetime.now()
        }

        self.evaluations.append(evaluation)
        return evaluation

    def get_summary(self):
        if not self.evaluations:
            return "无评估数据"

        avg_scores = {}
        for criterion in self.evaluations[0]["scores"].keys():
            avg_scores[criterion] = sum(
                e["scores"][criterion] for e in self.evaluations
            ) / len(self.evaluations)

        return {
            "total_evaluations": len(self.evaluations),
            "average_scores": avg_scores,
            "overall_average": sum(avg_scores.values()) / len(avg_scores)
        }
''')

print()
print("=" * 60)
print("7. 自动化测试")
print("=" * 60)

print('''
import unittest
from typing import Dict, Any

class AgentTestCase:
    """Agent测试用例"""
    def __init__(self, name: str, input_data: Dict, expected_output: Any, 
                 expected_tools: list = None):
        self.name = name
        self.input_data = input_data
        self.expected_output = expected_output
        self.expected_tools = expected_tools or []
        self.actual_output = None
        self.actual_tools = []
        self.passed = False

class AgentTestSuite:
    """Agent测试套件"""
    def __init__(self, agent):
        self.agent = agent
        self.test_cases = []
        self.results = []

    def add_test_case(self, test_case: AgentTestCase):
        self.test_cases.append(test_case)

    def run_tests(self):
        for test in self.test_cases:
            print(f"\\n运行测试: {test.name}")
            try:
                # 运行Agent
                result = self.agent.invoke(test.input_data)
                test.actual_output = result

                # 检查输出
                output_match = self._check_output(result, test.expected_output)

                # 检查工具调用
                tools_match = self._check_tools(test.actual_tools, test.expected_tools)

                test.passed = output_match and tools_match

                self.results.append({
                    "name": test.name,
                    "passed": test.passed,
                    "output_match": output_match,
                    "tools_match": tools_match
                })

                print(f"结果: {'通过' if test.passed else '失败'}")

            except Exception as e:
                print(f"错误: {e}")
                self.results.append({
                    "name": test.name,
                    "passed": False,
                    "error": str(e)
                })

        return self.get_report()

    def _check_output(self, actual, expected):
        # 简化的输出检查
        if isinstance(expected, str):
            return expected.lower() in str(actual).lower()
        return actual == expected

    def _check_tools(self, actual_tools, expected_tools):
        return set(actual_tools) == set(expected_tools)

    def get_report(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])

        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "details": self.results
        }

# 使用示例
def create_test_suite():
    suite = AgentTestSuite(agent)

    # 添加测试用例
    suite.add_test_case(AgentTestCase(
        name="简单查询",
        input_data={"query": "Python是什么?"},
        expected_output="编程语言",
        expected_tools=["search"]
    ))

    suite.add_test_case(AgentTestCase(
        name="数学计算",
        input_data={"query": "2+2=?"},
        expected_output="4",
        expected_tools=["calculator"]
    ))

    return suite
''')

print()
print("=" * 60)
print("8. A/B测试")
print("=" * 60)

print('''
class ABTest:
    """Agent A/B测试"""
    def __init__(self, agent_a, agent_b):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.results_a = []
        self.results_b = []

    def run_test(self, test_cases, metrics_fn):
        """运行A/B测试"""
        for i, test_case in enumerate(test_cases):
            print(f"测试用例 {i+1}/{len(test_cases)}")

            # Agent A
            result_a = self.agent_a.invoke(test_case)
            score_a = metrics_fn(result_a, test_case)
            self.results_a.append(score_a)

            # Agent B
            result_b = self.agent_b.invoke(test_case)
            score_b = metrics_fn(result_b, test_case)
            self.results_b.append(score_b)

        return self._analyze_results()

    def _analyze_results(self):
        import numpy as np

        mean_a = np.mean(self.results_a)
        mean_b = np.mean(self.results_b)

        # 统计显著性检验
        from scipy import stats
        t_stat, p_value = stats.ttest_ind(self.results_a, self.results_b)

        return {
            "agent_a_mean": mean_a,
            "agent_b_mean": mean_b,
            "difference": mean_b - mean_a,
            "improvement": (mean_b - mean_a) / mean_a * 100 if mean_a > 0 else 0,
            "p_value": p_value,
            "significant": p_value < 0.05
        }
''')

print()
print("=" * 60)
print("9. 持续评估")
print("=" * 60)

print('''
class ContinuousEvaluation:
    """持续评估系统"""
    def __init__(self, agent, evaluation_interval=100):
        self.agent = agent
        self.interval = evaluation_interval
        self.call_count = 0
        self.evaluation_history = []

    def record_interaction(self, input_data, output, feedback=None):
        self.call_count += 1

        # 定期评估
        if self.call_count % self.interval == 0:
            self._run_evaluation()

        # 记录反馈
        if feedback:
            self._record_feedback(input_data, output, feedback)

    def _run_evaluation(self):
        """运行定期评估"""
        # 使用测试集评估
        test_results = self._evaluate_on_test_set()

        self.evaluation_history.append({
            "timestamp": datetime.now(),
            "call_count": self.call_count,
            "results": test_results
        })

        # 检查性能下降
        if len(self.evaluation_history) >= 2:
            self._check_performance_degradation()

    def _check_performance_degradation(self):
        """检查性能是否下降"""
        recent = self.evaluation_history[-1]["results"]["average_score"]
        previous = self.evaluation_history[-2]["results"]["average_score"]

        if recent < previous * 0.9:  # 下降超过10%
            print(f"警告: 性能下降 {((previous - recent) / previous * 100):.1f}%")
            # 触发告警或重新训练

    def get_trend(self):
        """获取性能趋势"""
        if len(self.evaluation_history) < 2:
            return "数据不足"

        scores = [e["results"]["average_score"] for e in self.evaluation_history]

        import numpy as np
        slope = np.polyfit(range(len(scores)), scores, 1)[0]

        if slope > 0.01:
            return "上升"
        elif slope < -0.01:
            return "下降"
        else:
            return "稳定"
''')

print()
print("=" * 60)
print("10. 评估报告生成")
print("=" * 60)

print('''
class EvaluationReport:
    """生成评估报告"""
    def __init__(self):
        self.sections = []

    def add_section(self, title, content):
        self.sections.append({"title": title, "content": content})

    def generate_markdown(self):
        lines = ["# Agent评估报告", ""]

        for section in self.sections:
            lines.append(f"## {section['title']}")
            lines.append("")

            if isinstance(section["content"], dict):
                for key, value in section["content"].items():
                    lines.append(f"- **{key}**: {value}")
            else:
                lines.append(str(section["content"]))

            lines.append("")

        return "\\n".join(lines)

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.generate_markdown())

# 使用示例
def generate_sample_report():
    report = EvaluationReport()

    report.add_section("概览", {
        "测试时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "测试用例数": 100,
        "通过率": "85%"
    })

    report.add_section("性能指标", {
        "平均响应时间": "2.3s",
        "平均LLM调用": 3.5,
        "平均工具调用": 2.1,
        "平均成本": "$0.05"
    })

    report.add_section("改进建议", [
        "1. 优化工具选择逻辑",
        "2. 减少不必要的LLM调用",
        "3. 增强错误处理能力"
    ])

    return report.generate_markdown()
''')

print()
print("=" * 60)
print("11. 评估最佳实践")
print("=" * 60)

print("1. 测试数据设计")
print("  - 覆盖不同场景")
print("  - 包含边界情况")
print("  - 定期更新测试集")
print()
print("2. 评估指标选择")
print("  - 根据任务选择指标")
print("  - 不要过度优化单一指标")
print("  - 结合人工评估")
print()
print("3. 持续监控")
print("  - 生产环境监控")
print("  - 定期回归测试")
print("  - 及时发现问题")
print()
print("4. 对比实验")
print("  - A/B测试验证改进")
print("  - 控制变量")
print("  - 统计显著性")

print()
print("=" * 60)
print("12. 评估总结")
print("=" * 60)

print("Agent评估要点:")
print()
print("* 评估维度:")
print("  - 任务完成度、准确性、效率、稳定性、安全性")
print()
print("* 评估方法:")
print("  - 自动评估、人工评估、A/B测试")
print()
print("* 关键工具:")
print("  - 测试套件、评估框架、报告生成")
print()
print("* 最佳实践:")
print("  - 持续监控、定期评估、及时改进")
