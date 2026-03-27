"""
4. 分布式训练 - 代码示例
演示DeepSpeed和Accelerate的配置和使用方式。
"""

import json


# ============================================================
# 1. DeepSpeed配置生成
# ============================================================
def generate_deepspeed_configs():
    """生成不同ZeRO阶段的DeepSpeed配置"""

    # ZeRO Stage 2（最常用）
    ds_config_z2 = {
        "bf16": {"enabled": True},
        "zero_optimization": {
            "stage": 2,
            "offload_optimizer": {"device": "none"},
            "allgather_partitions": True,
            "allgather_bucket_size": 2e8,
            "reduce_scatter": True,
            "reduce_bucket_size": 2e8,
        },
        "gradient_accumulation_steps": 4,
        "gradient_clipping": 1.0,
        "train_batch_size": "auto",
        "train_micro_batch_size_per_gpu": "auto",
    }

    # ZeRO Stage 3（训练超大模型）
    ds_config_z3 = {
        "bf16": {"enabled": True},
        "zero_optimization": {
            "stage": 3,
            "offload_optimizer": {"device": "cpu"},
            "offload_param": {"device": "cpu"},
            "overlap_comm": True,
            "contiguous_gradients": True,
        },
        "gradient_accumulation_steps": 8,
        "gradient_clipping": 1.0,
        "train_batch_size": "auto",
        "train_micro_batch_size_per_gpu": "auto",
    }

    for name, config in [("zero2", ds_config_z2), ("zero3", ds_config_z3)]:
        filename = f"ds_config_{name}.json"
        with open(filename, "w") as f:
            json.dump(config, f, indent=2)
        print(f"已生成 {filename}")
        print(f"  使用: deepspeed --num_gpus=4 train.py --deepspeed {filename}")


# ============================================================
# 2. Accelerate配置
# ============================================================
def generate_accelerate_config():
    """生成HuggingFace Accelerate配置"""
    config = """# Accelerate配置示例
# 生成: accelerate config
# 使用: accelerate launch train.py

compute_environment: LOCAL_MACHINE
distributed_type: MULTI_GPU
num_machines: 1
num_processes: 4
mixed_precision: bf16
use_cpu: false

# DeepSpeed集成
deepspeed_config:
  deepspeed_config_file: ds_config_zero2.json
  zero3_init_flag: false
"""
    with open("accelerate_config.yaml", "w") as f:
        f.write(config)
    print("已生成 accelerate_config.yaml")
    print("  使用: accelerate launch --config_file accelerate_config.yaml train.py")


# ============================================================
# 3. 显存估算
# ============================================================
def estimate_memory():
    """估算不同并行策略的显存需求"""
    param_billions = [1, 7, 13, 70]

    print("显存估算（全量微调，fp16）:")
    print(f"{'参数量':>8s} | {'单卡(无优化)':>12s} | {'ZeRO-2(4卡)':>12s} | {'ZeRO-3(4卡)':>12s}")
    print("-" * 60)

    for b in param_billions:
        params_gb = b * 2  # fp16
        # 全量微调: 参数 + 梯度 + 优化器(Adam 2x) ≈ 参数 × 8
        single = params_gb * 8
        # ZeRO-2: 优化器+梯度分片
        zero2 = params_gb * 2 + (params_gb * 6) / 4
        # ZeRO-3: 全部分片
        zero3 = (params_gb * 8) / 4

        print(f"{b:>6d}B | {single:>10.1f}GB | {zero2:>10.1f}GB | {zero3:>10.1f}GB")


# ============================================================
# 4. 训练脚本模板
# ============================================================
def generate_train_script():
    """生成分布式训练脚本模板"""
    script = '''"""分布式训练脚本模板"""
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset

model_name = "Qwen/Qwen2.5-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

dataset = load_dataset("json", data_files="train.json", split="train")

args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    bf16=True,
    gradient_checkpointing=True,
    deepspeed="ds_config_zero2.json",  # DeepSpeed
    report_to="wandb",
)

trainer = Trainer(model=model, args=args, train_dataset=dataset)
trainer.train()
'''
    print("分布式训练脚本模板:")
    print(script)
    print("启动命令:")
    print("  accelerate launch --num_processes 4 train.py")
    print("  # 或")
    print("  deepspeed --num_gpus 4 train.py --deepspeed ds_config_zero2.json")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. DeepSpeed配置")
    print("=" * 60)
    generate_deepspeed_configs()

    print("\n" + "=" * 60)
    print("2. Accelerate配置")
    print("=" * 60)
    generate_accelerate_config()

    print("\n" + "=" * 60)
    print("3. 显存估算")
    print("=" * 60)
    estimate_memory()

    print("\n" + "=" * 60)
    print("4. 训练脚本模板")
    print("=" * 60)
    generate_train_script()
