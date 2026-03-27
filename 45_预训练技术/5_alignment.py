"""
5. RLHF与DPO对齐 - 代码示例
演示DPO训练的数据准备和使用TRL库进行DPO训练。
"""

import json
from datasets import Dataset


# ============================================================
# 1. DPO数据准备
# ============================================================
def create_dpo_dataset():
    """创建DPO偏好数据集"""
    data = [
        {
            "prompt": "解释Python的装饰器",
            "chosen": "装饰器是Python中用于修改函数行为的语法糖。它本质上是一个高阶函数，接受函数作为参数并返回新函数。使用@符号应用，常用于日志、缓存、权限控制等场景。",
            "rejected": "装饰器就是一个东西，用来装饰函数的。"
        },
        {
            "prompt": "什么是GIL？",
            "chosen": "GIL（全局解释器锁）是CPython中的互斥锁，确保同一时刻只有一个线程执行Python字节码。这限制了多线程的并行能力，CPU密集型任务建议使用multiprocessing。",
            "rejected": "GIL是Python的一个锁，让Python很慢。"
        },
        {
            "prompt": "如何优化Python性能？",
            "chosen": "Python性能优化方法：1.选择合适的数据结构和算法 2.使用内置函数和列表推导式 3.用生成器处理大数据 4.functools.lru_cache缓存 5.IO密集用asyncio，CPU密集用multiprocessing 6.用cProfile定位瓶颈。",
            "rejected": "用C语言重写就行了。"
        },
        {
            "prompt": "Python怎么读取JSON文件？",
            "chosen": "使用json模块：\n```python\nimport json\nwith open('data.json', 'r', encoding='utf-8') as f:\n    data = json.load(f)\n```\njson.load()读取文件对象，json.loads()读取字符串。",
            "rejected": "import json然后load"
        },
    ]

    # 保存
    with open("dpo_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    dataset = Dataset.from_list(data)
    print(f"DPO数据集: {len(dataset)} 条")
    print(f"示例: prompt={data[0]['prompt'][:30]}...")
    return dataset


# ============================================================
# 2. DPO训练（使用TRL库）
# ============================================================
def demo_dpo_training():
    """DPO训练示例代码（展示用，实际运行需要GPU）"""
    code = '''
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset
from peft import LoraConfig

# 加载模型
model_name = "Qwen/Qwen2.5-0.5B"
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# 加载DPO数据
dataset = load_dataset("json", data_files="dpo_data.json", split="train")

# LoRA配置（DPO也可以用LoRA降低显存）
peft_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"])

# DPO训练配置
training_args = DPOConfig(
    output_dir="./output/dpo",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=5e-5,
    beta=0.1,  # DPO的温度参数
    logging_steps=1,
    report_to="none",
)

# 创建DPO Trainer
trainer = DPOTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
)

# 训练
trainer.train()
trainer.save_model("./output/dpo")
'''
    print("DPO训练代码:")
    print(code)


# ============================================================
# 3. 对齐方法对比
# ============================================================
def compare_alignment_methods():
    """对比不同对齐方法"""
    methods = [
        {"name": "RLHF(PPO)", "models": 4, "complexity": "高", "stability": "差", "effect": "很好"},
        {"name": "DPO", "models": 1, "complexity": "低", "stability": "好", "effect": "好"},
        {"name": "ORPO", "models": 1, "complexity": "低", "stability": "好", "effect": "好"},
        {"name": "SimPO", "models": 1, "complexity": "很低", "stability": "很好", "effect": "中"},
        {"name": "KTO", "models": 1, "complexity": "低", "stability": "好", "effect": "中"},
    ]

    print("对齐方法对比:")
    print(f"{'方法':>12s} | {'模型数':>4s} | {'复杂度':>4s} | {'稳定性':>4s} | {'效果':>4s}")
    print("-" * 50)
    for m in methods:
        print(f"{m['name']:>12s} | {m['models']:>4d} | {m['complexity']:>4s} | {m['stability']:>4s} | {m['effect']:>4s}")
    print("\n当前主流: DPO（简单有效，推荐）")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 创建DPO数据集")
    print("=" * 60)
    create_dpo_dataset()

    print("\n" + "=" * 60)
    print("2. DPO训练代码")
    print("=" * 60)
    demo_dpo_training()

    print("\n" + "=" * 60)
    print("3. 对齐方法对比")
    print("=" * 60)
    compare_alignment_methods()
