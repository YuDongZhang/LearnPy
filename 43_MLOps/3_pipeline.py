"""
3. 自动化流水线 - 代码示例
演示一个简单的ML流水线：数据准备→训练→评估→注册。
"""

import json
import time
from dataclasses import dataclass


@dataclass
class PipelineResult:
    step: str
    status: str
    duration: float
    output: dict


class MLPipeline:
    """简单的ML流水线"""

    def __init__(self):
        self.results: list[PipelineResult] = []

    def run_step(self, name: str, func, **kwargs) -> dict:
        print(f"\n[{name}] 开始...")
        start = time.time()
        try:
            output = func(**kwargs)
            duration = time.time() - start
            self.results.append(PipelineResult(name, "success", duration, output))
            print(f"[{name}] 完成 ({duration:.2f}s)")
            return output
        except Exception as e:
            duration = time.time() - start
            self.results.append(PipelineResult(name, "failed", duration, {"error": str(e)}))
            print(f"[{name}] 失败: {e}")
            raise

    def report(self):
        print(f"\n{'='*50}")
        print("流水线报告")
        print(f"{'='*50}")
        total = sum(r.duration for r in self.results)
        for r in self.results:
            status = "✓" if r.status == "success" else "✗"
            print(f"  {status} {r.step:20s} {r.duration:.2f}s")
        print(f"  总耗时: {total:.2f}s")


# ============================================================
# 流水线步骤
# ============================================================
def step_prepare_data():
    """数据准备"""
    data = [{"q": f"问题{i}", "a": f"回答{i}"} for i in range(100)]
    train = data[:80]
    test = data[80:]
    return {"train_size": len(train), "test_size": len(test)}


def step_train(train_size: int = 0):
    """模型训练（模拟）"""
    time.sleep(0.5)  # 模拟训练
    return {"model_path": "./output/model", "epochs": 3, "final_loss": 0.42}


def step_evaluate(model_path: str = ""):
    """模型评估（模拟）"""
    time.sleep(0.2)
    accuracy = 0.86
    return {"accuracy": accuracy, "passed": accuracy > 0.8}


def step_register(accuracy: float = 0, passed: bool = False):
    """模型注册"""
    if not passed:
        raise ValueError(f"评估未通过 (accuracy={accuracy})")
    return {"registered": True, "version": "1.0", "stage": "staging"}


# ============================================================
# 运行流水线
# ============================================================
def run_pipeline():
    pipeline = MLPipeline()

    # Step 1: 数据准备
    data_result = pipeline.run_step("数据准备", step_prepare_data)

    # Step 2: 训练
    train_result = pipeline.run_step("模型训练", step_train, train_size=data_result["train_size"])

    # Step 3: 评估
    eval_result = pipeline.run_step("模型评估", step_evaluate, model_path=train_result["model_path"])

    # Step 4: 注册（评估通过才注册）
    pipeline.run_step("模型注册", step_register, **eval_result)

    pipeline.report()


if __name__ == "__main__":
    run_pipeline()
