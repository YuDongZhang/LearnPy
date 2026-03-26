# 第2节：Skill的基本结构

本节详细介绍Skill的组成部分，帮助你理解如何定义一个完整的Skill。

---

## Skill的组成部分

一个完整的Skill由以下部分组成：

```
┌─────────────────────────────────────────────┐
│              Skill结构                       │
├─────────────────────────────────────────────┤
│  1. name          - 唯一标识                 │
│  2. description   - 用途描述                 │
│  3. parameters    - 输入参数                │
│  4. output        - 输出格式                │
│  5. examples      - 使用示例                │
└─────────────────────────────────────────────┘
```

---

## 字段说明

### 1. name（名称）
- 唯一标识这个Skill
- 推荐使用：小写字母 + 下划线
- 示例：`code_review`, `document_generator`

### 2. description（描述）
- 告诉AI这个Skill能做什么
- 要清晰、简洁
- 示例："审查代码质量和安全问题"

### 3. parameters（参数）
Skill需要的输入参数：

| 字段 | 说明 | 必需 |
|------|------|------|
| name | 参数名 | 是 |
| type | 类型 (string, number, boolean, object) | 是 |
| description | 参数说明 | 是 |
| required | 是否必需 | 是 |
| default | 默认值 | 否 |

### 4. output（输出）
Skill返回什么：

| 字段 | 说明 |
|------|------|
| type | 返回类型 |
| description | 返回说明 |
| schema | 返回结构 |

### 5. examples（示例）
- 展示如何使用
- 帮助AI正确调用

---

## 示例：代码审查Skill

```yaml
# Skill定义示例
name: "code_review"
description: "审查代码质量和安全问题，发现潜在的bug和性能问题"

parameters:
  - name: code
    type: string
    description: "要审查的代码"
    required: true
  
  - name: language
    type: string
    description: "编程语言，如 python, javascript"
    required: false
    default: "python"
  
  - name: strictness
    type: string
    description: "审查严格程度"
    required: false
    default: "normal"
    enum: ["strict", "normal", "lenient"]

output:
  type: object
  description: "审查结果"
  schema:
    score: number        # 0-100的评分
    issues: array        # 发现的问题列表
    suggestions: array   # 改进建议

examples:
  - input: "def add(a, b): return a + b"
    output: "{score: 90, issues: [], suggestions: []}"
```

---

## 总结

| 组成部分 | 作用 |
|----------|------|
| name | 唯一标识 |
| description | 说明用途 |
| parameters | 定义输入 |
| output | 定义输出 |
| examples | 提供示例 |

---

## 下一节

[第3节：编写第一个简单Skill](skill_03_first_skill.md)
