# 4. AutoGen框架

## 什么是AutoGen

AutoGen是微软推出的多Agent对话框架，核心理念是"通过对话实现协作"。多个Agent之间通过自然语言对话来完成任务，而不是通过代码编排流程。

## 核心特性

- **对话驱动** — Agent之间通过对话协作，自然直观
- **代码执行** — 内置代码生成和执行能力
- **人类参与** — 灵活的人类介入模式
- **群聊** — 支持多Agent群聊讨论

## 核心Agent类型

| Agent类型 | 说明 | 用途 |
|-----------|------|------|
| AssistantAgent | AI助手，由LLM驱动 | 推理、生成、分析 |
| UserProxyAgent | 用户代理，可执行代码 | 代码执行、人类输入代理 |
| GroupChatManager | 群聊管理器 | 协调多Agent群聊 |

## 人类参与模式

`human_input_mode` 控制何时需要人类输入：
- `NEVER` — 完全自动，不需要人类
- `TERMINATE` — 结束时请求人类确认
- `ALWAYS` — 每轮都请求人类输入

## 对话模式

### 1对1对话
两个Agent之间直接对话，一个提问一个回答。

### 群聊（GroupChat）
多个Agent在同一个聊天中讨论，由GroupChatManager协调发言顺序。

### 嵌套对话
一个Agent在处理任务时，内部启动另一组Agent的对话。

## 代码执行

AutoGen的一大特色是内置代码执行：
- AssistantAgent生成代码
- UserProxyAgent自动执行代码
- 执行结果反馈给AssistantAgent
- 支持Docker沙箱执行（更安全）

## AutoGen vs LangChain

| 特性 | AutoGen | LangChain |
|------|---------|-----------|
| 协作方式 | 对话驱动 | 代码编排 |
| 多Agent | 原生支持 | 需额外配置 |
| 代码执行 | 内置 | 需工具 |
| 人类交互 | 简单灵活 | 较复杂 |
| 工具生态 | 较少 | 非常丰富 |
| 学习曲线 | 中等 | 较低 |

## 最佳实践

1. 每个Agent的system_message要简洁明确
2. 设置`max_consecutive_auto_reply`防止无限对话
3. 群聊设置`max_round`限制轮数
4. 代码执行使用沙箱环境
5. 敏感操作开启人类审核
