"""
5. 其他PEFT方法 - 代码示例
演示P-Tuning v2和Prefix Tuning的配置方式。
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import (
    get_peft_model,
    LoraConfig,
    PrefixTuningConfig,
    PromptTuningConfig,
    TaskType,
)


MODEL_NAME = "Qwen/Qwen2.5-0.5B"


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)
    return model, tokenizer


# ============================================================
# 1. LoRA（对比基线）
# ============================================================
def demo_lora():
    model, tokenizer = load_model()
    config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
    )
    peft_model = get_peft_model(model, config)
    print("LoRA:")
    peft_model.print_trainable_parameters()


# ============================================================
# 2. Prefix Tuning
# ============================================================
def demo_prefix_tuning():
    model, tokenizer = load_model()
    config = PrefixTuningConfig(
        task_type=TaskType.CAUSAL_LM,
        num_virtual_tokens=20,  # 前缀token数量
    )
    peft_model = get_peft_model(model, config)
    print("Prefix Tuning:")
    peft_model.print_trainable_parameters()


# ============================================================
# 3. Prompt Tuning
# ============================================================
def demo_prompt_tuning():
    model, tokenizer = load_model()
    config = PromptTuningConfig(
        task_type=TaskType.CAUSAL_LM,
        num_virtual_tokens=20,
    )
    peft_model = get_peft_model(model, config)
    print("Prompt Tuning:")
    peft_model.print_trainable_parameters()


# ============================================================
# 4. 对比所有方法的参数量
# ============================================================
def compare_all():
    """对比不同PEFT方法的可训练参数量"""
    print("=" * 60)
    print("PEFT方法参数量对比")
    print("=" * 60)

    methods = [
        ("LoRA (r=8)", lambda m: get_peft_model(m, LoraConfig(
            task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16,
            target_modules=["q_proj", "v_proj"]))),
        ("LoRA (r=32)", lambda m: get_peft_model(m, LoraConfig(
            task_type=TaskType.CAUSAL_LM, r=32, lora_alpha=64,
            target_modules=["q_proj", "v_proj"]))),
        ("Prefix Tuning (20)", lambda m: get_peft_model(m, PrefixTuningConfig(
            task_type=TaskType.CAUSAL_LM, num_virtual_tokens=20))),
        ("Prompt Tuning (20)", lambda m: get_peft_model(m, PromptTuningConfig(
            task_type=TaskType.CAUSAL_LM, num_virtual_tokens=20))),
    ]

    for name, create_fn in methods:
        model, _ = load_model()
        peft_model = create_fn(model)
        total = sum(p.numel() for p in peft_model.parameters())
        trainable = sum(p.numel() for p in peft_model.parameters() if p.requires_grad)
        ratio = trainable / total * 100
        print(f"  {name:30s} | 可训练: {trainable:>10,} | 占比: {ratio:.4f}%")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    compare_all()
