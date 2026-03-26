# 3. 结构化输出控制

## 为什么需要结构化输出

实际项目中，我们需要模型输出可解析的格式（JSON、列表、表格等），而不是自由文本。

## JSON输出

最常用的结构化输出方式：
```
请分析以下文本的情感，用JSON格式输出：
{"sentiment": "正面/负面/中性", "confidence": 0.0-1.0, "keywords": ["关键词"]}

文本：这个产品质量很好，物流也快
```

## 技巧：强制JSON输出

1. 在Prompt中明确要求JSON格式
2. 给出JSON Schema示例
3. 使用OpenAI的`response_format={"type": "json_object"}`
4. 用Pydantic做输出校验

## 列表/表格输出

```
列出Python的5个核心特性，用Markdown表格格式：
| 特性 | 说明 |
|------|------|
```

## 分步输出

```
请按以下步骤分析代码：
## 步骤1：功能描述
## 步骤2：潜在问题
## 步骤3：改进建议
```

## LangChain输出解析器

LangChain提供了多种OutputParser：
- `JsonOutputParser` — 解析JSON
- `PydanticOutputParser` — 用Pydantic模型校验
- `CommaSeparatedListOutputParser` — 解析逗号分隔列表
- `StructuredOutputParser` — 自定义结构

## 输出校验与重试

模型输出可能不符合格式要求，需要：
1. 解析输出
2. 校验格式
3. 失败则带错误信息重试
