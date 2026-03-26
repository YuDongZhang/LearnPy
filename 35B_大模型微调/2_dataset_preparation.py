"""
2. 数据集准备 - 代码示例
演示如何准备、加载和处理微调数据集。
"""

import json
from datasets import Dataset, load_dataset
from transformers import AutoTokenizer


# ============================================================
# 1. 创建Alpaca格式数据集
# ============================================================
def demo_create_dataset():
    """手动创建一个小型指令数据集"""
    data = [
        {
            "instruction": "解释Python中的列表推导式",
            "input": "",
            "output": "列表推导式是Python中创建列表的简洁语法。格式为 [表达式 for 变量 in 可迭代对象 if 条件]。例如 [x**2 for x in range(10)] 生成0到9的平方列表。"
        },
        {
            "instruction": "写一个Python函数",
            "input": "判断一个数是否为素数",
            "output": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"
        },
        {
            "instruction": "解释Python中的GIL",
            "input": "",
            "output": "GIL（全局解释器锁）是CPython中的互斥锁，确保同一时刻只有一个线程执行Python字节码。这意味着多线程无法利用多核CPU进行并行计算，但IO密集型任务仍然受益于多线程。"
        },
        {
            "instruction": "什么是装饰器？",
            "input": "",
            "output": "装饰器是Python中用于修改函数或类行为的语法糖。它本质上是一个接受函数作为参数并返回新函数的高阶函数。使用@符号应用，常用于日志记录、权限检查、缓存等场景。"
        },
        {
            "instruction": "解释async和await",
            "input": "",
            "output": "async和await是Python异步编程的关键字。async def定义协程函数，await用于等待异步操作完成。它们配合asyncio使用，适合IO密集型任务如网络请求、文件读写。"
        },
    ]

    # 保存为JSON
    with open("train_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已创建数据集: {len(data)} 条")

    # 转为Hugging Face Dataset
    dataset = Dataset.from_list(data)
    print(f"Dataset: {dataset}")
    print(f"示例: {dataset[0]}")
    return dataset


# ============================================================
# 2. 格式化为训练文本
# ============================================================
def demo_format_data():
    """将Alpaca格式转为模型训练所需的文本格式"""

    def format_alpaca(example):
        """Alpaca格式 → 训练文本"""
        if example["input"]:
            text = (
                f"### 指令:\n{example['instruction']}\n\n"
                f"### 输入:\n{example['input']}\n\n"
                f"### 回答:\n{example['output']}"
            )
        else:
            text = (
                f"### 指令:\n{example['instruction']}\n\n"
                f"### 回答:\n{example['output']}"
            )
        return {"text": text}

    # 加载数据
    with open("train_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    dataset = Dataset.from_list(data)

    # 格式化
    formatted = dataset.map(format_alpaca)
    print("格式化后的示例:")
    print(formatted[0]["text"])
    return formatted


# ============================================================
# 3. Tokenize数据
# ============================================================
def demo_tokenize():
    """对数据进行Tokenize处理"""
    model_name = "Qwen/Qwen2.5-0.5B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    # 确保有pad_token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    text = "### 指令:\n解释Python中的装饰器\n\n### 回答:\n装饰器是Python中用于修改函数行为的语法糖。"

    # Tokenize
    tokens = tokenizer(text, truncation=True, max_length=512, padding="max_length")
    print(f"原文长度: {len(text)} 字符")
    print(f"Token数量: {sum(1 for t in tokens['attention_mask'] if t == 1)}")
    print(f"前20个token IDs: {tokens['input_ids'][:20]}")
    print(f"解码回文本: {tokenizer.decode(tokens['input_ids'][:20])}")


# ============================================================
# 4. 加载公开数据集
# ============================================================
def demo_load_public_dataset():
    """从Hugging Face Hub加载公开数据集"""
    # 加载alpaca中文数据集（示例）
    try:
        dataset = load_dataset("silk-road/alpaca-data-gpt4-chinese", split="train[:5]")
        print(f"数据集大小: {len(dataset)}")
        print(f"字段: {dataset.column_names}")
        print(f"示例: {dataset[0]}")
    except Exception as e:
        print(f"加载失败（可能需要网络）: {e}")
        print("可以使用本地数据集替代")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 创建数据集")
    print("=" * 60)
    demo_create_dataset()

    print("\n" + "=" * 60)
    print("2. 格式化数据")
    print("=" * 60)
    demo_format_data()

    print("\n" + "=" * 60)
    print("3. Tokenize")
    print("=" * 60)
    demo_tokenize()

    print("\n" + "=" * 60)
    print("4. 加载公开数据集")
    print("=" * 60)
    demo_load_public_dataset()
