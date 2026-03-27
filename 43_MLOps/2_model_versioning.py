"""
2. 模型版本管理 - 代码示例
演示MLflow Model Registry的使用。
"""

import mlflow
from mlflow.tracking import MlflowClient


# ============================================================
# 1. 注册模型
# ============================================================
def demo_register_model():
    """训练并注册模型到Model Registry"""
    mlflow.set_experiment("model-registry-demo")

    with mlflow.start_run(run_name="v1-baseline"):
        mlflow.log_param("model", "Qwen2.5-0.5B")
        mlflow.log_param("method", "LoRA-r8")
        mlflow.log_metric("accuracy", 0.82)

        # 记录模型（这里用文本文件模拟）
        with open("model_info.txt", "w") as f:
            f.write("Qwen2.5-0.5B + LoRA r=8")
        mlflow.log_artifact("model_info.txt")

        # 注册模型
        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/model_info.txt"
        # mlflow.register_model(model_uri, "python-qa-model")
        print(f"模型已记录, run_id={run_id}")


# ============================================================
# 2. 模型版本管理
# ============================================================
def demo_model_lifecycle():
    """演示模型状态流转"""
    client = MlflowClient()

    print("模型版本状态流转:")
    print("  None → Staging（测试中）")
    print("  Staging → Production（上线）")
    print("  Production → Archived（归档）")
    print()
    print("操作命令:")
    print('  client.transition_model_version_stage("model-name", version=1, stage="Staging")')
    print('  client.transition_model_version_stage("model-name", version=1, stage="Production")')


# ============================================================
# 3. 简单的本地版本管理
# ============================================================
import json
import os
from datetime import datetime


class SimpleModelRegistry:
    """不依赖MLflow的简单模型版本管理"""

    def __init__(self, registry_dir: str = "./model_registry"):
        self.registry_dir = registry_dir
        self.registry_file = os.path.join(registry_dir, "registry.json")
        os.makedirs(registry_dir, exist_ok=True)
        self.registry = self._load()

    def _load(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file) as f:
                return json.load(f)
        return {"models": {}}

    def _save(self):
        with open(self.registry_file, "w") as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)

    def register(self, name: str, version: str, path: str, metrics: dict):
        if name not in self.registry["models"]:
            self.registry["models"][name] = []
        self.registry["models"][name].append({
            "version": version, "path": path, "metrics": metrics,
            "stage": "staging", "registered_at": datetime.now().isoformat()
        })
        self._save()
        print(f"注册: {name} v{version} (staging)")

    def promote(self, name: str, version: str):
        for m in self.registry["models"].get(name, []):
            if m["version"] == version:
                m["stage"] = "production"
        self._save()
        print(f"升级: {name} v{version} → production")

    def list_models(self):
        for name, versions in self.registry["models"].items():
            print(f"\n{name}:")
            for v in versions:
                print(f"  v{v['version']} [{v['stage']}] acc={v['metrics'].get('accuracy', 'N/A')}")


def demo_simple_registry():
    reg = SimpleModelRegistry()
    reg.register("python-qa", "1.0", "./models/v1", {"accuracy": 0.82})
    reg.register("python-qa", "1.1", "./models/v1.1", {"accuracy": 0.86})
    reg.promote("python-qa", "1.1")
    reg.list_models()


if __name__ == "__main__":
    print("=" * 60)
    print("1. MLflow注册模型")
    print("=" * 60)
    demo_register_model()

    print("\n" + "=" * 60)
    print("2. 简单版本管理")
    print("=" * 60)
    demo_simple_registry()
