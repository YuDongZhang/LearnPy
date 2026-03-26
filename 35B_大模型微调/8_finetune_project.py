"""
8. 微调实战项目 - QLoRA微调中文问答助手
完整流程：数据准备 → 模型加载 → QLoRA配置 → 训练 → 评估 → 推理
"""

import json
import sys
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, PeftModel, TaskType
from trl import SFTTrainer


# ============================================================
# 配置
# ============================================================
MODEL_NAME = "Qwen/Qwen2.5-0.5B"  # 小模型方便学习，实际可换1.5B/7B
OUTPUT_DIR = "./output/project_qlora"
MAX_LENGTH = 512


# ============================================================
# 1. 准备Python编程问答数据集
# ============================================================
def create_dataset():
    """创建Python编程领域的问答数据集"""
    data = [
        {"instruction": "什么是Python的装饰器？请举例说明", "input": "",
         "output": "装饰器是Python中用于修改函数行为的语法糖。它本质上是一个高阶函数。\n\n```python\ndef timer(func):\n    import time\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'耗时: {time.time()-start:.2f}s')\n        return result\n    return wrapper\n\n@timer\ndef slow_func():\n    time.sleep(1)\n```"},
        {"instruction": "解释Python中的生成器和迭代器的区别", "input": "",
         "output": "迭代器是实现了__iter__和__next__方法的对象。生成器是一种特殊的迭代器，使用yield关键字定义，更简洁。\n\n生成器函数每次yield时暂停，下次调用next()时从暂停处继续。生成器是惰性求值的，适合处理大数据。"},
        {"instruction": "如何在Python中实现单例模式？", "input": "",
         "output": "Python实现单例模式有多种方式：\n\n1. 使用装饰器：\n```python\ndef singleton(cls):\n    instances = {}\n    def get_instance(*args, **kwargs):\n        if cls not in instances:\n            instances[cls] = cls(*args, **kwargs)\n        return instances[cls]\n    return get_instance\n```\n\n2. 使用__new__方法：\n```python\nclass Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n```"},
        {"instruction": "解释Python的GIL及其影响", "input": "",
         "output": "GIL（全局解释器锁）是CPython中的互斥锁，确保同一时刻只有一个线程执行Python字节码。\n\n影响：\n- CPU密集型任务：多线程无法利用多核，应使用multiprocessing\n- IO密集型任务：线程在等待IO时会释放GIL，多线程仍然有效\n- 解决方案：多进程、C扩展、使用其他Python实现（如PyPy）"},
        {"instruction": "Python中的上下文管理器怎么用？", "input": "",
         "output": "上下文管理器通过with语句管理资源，确保资源正确释放。\n\n```python\n# 方式1: 类实现\nclass FileManager:\n    def __init__(self, filename):\n        self.filename = filename\n    def __enter__(self):\n        self.file = open(self.filename, 'r')\n        return self.file\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()\n\n# 方式2: contextlib\nfrom contextlib import contextmanager\n\n@contextmanager\ndef open_file(name):\n    f = open(name, 'r')\n    try:\n        yield f\n    finally:\n        f.close()\n```"},
        {"instruction": "什么是Python的列表推导式？和map/filter有什么区别？", "input": "",
         "output": "列表推导式是创建列表的简洁语法：[expr for x in iterable if condition]\n\n```python\n# 列表推导式\nsquares = [x**2 for x in range(10) if x % 2 == 0]\n\n# 等价的map+filter\nsquares = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(10))))\n```\n\n列表推导式更Pythonic、可读性更好。map/filter返回迭代器，内存效率更高。"},
        {"instruction": "解释Python的多重继承和MRO", "input": "",
         "output": "Python支持多重继承，一个类可以继承多个父类。MRO（方法解析顺序）决定了方法查找顺序，使用C3线性化算法。\n\n```python\nclass A:\n    def method(self): print('A')\nclass B(A):\n    def method(self): print('B')\nclass C(A):\n    def method(self): print('C')\nclass D(B, C):\n    pass\n\n# MRO: D -> B -> C -> A\nprint(D.mro())  # [D, B, C, A, object]\nD().method()    # 输出: B\n```"},
        {"instruction": "如何优化Python代码的性能？", "input": "",
         "output": "Python性能优化方法：\n\n1. 算法优化：选择合适的数据结构和算法\n2. 内置函数：用map/filter/sum等替代手写循环\n3. 列表推导式：比for循环快\n4. 生成器：处理大数据时节省内存\n5. 缓存：使用functools.lru_cache\n6. 并发：IO密集用asyncio/threading，CPU密集用multiprocessing\n7. C扩展：用Cython或ctypes调用C代码\n8. 性能分析：用cProfile定位瓶颈"},
    ]

    def format_text(example):
        text = f"### 指令:\n{example['instruction']}\n### 回答:\n{example['output']}"
        return {"text": text}

    dataset = Dataset.from_list(data).map(format_text)
    print(f"数据集准备完成: {len(dataset)} 条")
    return dataset


# ============================================================
# 2. 训练
# ============================================================
def train():
    """QLoRA微调训练"""
    print("=" * 60)
    print("开始QLoRA微调训练")
    print("=" * 60)

    # 加载Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 加载模型（尝试4bit量化，失败则用fp32）
    try:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True,
            quantization_config=bnb_config, device_map="auto",
        )
        use_bf16 = True
        print("使用4bit量化加载（QLoRA模式）")
    except Exception:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True,
        )
        use_bf16 = False
        print("使用fp32加载（无GPU或不支持量化）")

    # LoRA配置
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # 数据
    dataset = create_dataset()

    # 训练
    trainer = SFTTrainer(
        model=model,
        args=TrainingArguments(
            output_dir=OUTPUT_DIR,
            num_train_epochs=3,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            lr_scheduler_type="cosine",
            warmup_ratio=0.1,
            logging_steps=1,
            save_strategy="epoch",
            bf16=use_bf16,
            gradient_checkpointing=True,
            report_to="none",
        ),
        train_dataset=dataset,
        processing_class=tokenizer,
        max_seq_length=MAX_LENGTH,
    )

    trainer.train()
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"\n训练完成，权重保存到: {OUTPUT_DIR}")


# ============================================================
# 3. 推理对比（微调前 vs 微调后）
# ============================================================
def inference():
    """对比微调前后的回答质量"""
    print("=" * 60)
    print("推理对比: 微调前 vs 微调后")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

    # 微调前
    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

    # 微调后
    finetuned_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)
    finetuned_model = PeftModel.from_pretrained(finetuned_model, OUTPUT_DIR)

    questions = [
        "什么是Python的装饰器？",
        "解释Python的GIL",
        "如何优化Python性能？",
    ]

    for q in questions:
        prompt = f"### 指令:\n{q}\n### 回答:\n"
        inputs = tokenizer(prompt, return_tensors="pt")

        print(f"\n问: {q}")

        # 微调前
        out1 = base_model.generate(**inputs, max_new_tokens=150, do_sample=False)
        ans1 = tokenizer.decode(out1[0], skip_special_tokens=True)
        print(f"[微调前] {ans1[len(prompt):][:100]}...")

        # 微调后
        out2 = finetuned_model.generate(**inputs, max_new_tokens=150, do_sample=False)
        ans2 = tokenizer.decode(out2[0], skip_special_tokens=True)
        print(f"[微调后] {ans2[len(prompt):][:100]}...")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "train"

    if mode == "train":
        train()
    elif mode == "inference":
        inference()
    else:
        print("用法: python 8_finetune_project.py [train|inference]")
