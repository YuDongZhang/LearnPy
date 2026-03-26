# 5. Prompt工程实战

## 项目：构建一个智能代码审查助手

### 功能
- 接收Python代码
- 从多个维度审查（安全性、性能、可读性、最佳实践）
- 输出结构化的审查报告（JSON格式）
- 支持多轮对话追问

### 技术要点
- System Prompt设计（角色+规则+输出格式）
- Few-shot示例引导输出格式
- JSON结构化输出 + Pydantic校验
- 多维度评分

### 运行方式
```bash
python 5_prompt_project.py
```

### 输出示例
```json
{
  "overall_score": 7,
  "issues": [
    {"severity": "high", "category": "security", "description": "SQL注入风险", "suggestion": "使用参数化查询"}
  ],
  "summary": "代码功能正确，但存在安全隐患"
}
```
