"""
3. 全量微调 - 代码示例
演示使用Transformers进行全量微调的完整流程。
注意：全量微调7B模型需要60GB+显存，这里用小模型演示。
"""

import json
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)


# ============================================================
# 配置
# ============================================================
MODEL_NAME = "Qwen/Qwen2.5-0.5B"  # 小模型，方便学习
OUTPUT_DIR = "./output/full_finetune"
MAX_LENGTH = 256


# ============================================================
# 1. 准备数据
# ============================================================
def prepare_data(tokenizer):
    """准备训练数据"""
    data = [
        {"instruction": "解释Python装饰器", "input": "", "output": "装饰器是修改函数行为的语法糖，用@符号应用。"},
        {"instruction": "什么是列表推导式", "input": "", "output": "列表推导式是创建列表的简洁语法：[expr for x in iterable]。"},
        {"instruction": "解释GIL", "input": "", "output": "GIL是CPython的全局解释器锁，限制同一时刻只有一个线程执行字节码。"},
        {"instruction": "什么是生成器", "input": "", "output": "生成器是使用yield的函数，惰性产生值，节省内存。"},
        {"instruction": "解释async/await", "input": "", "output": "async定义协程，await等待异步操作，用于IO密集型任务。"},
    ]

    def format_and_tokenize(example):
        text = f"### 指令:\n{example['instruction']}\n### 回答:\n{example['output']}{tokenizer.eos_token}"
        tokens = tokenizer(text, truncation=True, max_length=MAX_LENGTH, padding="max_length")
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    dataset = Dataset.from_list(data)
    tokenized = dataset.map(format_and_tokenize, remove_columns=dataset.column_names)
    return tokenized


# ============================================================
# 2. 全量微调
# ============================================================
def train():
    """全量微调流程"""
    # 加载模型和Tokenizer
    print(f"加载模型: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 查看参数量
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"总参数: {total:,} | 可训练: {trainable:,} (100%)")

    # 准备数据
    dataset = prepare_data(tokenizer)
    print(f"训练数据: {len(dataset)} 条")

    # 训练参数
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        warmup_ratio=0.1,
        weight_decay=0.01,
        logging_steps=1,
        save_strategy="epoch",
        fp16=False,  # 小模型CPU训练时关闭
        report_to="none",
    )

    # 创建Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    # 开始训练
    print("\n开始全量微调...")
    trainer.train()

    # 保存
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"\n模型已保存到: {OUTPUT_DIR}")


# ============================================================
# 3. 推理测试
# ============================================================
def inference():
    """加载微调后的模型进行推理"""
    print(f"加载微调模型: {OUTPUT_DIR}")
    tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(OUTPUT_DIR, trust_remote_code=True)

    question = "### 指令:\n解释Python装饰器\n### 回答:\n"
    inputs = tokenizer(question, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"问: 解释Python装饰器")
    print(f"答: {answer}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "train"

    if mode == "train":
        train()
    elif mode == "inference":
        inference()
    else:
        print("用法: python 3_full_finetune.py [train|inference]")
