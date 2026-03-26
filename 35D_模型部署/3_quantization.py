"""
3. 模型量化 - 代码示例
演示加载GPTQ/AWQ量化模型和bitsandbytes动态量化。
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


MODEL_NAME = "Qwen/Qwen2.5-0.5B"


# ============================================================
# 1. bitsandbytes 8bit量化
# ============================================================
def demo_8bit():
    """8bit动态量化（最简单的量化方式）"""
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True,
            load_in_8bit=True, device_map="auto",
        )
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

        total = sum(p.numel() for p in model.parameters())
        print(f"8bit模型参数: {total:,}")
        print(f"估算显存: ~{total * 1 / 1024**3:.2f} GB (8bit)")

        inputs = tokenizer("Python是", return_tensors="pt").to(model.device)
        out = model.generate(**inputs, max_new_tokens=30, do_sample=False)
        print(f"推理: {tokenizer.decode(out[0], skip_special_tokens=True)}")
    except Exception as e:
        print(f"8bit量化需要GPU + bitsandbytes: {e}")


# ============================================================
# 2. bitsandbytes 4bit量化（NF4）
# ============================================================
def demo_4bit():
    """4bit NF4量化（QLoRA使用的方式）"""
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
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

        total = sum(p.numel() for p in model.parameters())
        print(f"4bit模型参数: {total:,}")
        print(f"估算显存: ~{total * 0.5 / 1024**3:.2f} GB (4bit)")

        inputs = tokenizer("Python是", return_tensors="pt").to(model.device)
        out = model.generate(**inputs, max_new_tokens=30, do_sample=False)
        print(f"推理: {tokenizer.decode(out[0], skip_special_tokens=True)}")
    except Exception as e:
        print(f"4bit量化需要GPU + bitsandbytes: {e}")


# ============================================================
# 3. 显存对比
# ============================================================
def demo_memory_comparison():
    """对比不同精度的显存占用"""
    param_count = 0.5e9  # 0.5B参数

    precisions = [
        ("FP32", 4),
        ("FP16", 2),
        ("INT8", 1),
        ("INT4", 0.5),
    ]
    print("显存估算（0.5B模型，仅模型权重）:")
    for name, bytes_per_param in precisions:
        size_gb = param_count * bytes_per_param / 1024**3
        print(f"  {name:6s}: {size_gb:.2f} GB")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 显存对比")
    print("=" * 60)
    demo_memory_comparison()

    print("\n" + "=" * 60)
    print("2. 8bit量化")
    print("=" * 60)
    demo_8bit()

    print("\n" + "=" * 60)
    print("3. 4bit量化")
    print("=" * 60)
    demo_4bit()
