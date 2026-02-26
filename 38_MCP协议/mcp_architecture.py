"""
MCP架构详解
==========

详细介绍MCP的架构设计和核心组件。
"""

print("=" * 60)
print("1. MCP整体架构")
print("=" * 60)

print("架构图:")
print()
print("  +-------------------+     MCP Protocol      +-------------------+")
print("  |                   | <------------------> |                   |")
print("  |   MCP Client      |    JSON-RPC/SSE      |   MCP Server      |")
print("  |   (AI应用/Agent)  |                      |   (工具提供者)     |")
print("  |                   |                      |                   |")
print("  +-------------------+                      +-------------------+")
print("         |                                            |")
print("         |                                            |")
print("    调用工具                                    执行实际功能")
print("    读取资源                                    访问数据源")
print()
print("核心组件:")
print("  - Transport Layer: 传输层")
print("  - Protocol Layer: 协议层")
print("  - Application Layer: 应用层")

print()
print("=" * 60)
print("2. 传输层 (Transport)")
print("=" * 60)

print("2.1 stdio传输")
print("  - 标准输入输出")
print("  - 适用于本地进程")
print("  - 简单高效")
print()
print('''
# stdio传输示例
from mcp.server import Server
from mcp.server.stdio import stdio_server

async def main():
    server = Server("my-server")

    async with stdio_server(server) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )
''')

print()
print("2.2 SSE传输")
print("  - Server-Sent Events")
print("  - 适用于Web应用")
print("  - 支持HTTP")
print()
print('''
# SSE传输示例
from mcp.server.sse import SseServerTransport

app = Server("my-server")
transport = SseServerTransport("/messages")

@app.route("/sse")
async def sse_endpoint(request):
    async with transport.connect_sse(request) as streams:
        await app.run(*streams, app.create_initialization_options())
''')

print()
print("2.3 传输层职责")
print("  - 建立连接")
print("  - 消息序列化/反序列化")
print("  - 错误处理")
print("  - 连接管理")

print()
print("=" * 60)
print("3. 协议层 (Protocol)")
print("=" * 60)

print("3.1 JSON-RPC 2.0")
print("  - 基于JSON的RPC协议")
print("  - 请求-响应模式")
print("  - 支持通知")
print()
print("消息格式:")
print('''
# 请求
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}

# 响应
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "tools": [...]
    }
}

# 错误
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32600,
        "message": "Invalid Request"
    }
}
''')

print()
print("3.2 MCP方法")
print("| 方法 | 说明 | 方向 |")
print("|------|------|------|")
print("| initialize | 初始化连接 | Client->Server |")
print("| initialized | 初始化完成通知 | Server->Client |")
print("| tools/list | 列出可用工具 | Client->Server |")
print("| tools/call | 调用工具 | Client->Server |")
print("| resources/list | 列出资源 | Client->Server |")
print("| resources/read | 读取资源 | Client->Server |")
print("| prompts/list | 列出提示模板 | Client->Server |")
print("| prompts/get | 获取提示模板 | Client->Server |")
print("| notifications/* | 各种通知 | 双向 |")

print()
print("=" * 60)
print("4. 应用层 (Application)")
print("=" * 60)

print("4.1 服务器端")
print("  - 工具定义和实现")
print("  - 资源管理")
print("  - 提示模板")
print("  - 能力声明")
print()
print("4.2 客户端")
print("  - 服务器连接")
print("  - 工具发现")
print("  - 工具调用")
print("  - 资源读取")

print()
print("=" * 60)
print("5. 初始化流程")
print("=" * 60)

print("流程图:")
print()
print("  Client                    Server")
print("    |                          |")
print("    |---- 1. initialize ----->|")
print("    |    (协议版本、能力)       |")
print("    |                          |")
print("    |<--- 2. initialize ------|")
print("    |    (协议版本、能力)       |")
print("    |                          |")
print("    |---- 3. initialized ----->|")
print("    |    (确认通知)            |")
print("    |                          |")
print("    |---- 4. tools/list ----->|")
print("    |                          |")
print("    |<--- 5. tools/list ------|")
print("    |    (工具列表)            |")
print("    |                          |")
print()
print("初始化内容:")
print('''
# 客户端初始化参数
{
    "protocolVersion": "2024-11-05",
    "capabilities": {
        "sampling": {},
        "roots": {
            "listChanged": True
        }
    },
    "clientInfo": {
        "name": "my-client",
        "version": "1.0.0"
    }
}

# 服务器初始化响应
{
    "protocolVersion": "2024-11-05",
    "capabilities": {
        "logging": {},
        "prompts": {
            "listChanged": True
        },
        "resources": {
            "subscribe": True,
            "listChanged": True
        },
        "tools": {
            "listChanged": True
        }
    },
    "serverInfo": {
        "name": "my-server",
        "version": "1.0.0"
    }
}
''')

print()
print("=" * 60)
print("6. 工具系统")
print("=" * 60)

