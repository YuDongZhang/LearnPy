"""
MCP实战项目
============

本项目实现一个完整的MCP应用：智能代码助手
包含：
- MCP服务器：提供代码分析和文档生成工具
- MCP客户端：集成到IDE或编辑器
- 实际应用场景演示
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

# ============================================================================
# 第一部分：代码分析工具
# ============================================================================

@dataclass
class CodeAnalysisResult:
    """代码分析结果"""
    language: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    functions: List[Dict] = field(default_factory=list)
    classes: List[Dict] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    complexity_score: float = 0.0
    issues: List[Dict] = field(default_factory=list)


class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        self.language_patterns = {
            "python": {
                "extension": ".py",
                "comment": r"#.*$",
                "docstring": r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')',
                "function": r"^def\s+(\w+)\s*\(",
                "class": r"^class\s+(\w+)",
                "import": r"^(?:import|from)\s+(\w+)"
            },
            "javascript": {
                "extension": ".js",
                "comment": r"//.*$",
                "docstring": r"/\*[\s\S]*?\*/",
                "function": r"(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(",
                "class": r"class\s+(\w+)",
                "import": r"(?:import|require)\s*\(?['\"]([^'\"]+)"
            }
        }
    
    def detect_language(self, code: str, filename: str = "") -> str:
        """检测编程语言"""
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            for lang, patterns in self.language_patterns.items():
                if patterns["extension"] == ext:
                    return lang
        
        # 通过代码特征检测
        if "def " in code and ":" in code:
            return "python"
        elif "function" in code or "const " in code or "let " in code:
            return "javascript"
        
        return "unknown"
    
    def analyze(self, code: str, filename: str = "") -> CodeAnalysisResult:
        """分析代码"""
        language = self.detect_language(code, filename)
        lines = code.split("\n")
        
        result = CodeAnalysisResult(
            language=language,
            total_lines=len(lines),
            code_lines=0,
            comment_lines=0,
            blank_lines=0
        )
        
        if language == "unknown":
            return result
        
        patterns = self.language_patterns[language]
        in_multiline_comment = False
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # 空行
            if not stripped:
                result.blank_lines += 1
                continue
            
            # 多行注释检测
            if language == "python":
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if stripped.count('"""') < 2 and stripped.count("'''") < 2:
                        in_multiline_comment = not in_multiline_comment
                    result.comment_lines += 1
                    continue
            
            if in_multiline_comment:
                result.comment_lines += 1
                continue
            
            # 单行注释
            if re.match(patterns["comment"], stripped):
                result.comment_lines += 1
                continue
            
            # 代码行
            result.code_lines += 1
            
            # 检测函数
            func_match = re.match(patterns["function"], stripped)
            if func_match:
                func_name = func_match.group(1) or func_match.group(2) if func_match.lastindex >= 2 else func_match.group(1)
                if func_name:
                    result.functions.append({
                        "name": func_name,
                        "line": i,
                        "signature": stripped[:50]
                    })
            
            # 检测类
            class_match = re.match(patterns["class"], stripped)
            if class_match:
                result.classes.append({
                    "name": class_match.group(1),
                    "line": i
                })
            
            # 检测导入
            import_match = re.match(patterns["import"], stripped)
            if import_match:
                result.imports.append(import_match.group(1))
        
        # 计算复杂度分数
        result.complexity_score = self._calculate_complexity(result)
        
        # 检测问题
        result.issues = self._detect_issues(code, language)
        
        return result
    
    def _calculate_complexity(self, result: CodeAnalysisResult) -> float:
        """计算代码复杂度分数"""
        score = 0.0
        
        # 基于函数数量
        score += len(result.functions) * 2
        
        # 基于类数量
        score += len(result.classes) * 3
        
        # 基于代码行数
        score += result.code_lines / 50
        
        # 基于导入数量
        score += len(result.imports) * 0.5
        
        return round(score, 2)
    
    def _detect_issues(self, code: str, language: str) -> List[Dict]:
        """检测代码问题"""
        issues = []
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # 行长度检查
            if len(line) > 100:
                issues.append({
                    "line": i,
                    "type": "style",
                    "severity": "warning",
                    "message": "行长度超过100字符"
                })
            
            # Python特定检查
            if language == "python":
                # 检查未使用的导入（简化检查）
                if stripped.startswith("import ") or stripped.startswith("from "):
                    module = stripped.split()[1].split(".")[0]
                    # 简化：假设如果导入后没有使用就是问题
                    # 实际实现需要更复杂的分析
                
                # 检查裸except
                if re.match(r"^except\s*:", stripped):
                    issues.append({
                        "line": i,
                        "type": "error",
                        "severity": "error",
                        "message": "使用裸except，建议捕获具体异常"
                    })
        
        return issues


