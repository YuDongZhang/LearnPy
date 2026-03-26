"""
7. 微调工具 - 代码示例
演示LLaMA-Factory的配置文件和Unsloth的使用方式。
"""


# ============================================================
# 1. LLaMA-Factory YAML配置示例
# ============================================================
def demo_llamafactory_config():
    """生成LLaMA-Factory的训练配置文件"""
    config = """
# LLaMA-Factory 训练配置示例
# 使用方式: llamafactory-cli train config.yaml

### 模型配置
model_name_or_path: Qwen/Qwen2.5-1.5B
trust_remote_code: true

### 微调方法
stage: sft
finetuning_type: lora
lora_rank: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target: all

### 数据集
dataset: alpaca_zh
template: qwen
cutoff_len: 1024

### 输出
output_dir: output/qwen-lora

### 训练参数
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
num_train_epochs: 3
learning_rate: 1.0e-4
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
gradient_checkpointing: true

### 日志
logging_steps: 10
save_steps: 100
"""
    # 保存配置文件
    with open("llamafactory_config.yaml", "w") as f:
        f.write(config)
    print("LLaMA-Factory配置已保存: llamafactory_config.yaml")
    print(config)
    print("运行方式:")
    print("  1. WebUI: llamafactory-cli webui")
    print("  2. 命令行: llamafactory-cli train llamafactory_config.yaml")


# ============================================================
# 2. Unsloth使用示例
# ============================================================
def demo_unsloth():
    """Unsloth微调示例（需要安装unsloth）"""
    code = '''
# pip install unsloth
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 1. 加载模型（Unsloth优化版，速度快2-5倍）
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-1.5B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

# 2. 添加LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0,
    use_gradient_checkpointing="unsloth",  # Unsloth优化版
)

# 3. 准备数据
dataset = load_dataset("silk-road/alpaca-data-gpt4-chinese", split="train")

# 4. 训练
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    max_seq_length=2048,
    args=TrainingArguments(
        output_dir="output/unsloth",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=10,
        report_to="none",
    ),
)
trainer.train()

# 5. 保存
model.save_pretrained("output/unsloth/lora")
# 或合并保存: model.save_pretrained_merged("output/unsloth/merged", tokenizer)
'''
    print("Unsloth微调示例代码:")
    print(code)


# ============================================================
# 3. 工具选择指南
# ============================================================
def demo_tool_guide():
    """打印工具选择建议"""
    print("微调工具选择指南:")
    print()
    print("  场景                    → 推荐工具")
    print("  " + "-" * 50)
    print("  初学者快速体验          → LLaMA-Factory (WebUI)")
    print("  深入理解原理            → Transformers + PEFT")
    print("  追求训练速度            → Unsloth")
    print("  生产环境                → Transformers + PEFT")
    print("  中文生态                → Swift (魔搭)")
    print("  配置文件驱动            → Axolotl")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. LLaMA-Factory配置")
    print("=" * 60)
    demo_llamafactory_config()

    print("\n" + "=" * 60)
    print("2. Unsloth示例")
    print("=" * 60)
    demo_unsloth()

    print("\n" + "=" * 60)
    print("3. 工具选择指南")
    print("=" * 60)
    demo_tool_guide()
