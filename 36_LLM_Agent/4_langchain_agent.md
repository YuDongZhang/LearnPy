# 4. LangChain Agent实践

## LangChain Agent简介

LangChain是目前最流行的LLM应用开发框架，其Agent模块封装了：
- ReAct推理循环
- 多种Agent类型
- 丰富的工具集成
- 记忆系统

## 使用Agent的基本流程

```
1. 创建LLM实例
2. 定义工具列表
3. 初始化Agent（选择类型）
4. 调用Agent执行任务
```

## Agent类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| ZERO_SHOT_REACT_DESCRIPTION | 零样本ReAct，根据工具描述选择 | 最常用，简单任务 |
| CHAT_ZERO_SHOT_REACT_DESCRIPTION | 聊天模型优化版 | 对话场景 |
| CONVERSATIONAL_REACT_DESCRIPTION | 带对话记忆的Agent | 多轮对话 |
| STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION | 支持多参数工具 | 复杂工具输入 |

## 记忆系统集成

Agent可以集成记忆，实现多轮对话：
- `ConversationBufferMemory` — 保存完整对话
- `ConversationSummaryMemory` — 摘要式记忆
- 配合 `CONVERSATIONAL_REACT_DESCRIPTION` 类型使用

## AgentExecutor

`AgentExecutor`是Agent的执行引擎，提供：
- `max_iterations` — 最大迭代次数，防止死循环
- `max_execution_time` — 最大执行时间
- `return_intermediate_steps` — 返回中间步骤，便于调试
- `handle_parsing_errors` — 自动处理输出解析错误

## 调试技巧

1. **verbose=True** — 打印每一步的Thought/Action/Observation
2. **max_iterations** — 限制迭代次数，避免无限循环
3. **return_intermediate_steps** — 查看中间步骤，定位问题
4. **callbacks** — 自定义回调，记录日志或监控

## 常见问题

- Agent选错工具 → 优化工具的description
- 输出格式解析失败 → 开启handle_parsing_errors
- 循环不停 → 设置max_iterations
- 响应太慢 → 减少工具数量，优化工具描述