# ============================================================================
# 第二部分：MCP代码助手服务器
# ============================================================================

class CodeAssistantServer:
    """代码助手MCP服务器"""
    
    def __init__(self):
        self.name = "code-assistant"
        self.version = "1.0.0"
        self.analyzer = CodeAnalyzer()
        self.tools = self._register_tools()
        self.resources = self._register_resources()
    
    def _register_tools(self) -> Dict[str, Dict]:
        """注册工具"""
        return {
            "analyze_code": {
                "name": "analyze_code",
                "description": "分析代码文件，返回代码统计、结构信息和潜在问题",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要分析的代码内容"
                        },
                        "filename": {
                            "type": "string",
                            "description": "文件名（用于语言检测）"
                        }
                    },
                    "required": ["code"]
                }
            },
            "generate_documentation": {
                "name": "generate_documentation",
                "description": "为代码生成文档字符串",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "函数或类的代码"
                        },
                        "style": {
                            "type": "string",
                            "enum": ["google", "numpy", "sphinx"],
                            "description": "文档风格"
                        }
                    },
                    "required": ["code"]
                }
            },
            "refactor_suggestions": {
                "name": "refactor_suggestions",
                "description": "提供代码重构建议",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要重构的代码"
                        }
                    },
                    "required": ["code"]
                }
            },
            "find_duplicates": {
                "name": "find_duplicates",
                "description": "查找代码中的重复片段",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要分析的代码"
                        },
                        "min_lines": {
                            "type": "integer",
                            "description": "最小重复行数",
                            "default": 5
                        }
                    },
                    "required": ["code"]
                }
            }
        }
    
    def _register_resources(self) -> Dict[str, Dict]:
        """注册资源"""
        return {
            "docs://style-guide": {
                "uri": "docs://style-guide",
                "name": "代码风格指南",
                "mimeType": "text/markdown"
            },
            "docs://best-practices": {
                "uri": "docs://best-practices",
                "name": "Python最佳实践",
                "mimeType": "text/markdown"
            }
        }
    
    def call_tool(self, name: str, arguments: Dict) -> Dict:
        """调用工具"""
        if name == "analyze_code":
            return self._analyze_code_tool(arguments)
        elif name == "generate_documentation":
            return self._generate_docs_tool(arguments)
        elif name == "refactor_suggestions":
            return self._refactor_tool(arguments)
        elif name == "find_duplicates":
            return self._find_duplicates_tool(arguments)
        else:
            return {
                "content": [{"type": "text", "text": f"未知工具: {name}"}],
                "isError": True
            }
    
    def _analyze_code_tool(self, arguments: Dict) -> Dict:
        """代码分析工具实现"""
        code = arguments.get("code", "")
        filename = arguments.get("filename", "")
        
        result = self.analyzer.analyze(code, filename)
        
        report = f"""代码分析报告
{'=' * 50}

语言: {result.language}
总行数: {result.total_lines}
代码行数: {result.code_lines}
注释行数: {result.comment_lines}
空行数: {result.blank_lines}
复杂度分数: {result.complexity_score}

结构信息:
- 函数数量: {len(result.functions)}
- 类数量: {len(result.classes)}
- 导入数量: {len(result.imports)}
"""
        
        if result.functions:
            report += "\n函数列表:\n"
            for func in result.functions:
                report += f"  - {func['name']} (第{func['line']}行)\n"
        
        if result.classes:
            report += "\n类列表:\n"
            for cls in result.classes:
                report += f"  - {cls['name']} (第{cls['line']}行)\n"
        
        if result.issues:
            report += f"\n发现 {len(result.issues)} 个问题:\n"
            for issue in result.issues:
                report += f"  [{issue['severity'].upper()}] 第{issue['line']}行: {issue['message']}\n"
        else:
            report += "\n✓ 未发现明显问题\n"
        
        return {
            "content": [{"type": "text", "text": report}],
            "isError": False
        }
    
    def _generate_docs_tool(self, arguments: Dict) -> Dict:
        """文档生成工具实现"""
        code = arguments.get("code", "")
        style = arguments.get("style", "google")
        
        # 解析函数信息
        func_match = re.search(r"def\s+(\w+)\s*\(([^)]*)\)", code)
        if not func_match:
            return {
                "content": [{"type": "text", "text": "无法解析函数定义"}],
                "isError": True
            }
        
        func_name = func_match.group(1)
        params_str = func_match.group(2)
        
        # 解析参数
        params = []
        if params_str.strip():
            for param in params_str.split(","):
                param = param.strip()
                if param and param != "self":
                    params.append(param.split(":")[0].split("=")[0].strip())
        
        # 生成文档
        if style == "google":
            doc = f'    """{func_name}函数的描述。\n\n'
            if params:
                doc += "    Args:\n"
                for param in params:
                    doc += f"        {param}: 参数描述\n"
                doc += "\n"
            doc += "    Returns:\n        返回值描述\n"
            doc += '    """'
        elif style == "numpy":
            doc = f'    """{func_name}函数的描述。\n\n'
            if params:
                doc += "    Parameters\n"
                doc += "    ----------\n"
                for param in params:
                    doc += f"    {param} : type\n        参数描述\n"
                doc += "\n"
            doc += "    Returns\n"
            doc += "    -------\n"
            doc += "    type\n        返回值描述\n"
            doc += '    """'
        else:  # sphinx
            doc = f'    """{func_name}函数的描述。"""\n'
            for param in params:
                doc += f"    :param {param}: 参数描述\n"
            doc += "    :return: 返回值描述"
        
        return {
            "content": [{"type": "text", "text": f"生成的文档:\n\n{doc}"}],
            "isError": False
        }
    
    def _refactor_tool(self, arguments: Dict) -> Dict:
        """重构建议工具实现"""
        code = arguments.get("code", "")
        
        suggestions = []
        lines = code.split("\n")
        
        # 检查长函数
        func_start = None
        for i, line in enumerate(lines):
            if re.match(r"^def\s+\w+", line.strip()):
                if func_start is not None:
                    func_length = i - func_start
                    if func_length > 30:
                        suggestions.append(f"第{func_start+1}行的函数过长({func_length}行)，建议拆分")
                func_start = i
        
        # 检查魔法数字
        magic_numbers = re.findall(r"[^\w](\d{2,})[^\w]", code)
        if magic_numbers:
            suggestions.append(f"发现魔法数字: {set(magic_numbers)}，建议使用常量替代")
        
        # 检查嵌套深度
        max_indent = max(len(line) - len(line.lstrip()) for line in lines if line.strip())
        if max_indent > 16:
            suggestions.append(f"代码嵌套过深(最大缩进{max_indent}空格)，建议简化逻辑")
        
        if suggestions:
            report = "重构建议:\n\n"
            for i, suggestion in enumerate(suggestions, 1):
                report += f"{i}. {suggestion}\n"
        else:
            report = "✓ 代码结构良好，暂无重构建议"
        
        return {
            "content": [{"type": "text", "text": report}],
            "isError": False
        }
    
    def _find_duplicates_tool(self, arguments: Dict) -> Dict:
        """查找重复代码工具实现"""
        code = arguments.get("code", "")
        min_lines = arguments.get("min_lines", 5)
        
        lines = code.split("\n")
        duplicates = []
        
        # 简单的重复检测算法
        for i in range(len(lines) - min_lines + 1):
            block = "\n".join(lines[i:i + min_lines])
            block_normalized = re.sub(r'\s+', ' ', block.strip())
            
            for j in range(i + min_lines, len(lines) - min_lines + 1):
                other_block = "\n".join(lines[j:j + min_lines])
                other_normalized = re.sub(r'\s+', ' ', other_block.strip())
                
                if block_normalized == other_normalized and len(block_normalized) > 20:
                    duplicates.append({
                        "block": block[:100] + "..." if len(block) > 100 else block,
                        "line1": i + 1,
                        "line2": j + 1
                    })
        
        if duplicates:
            report = f"发现 {len(duplicates)} 处重复代码:\n\n"
            for dup in duplicates[:5]:  # 只显示前5个
                report += f"第{dup['line1']}行 和 第{dup['line2']}行:\n"
                report += f"{dup['block']}\n\n"
        else:
            report = "✓ 未发现明显重复代码"
        
        return {
            "content": [{"type": "text", "text": report}],
            "isError": False
        }


