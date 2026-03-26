"""
6. 训练技巧 - 代码示例
演示学习率调度、梯度检查点、早停等训练技巧。
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    EarlyStoppingCallback,
)
from peft import LoraConfig, get_peft_model, TaskType


MODEL_NAME = "Qwen/Qwen2.5-0.5B"


# ============================================================
# 1. 不同学习率调度策略对比
# ============================================================
def demo_lr_schedules():
    """展示不同学习率调度策略的配置"""
    schedules = {
        "cosine": TrainingArguments(
            output_dir="./tmp", lr_scheduler_type="cosine",
            learning_rate=2e-4, warmup_ratio=0.1, num_train_epochs=3,
        ),
        "linear": TrainingArguments(
            output_dir="./tmp", lr_scheduler_type="linear",
            learning_rate=2e-4, warmup_ratio=0.1, num_train_epochs=3,
        ),
        "constant_with_warmup": TrainingArguments(
            output_dir="./tmp", lr_scheduler_type="constant_with_warmup",
            learning_rate=2e-4, warmup_ratio=0.1, num_train_epochs=3,
        ),
    }
    print("学习率调度策略:")
    for name, args in schedules.items():
        print(f"  {name}: lr={args.learning_rate}, warmup={args.warmup_ratio}")


# ============================================================
# 2. 梯度检查点（用计算换显存）
# ============================================================
def demo_gradient_checkpointing():
    """演示梯度检查点的显存节省效果"""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

    # 不开启梯度检查点
    params_before = sum(p.numel() for p in model.parameters())
    print(f"模型参数量: {params_before:,}")

    # 开启梯度检查点
    model.gradient_checkpointing_enable()
    print("梯度检查点已开启（显存减少约30-50%，速度慢约20%）")

    # 在TrainingArguments中配置
    args = TrainingArguments(
        output_dir="./tmp",
        gradient_checkpointing=True,  # 开启
        gradient_checkpointing_kwargs={"use_reentrant": False},
    )
    print(f"TrainingArguments.gradient_checkpointing = {args.gradient_checkpointing}")


# ============================================================
# 3. 有效批次大小计算
# ============================================================
def demo_effective_batch_size():
    """演示梯度累积的等效批次大小"""
    configs = [
        {"batch_size": 1, "accumulation": 16, "gpus": 1},
        {"batch_size": 2, "accumulation": 8, "gpus": 1},
        {"batch_size": 4, "accumulation": 4, "gpus": 1},
        {"batch_size": 2, "accumulation": 4, "gpus": 2},
    ]
    print("有效批次大小 = batch_size × accumulation × GPU数")
    for c in configs:
        effective = c["batch_size"] * c["accumulation"] * c["gpus"]
        print(f"  {c['batch_size']} × {c['accumulation']} × {c['gpus']}GPU = {effective}")


# ============================================================
# 4. 推荐训练配置模板
# ============================================================
def demo_recommended_configs():
    """不同场景的推荐训练配置"""

    # LoRA微调推荐配置
    lora_args = TrainingArguments(
        output_dir="./output/lora",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        weight_decay=0.01,
        logging_steps=10,
        save_strategy="steps",
        save_steps=100,
        gradient_checkpointing=True,
        report_to="none",
    )
    print("LoRA推荐配置:")
    print(f"  lr={lora_args.learning_rate}, epochs={lora_args.num_train_epochs}")
    print(f"  batch={lora_args.per_device_train_batch_size}, accum={lora_args.gradient_accumulation_steps}")
    print(f"  scheduler={lora_args.lr_scheduler_type}, warmup={lora_args.warmup_ratio}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 学习率调度策略")
    print("=" * 60)
    demo_lr_schedules()

    print("\n" + "=" * 60)
    print("2. 梯度检查点")
    print("=" * 60)
    demo_gradient_checkpointing()

    print("\n" + "=" * 60)
    print("3. 有效批次大小")
    print("=" * 60)
    demo_effective_batch_size()

    print("\n" + "=" * 60)
    print("4. 推荐训练配置")
    print("=" * 60)
    demo_recommended_configs()
