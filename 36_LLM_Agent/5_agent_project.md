# 5. Agent实战项目

## 项目概述

本节通过两个实战项目，综合运用前面学到的Agent知识：

1. **智能研究助手** — 自动搜索+摘要+多轮对话
2. **多Agent协作系统** — 研究员+写手+审核员协作完成任务

## 项目一：智能研究助手

### 功能
- 接收用户的研究主题
- 自动搜索互联网获取信息
- 对搜索结果进行摘要
- 支持多轮追问

### 技术要点
- 使用 `CONVERSATIONAL_REACT_DESCRIPTION` 类型（支持对话记忆）
- 集成 `DuckDuckGoSearchRun` 搜索工具
- 使用 `ConversationBufferMemory` 保持上下文

### 使用方式
```bash
python 5_agent_project.py
```
运行后进入交互模式，输入研究主题即可。输入 `exit` 退出。

## 项目二：多Agent协作系统

### 架构
```
用户输入主题
    ↓
研究员Agent → 搜索收集信息
    ↓
写手Agent → 基于研究结果撰写报告
    ↓
审核员Agent → 审核报告质量
    ↓
输出最终报告
```

### 技术要点
- 三个独立Agent，各自有专属工具
- 通过Python代码编排协作流程
- 上一个Agent的输出作为下一个Agent的输入

## 运行前准备

1. 安装依赖：
```bash
pip install langchain langchain-openai langchain-community duckduckgo-search
```

2. 设置环境变量：
```bash
export OPENAI_API_KEY="your-api-key"
```

## 扩展方向

- 加入更多工具（代码执行、文件读写等）
- 使用LangGraph实现更复杂的Agent工作流
- 加入向量数据库实现长期记忆
- 部署为Web服务
