"""
MCP客户端使用
==============

本文件详细介绍如何使用MCP客户端，包括：
- 客户端基础结构
- 连接管理
- 工具调用
- 资源访问
- 提示模板使用
"""

import json
import asyncio
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# 第一部分：MCP客户端基础
# ============================================================================

class MCPClient:
    """MCP客户端基类"""
    
    def __init__(self, name: str = "MCP客户端"):
        self.name = name
        self.connected = False
        self.server_info: Optional[Dict] = None
        self.available_tools: List[Dict] = []
        self.available_resources: List[Dict] = []
        self.available_prompts: List[Dict] = []
    
    async def connect(self, server_config: Dict) -> bool:
        """连接到MCP服务器"""
        print(f"连接到服务器: {server_config.get('name', 'Unknown')}")
        
        # 模拟连接过程
        await asyncio.sleep(0.1)
        
        self.connected = True
        self.server_info = {
            "name": server_config.get("name", "Unknown"),
            "version": server_config.get("version", "1.0.0"),
            "capabilities": server_config.get("capabilities", {})
        }
        
        print(f"✓ 连接成功: {self.server_info['name']} v{self.server_info['version']}")
        return True
    
    async def disconnect(self):
        """断开连接"""
        if self.connected:
            self.connected = False
            self.server_info = None
            print("✓ 已断开连接")
    
    async def initialize(self) -> Dict:
        """初始化会话"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        # 获取服务器能力
        capabilities = {
            "tools": {},
            "resources": {},
            "prompts": {}
        }
        
        print("✓ 会话已初始化")
        return capabilities
    
    async def list_tools(self) -> List[Dict]:
        """获取可用工具列表"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        return self.available_tools
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        """调用工具"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        raise NotImplementedError("需要在子类中实现")
    
    async def list_resources(self) -> List[Dict]:
        """获取可用资源列表"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        return self.available_resources
    
    async def read_resource(self, uri: str) -> Dict:
        """读取资源"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        raise NotImplementedError("需要在子类中实现")
    
    async def list_prompts(self) -> List[Dict]:
        """获取可用提示模板列表"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        return self.available_prompts
    
    async def get_prompt(self, name: str, arguments: Dict) -> Dict:
        """获取提示模板"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        raise NotImplementedError("需要在子类中实现")


# ============================================================================
# 第二部分：模拟MCP客户端实现
# ============================================================================

class MockMCPClient(MCPClient):
    """模拟MCP客户端（用于演示）"""
    
    def __init__(self, name: str = "模拟MCP客户端"):
        super().__init__(name)
        self.mock_tools: Dict[str, Callable] = {}
        self.mock_resources: Dict[str, Callable] = {}
        self.mock_prompts: Dict[str, Callable] = {}
    
    def register_mock_tool(self, name: str, schema: Dict, handler: Callable):
        """注册模拟工具"""
        self.mock_tools[name] = handler
        self.available_tools.append({
            "name": name,
            "description": schema.get("description", ""),
            "inputSchema": schema.get("inputSchema", {})
        })
    
    def register_mock_resource(self, uri: str, name: str, mime_type: str, handler: Callable):
        """注册模拟资源"""
        self.mock_resources[uri] = handler
        self.available_resources.append({
            "uri": uri,
            "name": name,
            "mimeType": mime_type
        })
    
    def register_mock_prompt(self, name: str, description: str, arguments: List[Dict], handler: Callable):
        """注册模拟提示模板"""
        self.mock_prompts[name] = handler
        self.available_prompts.append({
            "name": name,
            "description": description,
            "arguments": arguments
        })
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        """调用模拟工具"""
        if name not in self.mock_tools:
            raise ValueError(f"未知工具: {name}")
        
        print(f"  调用工具: {name}")
        print(f"  参数: {arguments}")
        
        result = self.mock_tools[name](arguments)
        return result
    
    async def read_resource(self, uri: str) -> Dict:
        """读取模拟资源"""
        if uri not in self.mock_resources:
            raise ValueError(f"未知资源: {uri}")
        
        print(f"  读取资源: {uri}")
        
        result = self.mock_resources[uri]()
        return result
    
    async def get_prompt(self, name: str, arguments: Dict) -> Dict:
        """获取模拟提示模板"""
        if name not in self.mock_prompts:
            raise ValueError(f"未知提示模板: {name}")
        
        print(f"  获取提示模板: {name}")
        print(f"  参数: {arguments}")
        
        result = self.mock_prompts[name](arguments)
        return result


# ============================================================================
# 第三部分：客户端使用模式
# ============================================================================

async def demonstrate_basic_usage():
    """演示基本使用模式"""
    
    print("=" * 60)
    print("MCP客户端基本使用")
    print("=" * 60)
    
    # 创建客户端
    client = MockMCPClient("演示客户端")
    
    # 注册模拟工具
    client.register_mock_tool(
        name="calculator",
        schema={
            "description": "计算器工具",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            }
        },
        handler=lambda args: {
            "content": [{"type": "text", "text": f"计算结果: {args['a']} {args['operation']} {args['b']}"}],
            "isError": False
        }
    )
    
    # 连接到服务器
    await client.connect({
        "name": "数学服务器",
        "version": "1.0.0",
        "capabilities": {"tools": True}
    })
    
    # 初始化
    await client.initialize()
    
    # 列出可用工具
    print("\n可用工具:")
    tools = await client.list_tools()
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # 调用工具
    print("\n调用工具:")
    result = await client.call_tool("calculator", {
        "operation": "add",
        "a": 10,
        "b": 5
    })
    print(f"  结果: {result['content'][0]['text']}")
    
    # 断开连接
    await client.disconnect()


async def demonstrate_resource_access():
    """演示资源访问"""
    
    print("\n" + "=" * 60)
    print("资源访问演示")
    print("=" * 60)
    
    client = MockMCPClient("资源客户端")
    
    # 注册模拟资源
    client.register_mock_resource(
        uri="docs://readme",
        name="README",
        mime_type="text/markdown",
        handler=lambda: {
            "contents": [{
                "uri": "docs://readme",
                "mimeType": "text/markdown",
                "text": "# 欢迎使用\n\n这是README文档。"
            }]
        }
    )
    
    client.register_mock_resource(
        uri="data://config.json",
        name="配置文件",
        mime_type="application/json",
        handler=lambda: {
            "contents": [{
                "uri": "data://config.json",
                "mimeType": "application/json",
                "text": json.dumps({"version": "1.0", "debug": True}, indent=2)
            }]
        }
    )
    
    # 连接
    await client.connect({
        "name": "资源服务器",
        "version": "1.0.0",
        "capabilities": {"resources": True}
    })
    
    # 列出资源
    print("\n可用资源:")
    resources = await client.list_resources()
    for resource in resources:
        print(f"  - {resource['uri']}: {resource['name']} ({resource['mimeType']})")
    
    # 读取资源
    print("\n读取资源:")
    
    print("\n  1. README文档:")
    result = await client.read_resource("docs://readme")
    content = result['contents'][0]
    print(f"     URI: {content['uri']}")
    print(f"     内容: {content['text'][:50]}...")
    
    print("\n  2. 配置文件:")
    result = await client.read_resource("data://config.json")
    content = result['contents'][0]
    config = json.loads(content['text'])
    print(f"     版本: {config['version']}")
    print(f"     调试模式: {config['debug']}")
    
    await client.disconnect()


async def demonstrate_prompt_usage():
    """演示提示模板使用"""
    
    print("\n" + "=" * 60)
    print("提示模板使用演示")
    print("=" * 60)
    
    client = MockMCPClient("提示客户端")
    
    # 注册模拟提示模板
    client.register_mock_prompt(
        name="code_review",
        description="代码审查",
        arguments=[
            {"name": "code", "description": "代码内容", "required": True},
            {"name": "language", "description": "编程语言", "required": False}
        ],
        handler=lambda args: {
            "description": f"代码审查: {args.get('language', 'unknown')}",
            "messages": [{
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"请审查以下{args.get('language', 'code')}代码:\n{args.get('code', '')}"
                }
            }]
        }
    )
    
    # 连接
    await client.connect({
        "name": "提示服务器",
        "version": "1.0.0",
        "capabilities": {"prompts": True}
    })
    
    # 列出提示模板
    print("\n可用提示模板:")
    prompts = await client.list_prompts()
    for prompt in prompts:
        print(f"  - {prompt['name']}: {prompt['description']}")
        print(f"    参数: {[arg['name'] for arg in prompt['arguments']]}")
    
    # 获取提示模板
    print("\n获取提示模板:")
    result = await client.get_prompt("code_review", {
        "code": "def hello(): print('world')",
        "language": "python"
    })
    print(f"  描述: {result['description']}")
    print(f"  消息内容: {result['messages'][0]['content']['text'][:60]}...")
    
    await client.disconnect()


# ============================================================================
# 第四部分：高级客户端模式
# ============================================================================

class AdvancedMCPClient(MCPClient):
    """高级MCP客户端"""
    
    def __init__(self, name: str = "高级MCP客户端"):
        super().__init__(name)
        self.tool_cache: Dict[str, Any] = {}
        self.resource_cache: Dict[str, Any] = {}
        self.request_history: List[Dict] = []
    
    async def call_tool_with_cache(self, name: str, arguments: Dict, 
                                   use_cache: bool = True) -> Dict:
        """带缓存的工具调用"""
        cache_key = f"{name}:{json.dumps(arguments, sort_keys=True)}"
        
        if use_cache and cache_key in self.tool_cache:
            print(f"  [缓存命中] {name}")
            return self.tool_cache[cache_key]
        
        result = await self.call_tool(name, arguments)
        
        if use_cache:
            self.tool_cache[cache_key] = result
        
        return result
    
    async def batch_call_tools(self, calls: List[Dict]) -> List[Dict]:
        """批量调用工具"""
        print(f"批量调用 {len(calls)} 个工具...")
        
        results = []
        for call in calls:
            try:
                result = await self.call_tool(call["name"], call["arguments"])
                results.append({"success": True, "result": result})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return results
    
    def get_request_history(self) -> List[Dict]:
        """获取请求历史"""
        return self.request_history
    
    def clear_cache(self):
        """清除缓存"""
        self.tool_cache.clear()
        self.resource_cache.clear()
        print("✓ 缓存已清除")


async def demonstrate_advanced_patterns():
    """演示高级使用模式"""
    
    print("\n" + "=" * 60)
    print("高级客户端模式")
    print("=" * 60)
    
    # 创建高级客户端
    client = AdvancedMCPClient("高级客户端")
    
    # 注册工具
    call_count = 0
    def expensive_operation(args: Dict) -> Dict:
        nonlocal call_count
        call_count += 1
        print(f"    [实际执行] 第 {call_count} 次调用")
        return {
            "content": [{"type": "text", "text": f"结果: {args['input']} * 2 = {args['input'] * 2}"}],
            "isError": False
        }
    
    # 使用MockMCPClient的方式注册工具
    client.__class__ = type('AdvancedMockClient', (AdvancedMCPClient, MockMCPClient), {})
    client.mock_tools = {}
    client.mock_resources = {}
    client.mock_prompts = {}
    
    # 手动添加模拟工具
    client.available_tools.append({
        "name": "double",
        "description": "将输入翻倍",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input": {"type": "number"}
            }
        }
    })
    client.mock_tools["double"] = expensive_operation
    
    # 覆盖call_tool方法
    async def mock_call_tool(name: str, arguments: Dict) -> Dict:
        if name not in client.mock_tools:
            raise ValueError(f"未知工具: {name}")
        return client.mock_tools[name](arguments)
    
    client.call_tool = mock_call_tool
    
    await client.connect({"name": "高级服务器", "version": "1.0.0"})
    
    # 演示缓存
    print("\n1. 缓存演示:")
    print("  第一次调用 (无缓存):")
    result1 = await client.call_tool_with_cache("double", {"input": 5}, use_cache=True)
    print(f"    结果: {result1['content'][0]['text']}")
    
    print("\n  第二次调用 (相同参数，使用缓存):")
    result2 = await client.call_tool_with_cache("double", {"input": 5}, use_cache=True)
    print(f"    结果: {result2['content'][0]['text']}")
    
    print("\n  第三次调用 (不同参数):")
    result3 = await client.call_tool_with_cache("double", {"input": 10}, use_cache=True)
    print(f"    结果: {result3['content'][0]['text']}")
    
    print(f"\n  总调用次数: {call_count} (缓存减少了实际调用)")
    
    # 演示批量调用
    print("\n2. 批量调用演示:")
    batch_calls = [
        {"name": "double", "arguments": {"input": 1}},
        {"name": "double", "arguments": {"input": 2}},
        {"name": "double", "arguments": {"input": 3}}
    ]
    
    results = await client.batch_call_tools(batch_calls)
    for i, result in enumerate(results):
        if result["success"]:
            text = result["result"]["content"][0]["text"]
            print(f"  调用 {i+1}: {text}")
    
    await client.disconnect()


# ============================================================================
# 第五部分：错误处理和重试
# ============================================================================

class RetryableMCPClient(MCPClient):
    """支持重试的MCP客户端"""
    
    def __init__(self, name: str = "重试客户端", max_retries: int = 3, 
                 retry_delay: float = 1.0):
        super().__init__(name)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def call_tool_with_retry(self, name: str, arguments: Dict) -> Dict:
        """带重试的工具调用"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                print(f"  尝试 {attempt + 1}/{self.max_retries}...")
                result = await self.call_tool(name, arguments)
                
                if not result.get("isError", False):
                    if attempt > 0:
                        print(f"  ✓ 在第 {attempt + 1} 次尝试成功")
                    return result
                
                last_error = result.get("content", [{}])[0].get("text", "Unknown error")
                
            except Exception as e:
                last_error = str(e)
            
            if attempt < self.max_retries - 1:
                print(f"  等待 {self.retry_delay} 秒后重试...")
                await asyncio.sleep(self.retry_delay)
        
        return {
            "content": [{"type": "text", "text": f"重试耗尽: {last_error}"}],
            "isError": True
        }


