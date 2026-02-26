"""
MCP服务器开发
==============

本文件详细介绍如何开发MCP服务器，包括：
- 服务器基础结构
- 工具定义与实现
- 资源管理
- 提示模板
- 错误处理
"""

import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# 第一部分：MCP服务器基础
# ============================================================================

class MCPServerBase:
    """MCP服务器基类"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict] = {}
        self.resources: Dict[str, Dict] = {}
        self.prompts: Dict[str, Dict] = {}
        self.handlers: Dict[str, Callable] = {}
    
    def register_tool(self, name: str, description: str, 
                      input_schema: Dict, handler: Callable) -> None:
        """注册工具"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema
        }
        self.handlers[name] = handler
        print(f"✓ 工具已注册: {name}")
    
    def register_resource(self, uri: str, name: str, 
                         mime_type: str, handler: Callable) -> None:
        """注册资源"""
        self.resources[uri] = {
            "uri": uri,
            "name": name,
            "mimeType": mime_type
        }
        self.handlers[uri] = handler
        print(f"✓ 资源已注册: {uri}")
    
    def register_prompt(self, name: str, description: str,
                       arguments: List[Dict], handler: Callable) -> None:
        """注册提示模板"""
        self.prompts[name] = {
            "name": name,
            "description": description,
            "arguments": arguments
        }
        self.handlers[name] = handler
        print(f"✓ 提示模板已注册: {name}")
    
    def call_tool(self, name: str, arguments: Dict) -> Any:
        """调用工具"""
        if name not in self.handlers:
            raise ValueError(f"未知工具: {name}")
        return self.handlers[name](arguments)
    
    def get_resource(self, uri: str) -> Any:
        """获取资源"""
        if uri not in self.handlers:
            raise ValueError(f"未知资源: {uri}")
        return self.handlers[uri]()
    
    def get_prompt(self, name: str, arguments: Dict) -> Any:
        """获取提示模板"""
        if name not in self.handlers:
            raise ValueError(f"未知提示模板: {name}")
        return self.handlers[name](arguments)


# ============================================================================
# 第二部分：工具定义与实现
# ============================================================================

def create_math_tools(server: MCPServerBase):
    """创建数学计算工具"""
    
    # 加法工具
    def add_handler(args: Dict) -> Dict:
        a = args.get("a", 0)
        b = args.get("b", 0)
        result = a + b
        return {
            "content": [{"type": "text", "text": f"{a} + {b} = {result}"}],
            "isError": False
        }
    
    server.register_tool(
        name="add",
        description="计算两个数的和",
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "第一个数"},
                "b": {"type": "number", "description": "第二个数"}
            },
            "required": ["a", "b"]
        },
        handler=add_handler
    )
    
    # 乘法工具
    def multiply_handler(args: Dict) -> Dict:
        a = args.get("a", 0)
        b = args.get("b", 0)
        result = a * b
        return {
            "content": [{"type": "text", "text": f"{a} × {b} = {result}"}],
            "isError": False
        }
    
    server.register_tool(
        name="multiply",
        description="计算两个数的乘积",
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "第一个数"},
                "b": {"type": "number", "description": "第二个数"}
            },
            "required": ["a", "b"]
        },
        handler=multiply_handler
    )
    
    # 幂运算工具
    def power_handler(args: Dict) -> Dict:
        base = args.get("base", 0)
        exponent = args.get("exponent", 0)
        result = base ** exponent
        return {
            "content": [{"type": "text", "text": f"{base}^{exponent} = {result}"}],
            "isError": False
        }
    
    server.register_tool(
        name="power",
        description="计算幂运算",
        input_schema={
            "type": "object",
            "properties": {
                "base": {"type": "number", "description": "底数"},
                "exponent": {"type": "number", "description": "指数"}
            },
            "required": ["base", "exponent"]
        },
        handler=power_handler
    )


def create_string_tools(server: MCPServerBase):
    """创建字符串处理工具"""
    
    # 字符串反转
    def reverse_handler(args: Dict) -> Dict:
        text = args.get("text", "")
        result = text[::-1]
        return {
            "content": [{"type": "text", "text": f"反转结果: {result}"}],
            "isError": False
        }
    
    server.register_tool(
        name="reverse_string",
        description="反转字符串",
        input_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要反转的字符串"}
            },
            "required": ["text"]
        },
        handler=reverse_handler
    )
    
    # 统计单词数
    def word_count_handler(args: Dict) -> Dict:
        text = args.get("text", "")
        words = text.split()
        count = len(words)
        return {
            "content": [{"type": "text", "text": f"单词数: {count}"}],
            "isError": False
        }
    
    server.register_tool(
        name="word_count",
        description="统计文本中的单词数量",
        input_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要统计的文本"}
            },
            "required": ["text"]
        },
        handler=word_count_handler
    )
    
    # 文本格式化
    def format_handler(args: Dict) -> Dict:
        text = args.get("text", "")
        format_type = args.get("format_type", "upper")
        
        if format_type == "upper":
            result = text.upper()
        elif format_type == "lower":
            result = text.lower()
        elif format_type == "title":
            result = text.title()
        else:
            result = text
        
        return {
            "content": [{"type": "text", "text": f"格式化结果: {result}"}],
            "isError": False
        }
    
    server.register_tool(
        name="format_text",
        description="格式化文本（大写/小写/标题）",
        input_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要格式化的文本"},
                "format_type": {
                    "type": "string",
                    "enum": ["upper", "lower", "title"],
                    "description": "格式化类型"
                }
            },
            "required": ["text", "format_type"]
        },
        handler=format_handler
    )


