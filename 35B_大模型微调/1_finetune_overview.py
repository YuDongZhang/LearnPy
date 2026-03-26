"""
1. 微调概述 - 代码示例
演示如何查看模型结构和参数量，理解微调的基本概念。
"""

from transformers import AutoModelForCausalLM, AutoTokenizer


# ============================================================
# 1. 加载一个小模型，查看结构
# ============================================================
def demo_model_structure():
    """加载模型并查看参数信息"""
    model_name = "Qwen/Qwen2.5-0.5B"  # 小模型，方便学习

    print(f"加载模型: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, trust_remote_code=True, device_map="auto"
    )

    # 查看模型结构
    print("\n模型结构（前几层）:")
    for name, param in list(model.named_parameters())[:10]:
        print(f"  {name}: {param.shape}")

    # 统计参数量
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n总参数量: {total_params:,}")
    print(f"可训练参数: {trainable_params:,}")
    print(f"模型大小(fp16): ~{total_params * 2 / 1024**3:.2f} GB")


# ============================================================
# 2. 简单推理测试（微调前的基线）
# ============================================================
def demo_baseline_inference():
    """微调前先测试模型的基线表现"""
    model_name = "Qwen/Qwen2.5-0.5B"

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, trust_remote_code=True, device_map="auto"
    )

    questions = [
        "Python中的装饰器是什么？",
        "解释一下什么是LoRA微调",
    ]

    print("基线推理测试:")
    for q in questions:
        inputs = tokenizer(q, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=100, do_sample=False)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\n问: {q}")
        print(f"答: {answer}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 查看模型结构和参数量")
    print("=" * 60)
    demo_model_structure()

    print("\n" + "=" * 60)
    print("2. 基线推理测试")
    print("=" * 60)
    demo_baseline_inference()