async def demonstrate_error_handling():
    """演示错误处理"""
    
    print("\n" + "=" * 60)
    print("错误处理和重试")
    print("=" * 60)
    
    client = RetryableMCPClient(max_retries=3, retry_delay=0.5)
    
    # 模拟一个会失败的工具
    fail_count = 0
    def flaky_tool(args: Dict) -> Dict:
        nonlocal fail_count
        fail_count += 1
        
        if fail_count < 3:
            return {
                "content": [{"type": "text", "text": f"临时错误 (尝试 {fail_count})"}],
                "isError": True
            }
        
        return {
            "content": [{"type": "text", "text": "成功!"}],
            "isError": False
        }
    
    # 设置模拟
    client.__class__ = type('RetryableMockClient', (RetryableMCPClient, MockMCPClient), {})
    client.mock_tools = {"flaky": flaky_tool}
    
    async def mock_call_tool(name: str, arguments: Dict) -> Dict:
        return client.mock_tools[name](arguments)
    
    client.call_tool = mock_call_tool
    
    await client.connect({"name": "不稳定服务器", "version": "1.0.0"})
    
    print("\n调用不稳定工具 (带重试):")
    result = await client.call_tool_with_retry("flaky", {})
    print(f"最终结果: {result['content'][0]['text']}")
    print(f"总尝试次数: {fail_count}")
    
    await client.disconnect()