# ============================================================================
# 第三部分：资源管理
# ============================================================================

def create_documentation_resources(server: MCPServerBase):
    """创建文档资源"""
    
    # API文档
    api_docs = """
# API 文档

## 数学运算 API

### add(a, b)
计算两个数的和。

**参数:**
- a: 第一个数
- b: 第二个数

**返回:** 两数之和

### multiply(a, b)
计算两个数的乘积。

**参数:**
- a: 第一个数
- b: 第二个数

**返回:** 两数之积

## 字符串处理 API

### reverse_string(text)
反转字符串。

**参数:**
- text: 要反转的字符串

**返回:** 反转后的字符串
"""
    
    def api_docs_handler() -> Dict:
        return {
            "contents": [{
                "uri": "docs://api",
                "mimeType": "text/markdown",
                "text": api_docs
            }]
        }
    
    server.register_resource(
        uri="docs://api",
        name="API文档",
        mime_type="text/markdown",
        handler=api_docs_handler
    )
    
    # 配置文件
    config = {
        "server": {
            "name": "示例MCP服务器",
            "version": "1.0.0"
        },
        "features": {
            "math_tools": True,
            "string_tools": True,
            "resources": True
        },
        "limits": {
            "max_request_size": 1048576,
            "timeout": 30
        }
    }
    
    def config_handler() -> Dict:
        return {
            "contents": [{
                "uri": "config://server",
                "mimeType": "application/json",
                "text": json.dumps(config, indent=2)
            }]
        }
    
    server.register_resource(
        uri="config://server",
        name="服务器配置",
        mime_type="application/json",
        handler=config_handler
    )


# ============================================================================
# 第四部分：提示模板
# ============================================================================

def create_prompt_templates(server: MCPServerBase):
    """创建提示模板"""
    
    # 代码审查模板
    def code_review_prompt(args: Dict) -> Dict:
        code = args.get("code", "")
        language = args.get("language", "python")
        
        prompt = f"""请审查以下{language}代码:

```{language}
{code}
```

请检查:
1. 代码风格和可读性
2. 潜在的错误或bug
3. 性能优化建议
4. 安全考虑
5. 最佳实践遵循情况

请提供详细的反馈。"""
        
        return {
            "description": f"代码审查: {language}",
            "messages": [{
                "role": "user",
                "content": {"type": "text", "text": prompt}
            }]
        }
    
    server.register_prompt(
        name="code_review",
        description="代码审查提示模板",
        arguments=[
            {
                "name": "code",
                "description": "要审查的代码",
                "required": True
            },
            {
                "name": "language",
                "description": "编程语言",
                "required": False
            }
        ],
        handler=code_review_prompt
    )
    
    # 文档生成模板
    def doc_gen_prompt(args: Dict) -> Dict:
        function_code = args.get("function_code", "")
        
        prompt = f"""请为以下函数生成文档字符串:

```python
{function_code}
```

请包含:
- 函数描述
- 参数说明
- 返回值说明
- 使用示例
- 异常说明（如果有）"""
        
        return {
            "description": "文档生成",
            "messages": [{
                "role": "user",
                "content": {"type": "text", "text": prompt}
            }]
        }
    
    server.register_prompt(
        name="generate_docs",
        description="生成函数文档",
        arguments=[
            {
                "name": "function_code",
                "description": "函数代码",
                "required": True
            }
        ],
        handler=doc_gen_prompt
    )


# ============================================================================
# 第五部分：错误处理
# ============================================================================

class MCPError(Exception):
    """MCP错误基类"""
    def __init__(self, code: int, message: str, data: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.data = data or {}
        super().__init__(message)


class ToolError(MCPError):
    """工具执行错误"""
    def __init__(self, message: str, tool_name: str = ""):
        super().__init__(-32603, message, {"tool": tool_name})


class ValidationError(MCPError):
    """参数验证错误"""
    def __init__(self, message: str, field: str = ""):
        super().__init__(-32602, message, {"field": field})


def safe_tool_call(tool_func: Callable, arguments: Dict) -> Dict:
    """安全地调用工具，处理错误"""
    try:
        result = tool_func(arguments)
        return result
    except ValidationError as e:
        return {
            "content": [{"type": "text", "text": f"参数错误: {e.message}"}],
            "isError": True,
            "errorCode": e.code
        }
    except ToolError as e:
        return {
            "content": [{"type": "text", "text": f"工具错误: {e.message}"}],
            "isError": True,
            "errorCode": e.code
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"执行错误: {str(e)}"}],
            "isError": True,
            "errorCode": -32603
        }