# ============================================================================
# 第三部分：MCP客户端集成
# ============================================================================

class CodeAssistantClient:
    """代码助手客户端"""
    
    def __init__(self):
        self.server = CodeAssistantServer()
        self.history: List[Dict] = []
    
    async def analyze_file(self, filepath: str) -> str:
        """分析文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            filename = os.path.basename(filepath)
            
            result = self.server.call_tool("analyze_code", {
                "code": code,
                "filename": filename
            })
            
            self.history.append({
                "action": "analyze",
                "file": filepath,
                "timestamp": datetime.now().isoformat()
            })
            
            return result["content"][0]["text"]
            
        except Exception as e:
            return f"错误: {str(e)}"
    
    async def generate_docs(self, code: str, style: str = "google") -> str:
        """生成文档"""
        result = self.server.call_tool("generate_documentation", {
            "code": code,
            "style": style
        })
        
        self.history.append({
            "action": "generate_docs",
            "style": style,
            "timestamp": datetime.now().isoformat()
        })
        
        return result["content"][0]["text"]
    
    async def get_refactor_suggestions(self, code: str) -> str:
        """获取重构建议"""
        result = self.server.call_tool("refactor_suggestions", {
            "code": code
        })
        
        self.history.append({
            "action": "refactor",
            "timestamp": datetime.now().isoformat()
        })
        
        return result["content"][0]["text"]
    
    def get_history(self) -> List[Dict]:
        """获取操作历史"""
        return self.history


# ============================================================================
# 第四部分：演示
# ============================================================================

async def demonstrate_code_analysis():
    """演示代码分析"""
    
    print("=" * 60)
    print("代码分析演示")
    print("=" * 60)
    
    # 示例代码
    sample_code = '''
import os
import sys
from typing import List, Dict

def calculate_sum(numbers: List[int]) -> int:
    """Calculate the sum of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total

