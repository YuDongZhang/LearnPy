# 6. CrewAI多Agent框架

## 什么是CrewAI

CrewAI是一个专注于多Agent角色扮演协作的框架。它的核心思想是模拟真实团队：定义Agent的角色（Role）、目标（Goal）、背景（Backstory），然后分配任务（Task），让他们像真实团队一样协作。

## 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| Agent | 有角色和目标的智能体 | 团队成员 |
| Task | 需要完成的具体任务 | 工作任务 |
| Crew | Agent的集合，协作完成任务 | 团队 |
| Tool | Agent可使用的工具 | 工作工具 |
| Process | 任务执行方式 | 工作流程 |

## Agent定义

每个Agent需要三个核心属性：
- **role** — 角色名称（如"高级研究员"）
- **goal** — 目标（如"发现最新的AI趋势"）
- **backstory** — 背景故事（如"你是一位有10年经验的AI研究员..."）

这种角色扮演的方式让LLM更好地进入角色，产出更专业的结果。

## Task定义

每个Task包含：
- **description** — 任务描述
- **expected_output** — 期望输出格式
- **agent** — 负责执行的Agent

## 执行模式（Process）

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| sequential | 任务按顺序执行 | 有依赖关系的任务 |
| hierarchical | 有管理者Agent分配任务 | 复杂项目管理 |

## CrewAI vs AutoGen vs LangGraph

| 特性 | CrewAI | AutoGen | LangGraph |
|------|--------|---------|-----------|
| 核心理念 | 角色扮演团队 | 对话驱动 | 图结构工作流 |
| 上手难度 | 低 | 中 | 中高 |
| 灵活性 | 中 | 高 | 很高 |
| 多Agent | 原生支持 | 原生支持 | 需自行编排 |
| 工具集成 | 内置常用工具 | 较少 | 依赖LangChain |
| 适用场景 | 团队协作任务 | 对话式协作 | 复杂工作流 |

## 最佳实践

1. 角色设计要具体，backstory越详细Agent表现越好
2. Task的expected_output要明确，引导Agent输出格式
3. 合理选择Process模式
4. 善用内置工具（搜索、文件读写等）
5. 复杂任务拆分为多个小Task
