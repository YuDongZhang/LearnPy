"""
1. 部署概述 - 代码示例
演示用Transformers加载模型进行本地推理（最基础的部署方式）。
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import time


# ============================================================
# 1. 基础本地推理
# ============================================================
def demo_basic_inference():
    """用Transformers加载模型并推理"""
    model_name = "Qwen/Qwen2.5-0.5B"  # 小模型演示

    print(f"加载模型: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, device_map="auto")

    question = "什么是Python的装饰器？"
    inputs = tokenizer(question, return_tensors="pt").to(model.device)

    start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    elapsed = time.time() - start

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    tokens_generated = outputs.shape[1] - inputs["input_ids"].shape[1]

    print(f"问: {question}")
    print(f"答: {answer}")
    print(f"生成 {tokens_generated} tokens，耗时 {elapsed:.2f}s")
    print(f"速度: {tokens_generated/elapsed:.1f} tokens/s")


# ============================================================
# 2. 对比不同精度的推理速度
# ============================================================
def demo_precision_comparison():
    """对比fp32和fp16的推理速度"""
    import torch
    model_name = "Qwen/Qwen2.5-0.5B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    configs = [
        ("fp32", {}),
        ("fp16", {"torch_dtype": torch.float16}),
    ]

    question = "Python是什么？"
    inputs = tokenizer(question, return_tensors="pt")

    for name, kwargs in configs:
        try:
            model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, **kwargs)
            inputs_device = {k: v.to(model.device) for k, v in inputs.items()}

            start = time.time()
            outputs = model.generate(**inputs_device, max_new_tokens=50, do_sample=False)
            elapsed = time.time() - start

            tokens = outputs.shape[1] - inputs["input_ids"].shape[1]
            print(f"  {name}: {tokens} tokens, {elapsed:.2f}s, {tokens/elapsed:.1f} tok/s")
            del model
        except Exception as e:
            print(f"  {name}: 不支持 ({e})")


if __name__ == "__main__":
    print("=" * 60)
    print("1. 基础本地推理")
    print("=" * 60)
    demo_basic_inference()

    print("\n" + "=" * 60)
    print("2. 精度对比")
    print("=" * 60)
    demo_precision_comparison()
