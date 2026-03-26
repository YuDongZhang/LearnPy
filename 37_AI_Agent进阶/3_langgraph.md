# 3. LangGraph框架

## 什么是LangGraph

LangGraph是LangChain团队推出的图结构工作流框架，专门用于构建复杂的Agent工作流。它用"图"来描述流程：节点是执行步骤，边是流转规则。

## 为什么用LangGraph

| 对比 | LangChain Agent | LangGraph |
|------|-----------------|-----------|
| 流程控制 | LLM自主决策 | 开发者定义图结构 |
| 循环支持 | 有限 | 原生支持 |
| 条件分支 | 有限 | 灵活的条件边 |
| 状态管理 | 简单 | 完整的状态系统 |
| 可视化 | 无 | 支持图可视化 |
| 适用场景 | 简单Agent | 复杂多步骤工作流 |

## 四个核心概念

### 1. State（状态）
所有节点共享的数据结构，用TypedDict定义：
```python
class MyState(TypedDict):
    messages: list
    result: str
```

### 2. Node（节点）
执行单元，接收State、返回更新后的State：
```python
def my_node(state: MyState) -> dict:
    return {"result": "处理完成"}
```

### 3. Edge（边）
节点之间的连接关系：
- **普通边** — A → B，无条件流转
- **条件边** — A → (条件判断) → B 或 C

### 4. Graph（图）
由节点和边组成的完整工作流，编译后可执行。

## 基本使用流程

```
1. 定义State（TypedDict）
2. 编写Node函数
3. 创建StateGraph
4. 添加节点和边
5. 设置入口点
6. 编译图
7. 调用invoke执行
```

## 条件边

根据状态动态选择下一个节点：
```python
workflow.add_conditional_edges(
    "当前节点",
    判断函数,
    {"条件A": "节点A", "条件B": "节点B"}
)
```

## 循环

LangGraph原生支持循环——条件边指回之前的节点即可。常用于"生成→检查→不满意→重新生成"的迭代模式。

## 状态持久化

支持将状态保存到外部存储，实现：
- 长时间运行的工作流可中断恢复
- 同一会话的多次调用共享状态
- 常用：`MemorySaver`（内存）、`SqliteSaver`（SQLite）

## 人类介入（Human-in-the-Loop）

在关键节点暂停，等待人类审核或输入：
- 审批节点：人类决定是否继续
- 反馈节点：人类提供修改意见
- 配合`interrupt_before`或`interrupt_after`使用

## 流式输出

支持逐步输出中间结果：
```python
for chunk in graph.stream({"task": "..."}):
    print(chunk)
```

## 最佳实践

1. State只保留必要字段，避免膨胀
2. 每个Node职责单一，输入输出清晰
3. 条件边的判断逻辑要简单明确
4. 设置最大迭代次数防止死循环
5. 节点内做好try-except错误处理