# ============================================================================
# 第六部分：完整服务器示例
# ============================================================================

def create_complete_server():
    """创建完整的MCP服务器"""
    
    print("=" * 60)
    print("创建MCP服务器")
    print("=" * 60)
    
    # 创建服务器实例
    server = MCPServerBase(name="完整示例服务器", version="1.0.0")
    
    # 注册工具
    print("\n1. 注册工具:")
    create_math_tools(server)
    create_string_tools(server)
    
    # 注册资源
    print("\n2. 注册资源:")
    create_documentation_resources(server)
    
    # 注册提示模板
    print("\n3. 注册提示模板:")
    create_prompt_templates(server)
    
    return server


def demonstrate_server(server: MCPServerBase):
    """演示服务器功能"""
    
    print("\n" + "=" * 60)
    print("演示服务器功能")
    print("=" * 60)
    
    # 演示工具调用
    print("\n1. 工具调用演示:")
    
    print("\n  a) 加法工具:")
    result = server.call_tool("add", {"a": 10, "b": 5})
    print(f"     输入: a=10, b=5")
    print(f"     输出: {result['content'][0]['text']}")
    
    print("\n  b) 字符串反转:")
    result = server.call_tool("reverse_string", {"text": "Hello MCP"})
    print(f"     输入: text='Hello MCP'")
    print(f"     输出: {result['content'][0]['text']}")
    
    print("\n  c) 文本格式化:")
    result = server.call_tool("format_text", {"text": "hello world", "format_type": "title"})
    print(f"     输入: text='hello world', format_type='title'")
    print(f"     输出: {result['content'][0]['text']}")
    
    # 演示资源获取
    print("\n2. 资源获取演示:")
    
    print("\n  a) API文档:")
    resource = server.get_resource("docs://api")
    text = resource['contents'][0]['text']
    print(f"     内容预览: {text[:100]}...")
    
    print("\n  b) 服务器配置:")
    resource = server.get_resource("config://server")
    config = json.loads(resource['contents'][0]['text'])
    print(f"     服务器名称: {config['server']['name']}")
    print(f"     功能: {list(config['features'].keys())}")
    
    # 演示提示模板
    print("\n3. 提示模板演示:")
    
    print("\n  a) 代码审查模板:")
    prompt = server.get_prompt("code_review", {
        "code": "def add(a, b): return a + b",
        "language": "python"
    })
    print(f"     描述: {prompt['description']}")
    print(f"     提示内容预览: {prompt['messages'][0]['content']['text'][:80]}...")


def demonstrate_error_handling():
    """演示错误处理"""
    
    print("\n" + "=" * 60)
    print("错误处理演示")
    print("=" * 60)
    
    # 创建带错误处理的工具
    def divide_handler(args: Dict) -> Dict:
        try:
            a = args.get("a", 0)
            b = args.get("b", 0)
            
            if b == 0:
                raise ValidationError("除数不能为零", "b")
            
            result = a / b
            return {
                "content": [{"type": "text", "text": f"{a} / {b} = {result}"}],
                "isError": False
            }
        except ValidationError as e:
            return {
                "content": [{"type": "text", "text": f"错误: {e.message}"}],
                "isError": True
            }
    
    server = MCPServerBase("错误处理演示")
    server.register_tool(
        name="divide",
        description="除法运算",
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            }
        },
        handler=divide_handler
    )
    
    print("\n1. 正常除法:")
    result = server.call_tool("divide", {"a": 10, "b": 2})
    print(f"   结果: {result['content'][0]['text']}")
    print(f"   是否错误: {result['isError']}")
    
    print("\n2. 除零错误:")
    result = server.call_tool("divide", {"a": 10, "b": 0})
    print(f"   结果: {result['content'][0]['text']}")
    print(f"   是否错误: {result['isError']}")
    
    print("\n3. 调用不存在的工具:")
    try:
        result = server.call_tool("nonexistent", {})
    except ValueError as e:
        print(f"   捕获错误: {e}")


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    # 创建完整服务器
    server = create_complete_server()
    
    # 演示服务器功能
    demonstrate_server(server)
    
    # 演示错误处理
    demonstrate_error_handling()
    
    # 总结
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print(f"""
MCP服务器开发要点:

1. 服务器结构
   - 使用MCPServerBase作为基类
   - 分别注册工具、资源和提示模板
   - 为每个功能提供处理器函数

2. 工具开发
   - 定义清晰的输入模式（JSON Schema）
   - 提供详细的描述信息
   - 返回标准化的结果格式

3. 资源管理
   - 使用URI标识资源
   - 指定正确的MIME类型
   - 支持动态内容生成

4. 提示模板
   - 定义参数结构
   - 提供默认参数值
   - 生成结构化的提示内容

5. 错误处理
   - 使用特定的错误类型
   - 提供有意义的错误信息
   - 在工具结果中标记错误状态

实际部署时，使用官方mcp库:
   pip install mcp
   
然后参考官方文档实现完整的服务器功能。
""")
