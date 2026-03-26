"""
4. LoRA与QLoRA微调 - 代码示例（重点）
演示使用PEFT库进行LoRA/QLoRA微调的完整流程。
"""

import json
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer


# ============================================================
# 配置
# ============================================================
MODEL_NAME = "Qwen/Qwen2.5-0.5B"
OUTPUT_DIR = "./output/lora_finetune"
MAX_LENGTH = 256


# ============================================================
# 1. 准备数据
# ============================================================
def prepare_data():
    data = [
        {"instruction": "解释Python装饰器", "input": "", "output": "装饰器是修改函数行为的语法糖，用@符号应用。本质是高阶函数，接受函数作为参数并返回新函数。"},
        {"instruction": "什么是列表推导式", "input": "", "output": "列表推导式是创建列表的简洁语法：[expr for x in iterable if condition]。比for循环更Pythonic。"},
        {"instruction": "解释GIL", "input": "", "output": "GIL是CPython的全局解释器锁，限制同一时刻只有一个线程执行字节码。多线程适合IO密集型，CPU密集型用多进程。"},
        {"instruction": "什么是生成器", "input": "", "output": "生成器是使用yield的函数，惰性产生值，节省内存。适合处理大数据集或无限序列。"},
        {"instruction": "解释async/await", "input": "", "output": "async定义协程函数，await等待异步操作完成。配合asyncio使用，适合IO密集型任务如网络请求。"},
        {"instruction": "什么是上下文管理器", "input": "", "output": "上下文管理器通过with语句管理资源的获取和释放。实现__enter__和__exit__方法，或使用contextlib.contextmanager装饰器。"},
        {"instruction": "解释Python的多重继承", "input": "", "output": "Python支持多重继承，一个类可以继承多个父类。方法解析顺序(MRO)使用C3线性化算法，可通过ClassName.mro()查看。"},
        {"instruction": "什么是元类", "input": "", "output": "元类是创建类的类。Python中type是默认元类。通过定义__metaclass__或metaclass参数自定义类的创建行为。"},
    ]

    def format_text(example):
        if example["input"]:
            text = f"### 指令:\n{example['instruction']}\n### 输入:\n{example['input']}\n### 回答:\n{example['output']}"
        else:
            text = f"### 指令:\n{example['instruction']}\n### 回答:\n{example['output']}"
        return {"text": text}

    dataset = Dataset.from_list(data)
    return dataset.map(format_text)


# ============================================================
# 2. LoRA微调（fp16）
# ============================================================
def train_lora():
    """标准LoRA微调"""
    print("=" * 60)
    print("LoRA微调")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, trust_remote_code=True, torch_dtype=torch.float32
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # LoRA配置
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,                        # 秩
        lora_alpha=16,              # 缩放系数
        lora_dropout=0.05,          # Dropout
        target_modules=["q_proj", "v_proj"],  # 应用LoRA的层
    )

    # 包装模型
    model = get_peft_model(model, lora_config)

    # 查看参数量对比
    model.print_trainable_parameters()

    # 准备数据
    dataset = prepare_data()

    # 训练参数
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,         # LoRA学习率比全量微调大
        warmup_ratio=0.1,
        logging_steps=1,
        save_strategy="epoch",
        report_to="none",
    )

    # 使用SFTTrainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        max_seq_length=MAX_LENGTH,
    )

    print("\n开始LoRA训练...")
    trainer.train()

    # 保存LoRA权重（很小，通常几MB）
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"\nLoRA权重已保存到: {OUTPUT_DIR}")


# ============================================================
# 3. QLoRA微调（4bit量化）
# ============================================================
def train_qlora():
    """QLoRA微调（需要GPU + bitsandbytes）"""
    print("=" * 60)
    print("QLoRA微调")
    print("=" * 60)

    # 4bit量化配置
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
        quantization_config=bnb_config,
        device_map="auto",
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # LoRA配置（QLoRA = 4bit模型 + LoRA）
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    dataset = prepare_data()

    training_args = TrainingArguments(
        output_dir="./output/qlora_finetune",
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        warmup_ratio=0.1,
        logging_steps=1,
        save_strategy="epoch",
        bf16=True,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        max_seq_length=MAX_LENGTH,
    )

    print("\n开始QLoRA训练...")
    trainer.train()

    model.save_pretrained("./output/qlora_finetune")
    tokenizer.save_pretrained("./output/qlora_finetune")
    print("\nQLoRA权重已保存")


# ============================================================
# 4. 推理 + 合并权重
# ============================================================
def inference_and_merge():
    """加载LoRA权重推理，并演示合并"""
    from peft import PeftModel

    print("加载基座模型...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

    print("加载LoRA权重...")
    model = PeftModel.from_pretrained(base_model, OUTPUT_DIR)

    # 推理
    question = "### 指令:\n解释Python装饰器\n### 回答:\n"
    inputs = tokenizer(question, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    print(f"LoRA推理: {tokenizer.decode(outputs[0], skip_special_tokens=True)}")

    # 合并权重
    print("\n合并LoRA权重到基座模型...")
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained("./output/merged_model")
    tokenizer.save_pretrained("./output/merged_model")
    print("合并后的完整模型已保存到 ./output/merged_model")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "lora"

    if mode == "lora":
        train_lora()
    elif mode == "qlora":
        train_qlora()
    elif mode == "inference":
        inference_and_merge()
    else:
        print("用法: python 4_lora.py [lora|qlora|inference]")
