# 8. 微调实战项目

## 项目：用QLoRA微调一个中文问答助手

### 目标
用QLoRA在Qwen2.5模型上微调一个中文问答助手，让它在特定领域（如Python编程）表现更好。

### 技术方案
- 基座模型：Qwen/Qwen2.5-1.5B（小模型，方便学习）
- 微调方法：QLoRA（4bit量化 + LoRA）
- 数据集：自建Python编程问答数据
- 工具：Transformers + PEFT + TRL

### 流程

```
1. 准备数据集（Alpaca格式的Python问答）
2. 4bit量化加载模型
3. 配置LoRA参数
4. 训练
5. 评估（对比微调前后的回答质量）
6. 保存和合并权重
7. 推理测试
```

### 运行方式

```bash
# 训练
python 8_finetune_project.py --mode train

# 推理测试
python 8_finetune_project.py --mode inference
```

### 数据集示例

```json
[
  {
    "instruction": "解释Python中的装饰器",
    "input": "",
    "output": "装饰器是Python中用于修改函数或类行为的语法糖..."
  },
  {
    "instruction": "写一个Python函数",
    "input": "计算斐波那契数列第n项",
    "output": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
  }
]
```

### 评估方法

1. 人工评估：对比微调前后的回答质量
2. 自动评估：计算验证集的loss
3. 特定任务评估：测试Python编程问题的回答准确性

### 扩展方向

- 换更大的基座模型（7B、14B）
- 增加训练数据量
- 尝试不同的LoRA参数（rank、target_modules）
- 用DPO/RLHF进一步对齐
- 部署为API服务（vLLM + FastAPI）