def calculate_average(numbers: List[int]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

class DataProcessor:
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def process(self) -> List[Dict]:
        results = []
        for item in self.data:
            processed = {
                "id": item.get("id"),
                "value": item.get("value", 0) * 2
            }
            results.append(processed)
        return results

# Main execution
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    print(calculate_sum(numbers))
    print(calculate_average(numbers))
'''
    
    client = CodeAssistantClient()
    
    print("\n1. 分析代码结构:")
    print("-" * 40)
    # 直接调用服务器
    result = client.server.call_tool("analyze_code", {
        "code": sample_code,
        "filename": "example.py"
    })
    print(result["content"][0]["text"])


async def demonstrate_documentation_generation():
    """演示文档生成"""
    
    print("\n" + "=" * 60)
    print("文档生成演示")
    print("=" * 60)
    
    sample_function = '''
def process_user_data(users: List[Dict], options: Dict = None) -> Dict:
    if options is None:
        options = {}
    
    results = {
        "total": len(users),
        "processed": 0,
        "failed": 0
    }
    
    for user in users:
        try:
            # Process user
            results["processed"] += 1
        except Exception:
            results["failed"] += 1
    
    return results
'''
    
    client = CodeAssistantClient()
    
    print("\n1. Google风格文档:")
    print("-" * 40)
    result = client.server.call_tool("generate_documentation", {
        "code": sample_function,
        "style": "google"
    })
    print(result["content"][0]["text"])
    
    print("\n2. NumPy风格文档:")
    print("-" * 40)
    result = client.server.call_tool("generate_documentation", {
        "code": sample_function,
        "style": "numpy"
    })
    print(result["content"][0]["text"])


async def demonstrate_refactoring():
    """演示重构建议"""
    
    print("\n" + "=" * 60)
    print("重构建议演示")
    print("=" * 60)
    
    code_with_issues = '''
def complex_function(data):
    result = []
    for item in data:
        if item > 0:
            if item % 2 == 0:
                if item > 100:
                    result.append(item * 2)
                else:
                    result.append(item * 3)
            else:
                if item > 50:
                    result.append(item * 4)
                else:
                    result.append(item * 5)
        else:
            result.append(0)
    return result

def another_function(x):
    if x > 10:
        if x > 20:
            if x > 30:
                if x > 40:
                    return 100
    return 0
'''
    
    client = CodeAssistantClient()
    
    print("\n重构建议:")
    print("-" * 40)
    result = client.server.call_tool("refactor_suggestions", {
        "code": code_with_issues
    })
    print(result["content"][0]["text"])


async def demonstrate_duplicate_detection():
    """演示重复代码检测"""
    
    print("\n" + "=" * 60)
    print("重复代码检测演示")
    print("=" * 60)
    
    code_with_duplicates = '''
def process_a(data):
    cleaned = []
    for item in data:
        if item is not None:
            if isinstance(item, str):
                cleaned.append(item.strip())
            else:
                cleaned.append(str(item))
    return cleaned

def process_b(items):
    cleaned = []
    for item in items:
        if item is not None:
            if isinstance(item, str):
                cleaned.append(item.strip())
            else:
                cleaned.append(str(item))
    return cleaned

def unique_function(x):
    return x * 2
'''
    
    client = CodeAssistantClient()
    
    print("\n重复代码检测结果:")
    print("-" * 40)
    result = client.server.call_tool("find_duplicates", {
        "code": code_with_duplicates,
        "min_lines": 5
    })
    print(result["content"][0]["text"])


# ============================================================================
# 主程序
# ============================================================================

async def main():
    """主函数"""
    
    print("MCP实战项目：智能代码助手")
    print("=" * 60)
    
    # 代码分析演示
    await demonstrate_code_analysis()
    
    # 文档生成演示
    await demonstrate_documentation_generation()
    
    # 重构建议演示
    await demonstrate_refactoring()
    
    # 重复代码检测演示
    await demonstrate_duplicate_detection()
    
    # 总结
    print("\n" + "=" * 60)
    print("项目总结")
    print("=" * 60)
    print("""
智能代码助手项目实现了以下功能:

1. 代码分析工具 (CodeAnalyzer)
   - 自动检测编程语言
   - 统计代码行数、注释、空行
   - 识别函数、类、导入语句
   - 计算代码复杂度
   - 检测潜在问题

2. MCP服务器 (CodeAssistantServer)
   - analyze_code: 全面代码分析
   - generate_documentation: 自动生成文档
   - refactor_suggestions: 重构建议
   - find_duplicates: 重复代码检测

3. MCP客户端 (CodeAssistantClient)
   - 封装服务器调用
   - 操作历史记录
   - 文件读写支持

实际应用场景:
- IDE插件开发
- 代码审查工具
- 自动化文档生成
- 代码质量检查

扩展方向:
- 支持更多编程语言
- 集成LLM进行智能分析
- 添加代码自动修复功能
- 实现团队协作功能
""")


if __name__ == "__main__":
    asyncio.run(main())
