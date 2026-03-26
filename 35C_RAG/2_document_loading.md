# 2. 文档加载与切分

## 文档加载

LangChain提供了丰富的文档加载器：

| 格式 | 加载器 | 说明 |
|------|--------|------|
| TXT | TextLoader | 纯文本 |
| PDF | PyPDFLoader | PDF文件 |
| Word | Docx2txtLoader | Word文档 |
| Markdown | UnstructuredMarkdownLoader | Markdown |
| CSV | CSVLoader | CSV表格 |
| 网页 | WebBaseLoader | 网页内容 |
| 目录 | DirectoryLoader | 批量加载目录 |

## 文本切分

为什么要切分：
- LLM上下文窗口有限
- 小块文本检索更精准
- 避免无关信息干扰

### 切分策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| 固定大小 | 按字符数切分 | 通用 |
| 递归切分 | 按段落→句子→字符逐级切分 | 最常用 |
| 语义切分 | 按语义边界切分 | 高质量需求 |
| 按标题切分 | 按Markdown标题切分 | 结构化文档 |

### 关键参数

- `chunk_size`：每块的最大字符数（常用500-1000）
- `chunk_overlap`：相邻块的重叠字符数（常用50-200）

重叠的作用：避免切分时丢失跨块的上下文信息。

## 切分最佳实践

1. chunk_size不要太大（检索不精准）也不要太小（缺少上下文）
2. 保持适当的overlap（通常chunk_size的10-20%）
3. 结构化文档优先按标题切分
4. 切分后检查质量，确保每块内容完整有意义
