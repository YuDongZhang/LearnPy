"""
1. MLOps概述 - 代码示例
演示用MLflow进行实验追踪的基本用法。
"""

import mlflow


# ============================================================
# 1. MLflow实验追踪
# ============================================================
def demo_mlflow_tracking():
    """记录一次训练实验"""
    mlflow.set_experiment("python-qa-finetune")

    with mlflow.start_run(run_name="lora-r8-lr2e4"):
        # 记录参数
        mlflow.log_param("model", "Qwen2.5-0.5B")
        mlflow.log_param("method", "LoRA")
        mlflow.log_param("lora_r", 8)
        mlflow.log_param("learning_rate", 2e-4)
        mlflow.log_param("epochs", 3)
        mlflow.log_param("dataset_size", 1000)

        # 模拟训练过程，记录指标
        for epoch in range(1, 4):
            train_loss = 2.5 / epoch
            eval_loss = 2.8 / epoch
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("eval_loss", eval_loss, step=epoch)
            print(f"  Epoch {epoch}: train_loss={train_loss:.3f}, eval_loss={eval_loss:.3f}")

        # 记录最终指标
        mlflow.log_metric("final_accuracy", 0.85)

        # 记录产物（模型文件等）
        with open("model_config.txt", "w") as f:
            f.write("model=Qwen2.5-0.5B\nmethod=LoRA\nr=8")
        mlflow.log_artifact("model_config.txt")

    print("\n实验已记录到MLflow")
    print("查看: mlflow ui  (然后打开 http://localhost:5000)")


# ============================================================
# 2. 对比多次实验
# ============================================================
def demo_compare_experiments():
    """记录多组实验用于对比"""
    mlflow.set_experiment("lora-comparison")

    configs = [
        {"r": 8, "lr": 2e-4, "acc": 0.82},
        {"r": 16, "lr": 2e-4, "acc": 0.86},
        {"r": 32, "lr": 1e-4, "acc": 0.88},
        {"r": 64, "lr": 1e-4, "acc": 0.87},
    ]

    for cfg in configs:
        with mlflow.start_run(run_name=f"lora-r{cfg['r']}"):
            mlflow.log_param("lora_r", cfg["r"])
            mlflow.log_param("learning_rate", cfg["lr"])
            mlflow.log_metric("accuracy", cfg["acc"])
            print(f"  r={cfg['r']}, lr={cfg['lr']} → acc={cfg['acc']}")

    print("\n对比实验已记录，用 mlflow ui 查看")


if __name__ == "__main__":
    print("=" * 60)
    print("1. MLflow实验追踪")
    print("=" * 60)
    demo_mlflow_tracking()

    print("\n" + "=" * 60)
    print("2. 对比实验")
    print("=" * 60)
    demo_compare_experiments()