print("6.1 工具定义")
print('''
{
    "name": "calculate",
    "description": "Perform mathematical calculations",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate"
            }
        },
        "required": ["expression"]
    }
}
''')

print()
print("6.2 工具调用")
print('''
# 调用请求
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "calculate",
        "arguments": {
            "expression": "2 + 2"
        }
    }
}

# 调用响应
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "4"
            }
        ],
        "isError": false
    }
}
''')

print()
print("=" * 60)
print("7. 资源系统")
print("=" * 60)

print("7.1 资源定义")
print('''
{
    "uri": "file:///data/report.txt",
    "name": "Report File",
    "description": "Monthly sales report",
    "mimeType": "text/plain"
}
''')

print()
print("7.2 资源读取")
print('''
# 读取请求
{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "resources/read",
    "params": {
        "uri": "file:///data/report.txt"
    }
}

# 读取响应
{
    "jsonrpc": "2.0",
    "id": 3,
    "result": {
        "contents": [
            {
                "uri": "file:///data/report.txt",
                "mimeType": "text/plain",
                "text": "Sales: $10000"
            }
        ]
    }
}
''')

print()
print("=" * 60)
print("8. 提示模板系统")
print("=" * 60)

print("8.1 提示模板定义")
print('''
{
    "name": "code_review",
    "description": "Review code for best practices",
    "arguments": [
        {
            "name": "language",
            "description": "Programming language",
            "required": true
        },
        {
            "name": "code",
            "description": "Code to review",
            "required": true
        }
    ]
}
''')

print()
print("8.2 获取提示模板")
print('''
# 获取请求
{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "prompts/get",
    "params": {
        "name": "code_review",
        "arguments": {
            "language": "python",
            "code": "def hello(): print('Hello')"
        }
    }
}

# 获取响应
{
    "jsonrpc": "2.0",
    "id": 4,
    "result": {
        "description": "Code review prompt",
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "Please review this Python code..."
                }
            }
        ]
    }
}
''')

print()
print("=" * 60)
print("9. 通知机制")
print("=" * 60)

print("9.1 服务器通知")
print("| 通知 | 说明 |")
print("|------|------|")
print("| notifications/tools/list_changed | 工具列表变化 |")
print("| notifications/resources/list_changed | 资源列表变化 |")
print("| notifications/resources/updated | 资源更新 |")
print("| notifications/prompts/list_changed | 提示模板列表变化 |")
print("| notifications/message | 日志消息 |")
print()
print("9.2 客户端通知")
print("| 通知 | 说明 |")
print("|------|------|")
print("| notifications/roots/list_changed | 根目录变化 |")
print("| notifications/cancelled | 取消请求 |")

print()
print("=" * 60)
print("10. 错误处理")
print("=" * 60)

print("10.1 标准错误码")
print("| 错误码 | 说明 |")
print("|--------|------|")
print("| -32700 | Parse error |")
print("| -32600 | Invalid Request |")
print("| -32601 | Method not found |")
print("| -32602 | Invalid params |")
print("| -32603 | Internal error |")
print("| -32000 | Server error |")
print()
print("10.2 MCP特定错误")
print("| 错误码 | 说明 |")
print("|--------|------|")
print("| -32001 | Connection closed |")
print("| -32002 | Request timeout |")
print("| -32003 | Capability not supported |")

print()
print("=" * 60)
print("11. 安全模型")
print("=" * 60)

print("11.1 能力协商")
print("  - 客户端声明需要的能力")
print("  - 服务器声明支持的能力")
print("  - 只使用双方都支持的功能")
print()
print("11.2 权限控制")
print("  - 服务器控制资源访问")
print("  - 客户端控制采样请求")
print("  - 明确的权限边界")
print()
print("11.3 数据安全")
print("  - 敏感数据不传输")
print("  - URI引用而非内容")
print("  - 客户端主动读取")

print()
print("=" * 60)
print("12. 架构最佳实践")
print("=" * 60)

print("1. 服务器设计")
print("  - 单一职责")
print("  - 清晰的工具定义")
print("  - 完善的错误处理")
print("  - 合理的资源粒度")
print()
print("2. 客户端设计")
print("  - 优雅降级")
print("  - 连接重试")
print("  - 超时处理")
print("  - 资源缓存")
print()
print("3. 协议使用")
print("  - 正确的初始化顺序")
print("  - 及时响应通知")
print("  - 合理的并发控制")

print()
print("=" * 60)
print("13. 架构总结")
print("=" * 60)

print("MCP架构要点:")
print()
print("* 三层架构:")
print("  - 传输层: stdio/SSE/HTTP")
print("  - 协议层: JSON-RPC 2.0")
print("  - 应用层: 工具/资源/提示")
print()
print("* 核心流程:")
print("  - 初始化 -> 发现 -> 调用")
print()
print("* 关键机制:")
print("  - 能力协商、通知、错误处理")
print()
print("* 设计原则:")
print("  - 标准化、安全、可扩展")