# ============================================================================
# 主程序
# ============================================================================

async def main():
    """主函数"""
    
    print("MCP客户端使用示例")
    print("=" * 60)
    
    # 基本使用
    await demonstrate_basic_usage()
    
    # 资源访问
    await demonstrate_resource_access()
    
    # 提示模板
    await demonstrate_prompt_usage()
    
    # 高级模式
    await demonstrate_advanced_patterns()
    
    # 错误处理
    await demonstrate_error_handling()
    
    # 总结
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
MCP客户端使用要点:

1. 基本流程
   - 创建客户端实例
   - 连接到服务器
   - 初始化会话
   - 使用功能（工具/资源/提示）
   - 断开连接

2. 工具调用
   - 先列出可用工具
   - 准备正确的参数
   - 处理返回结果
   - 检查错误状态

3. 资源访问
   - 使用URI标识资源
   - 注意MIME类型
   - 处理二进制内容

4. 提示模板
   - 提供必需的参数
   - 获取结构化的提示
   - 用于LLM交互

5. 最佳实践
   - 使用连接池管理连接
   - 实现缓存减少调用
   - 添加重试机制
   - 记录请求历史
   - 妥善处理错误

实际使用时，使用官方mcp库:
   pip install mcp
   
然后使用mcp.Client类连接真实服务器。
""")


if __name__ == "__main__":
    asyncio.run(main())
