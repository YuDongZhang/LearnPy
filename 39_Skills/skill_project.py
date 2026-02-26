"""
Skills实战项目
==============

本项目实现一个完整的Skill系统：智能开发助手
包含：
- Skill注册和管理
- 代码处理Skill集
- AI Agent集成
- 工作流自动化
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
import re
import json

# ============================================================================
# 第一部分：Skill核心系统
# ============================================================================

@dataclass
class SkillInfo:
    """Skill信息"""
    name: str
    description: str
    category: str
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)


class SkillSystem:
    """Skill核心系统"""
    
    def __init__(self):
        self.skills: Dict[str, Callable] = {}
        self.metadata: Dict[str, SkillInfo] = {}
    
    def register(self, name: str, handler: Callable, 
                 description: str = "", category: str = "general",
                 tags: List[str] = None):
        """注册Skill"""
        self.skills[name] = handler
        self.metadata[name] = SkillInfo(
            name=name,
            description=description,
            category=category,
            tags=tags or []
        )
        print(f"✓ Skill已注册: {name}")
    
    def execute(self, name: str, params: Dict) -> Dict:
        """执行Skill"""
        if name not in self.skills:
            return {"error": f"Skill不存在: {name}"}
        
        try:
            result = self.skills[name](params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_all(self) -> List[SkillInfo]:
        """列出所有Skill"""
        return list(self.metadata.values())


# ============================================================================
# 第二部分：代码处理Skills
# ============================================================================

class CodeProcessor:
    """代码处理器"""
    
    @staticmethod
    def analyze(code: str, language: str = "python") -> Dict:
        """分析代码"""
        lines = code.split("\n")
        
        result = {
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith("#")]),
            "comment_lines": len([l for l in lines if l.strip().startswith("#")]),
            "blank_lines": len([l for l in lines if not l.strip()]),
            "functions": len(re.findall(r"^def\s+", code, re.MULTILINE)),
            "classes": len(re.findall(r"^class\s+", code, re.MULTILINE))
        }
        
        return result
    
    @staticmethod
    def format(code: str, style: str = "python") -> str:
        """格式化代码"""
        if style == "python":
            lines = code.split("\n")
            formatted = []
            indent_level = 0
            
            for line in lines:
                stripped = line.strip()
                
                if not stripped:
                    formatted.append("")
                    continue
                
                if stripped.startswith(("return", "break", "continue", "pass")):
                    indent_level = max(0, indent_level - 1)
                
                formatted.append("    " * indent_level + stripped)
                
                if stripped.endswith(":"):
                    indent_level += 1
                
                if stripped.startswith(("return", "break", "continue", "pass")):
                    indent_level = max(0, indent_level - 1)
            
            return "\n".join(formatted)
        
        return code
    
    @staticmethod
    def validate(code: str, language: str = "python") -> Dict:
        """验证代码"""
        issues = []
        
        if language == "python":
            if "except:" in code:
                issues.append({"type": "error", "message": "使用裸except"})
            
            if re.search(r"\s+=\s+\d+", code):
                issues.append({"type": "warning", "message": "使用魔法数字"})
            
            if len(code.split("\n")) > 500:
                issues.append({"type": "info", "message": "文件较长，考虑拆分"})
        
        return {
            "valid": len([i for i in issues if i["type"] == "error"]) == 0,
            "issues": issues
        }


class DocumentationGenerator:
    """文档生成器"""
    
    @staticmethod
    def generate_docstring(code: str, style: str = "google") -> str:
        """生成文档字符串"""
        func_match = re.search(
            r"def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(\w+))?:",
            code
        )
        
        if not func_match:
            return "无法解析函数"
        
        name = func_match.group(1)
        params_str = func_match.group(2)
        return_type = func_match.group(3)
        
        params = []
        if params_str.strip():
            for p in params_str.split(","):
                p = p.strip()
                if p and p != "self":
                    params.append(p.split(":")[0].strip())
        
        if style == "google":
            lines = ['    """']
            lines.append(f"    {name}的详细说明。")
            lines.append("")
            
            if params:
                lines.append("    Args:")
                for p in params:
                    lines.append(f"        {p}: 参数说明")
                lines.append("")
            
            if return_type:
                lines.append(f"    Returns:")
                lines.append(f"        {return_type}: 返回值说明")
            else:
                lines.append("    Returns:")
                lines.append("        None")
            
            lines.append('    """')
            return "\n".join(lines)
        
        return '    """函数说明"""'
    
    @staticmethod
    def generate_readme(project_name: str, description: str = "") -> str:
        """生成README"""
        return f"""# {project_name}

{description or "项目描述"}

## 安装

```bash
pip install {project_name.lower().replace(" ", "-")}
```

## 使用

```python
import {project_name.lower().replace(" ", "_")}

# 你的代码
```

## 贡献

欢迎提交Pull Request！

## 许可证

MIT
"""


class TestGenerator:
    """测试生成器"""
    
    @staticmethod
    def generate_tests(code: str, language: str = "python") -> str:
        """生成测试代码"""
        func_match = re.search(
            r"def\s+(\w+)\s*\(([^)]*)\)",
            code
        )
        
        if not func_match:
            return "# 无法解析函数"
        
        name = func_match.group(1)
        params_str = func_match.group(2)
        
        params = []
        if params_str.strip():
            for p in params_str.split(","):
                p = p.strip()
                if p and p != "self":
                    params.append(p.split(":")[0].strip())
        
        if language == "python":
            test_code = f'''import unittest
from your_module import {name}


class Test{name.title()}(unittest.TestCase):
    """测试{name}函数"""
'''
            
            if params:
                test_code += f'''
    def test_{name}_basic(self):
        """基本测试"""
        result = {name}({', '.join([f'{p}=None' for p in params])})
        self.assertIsNotNone(result)
'''
            
            test_code += '''
    def test_edge_cases(self):
        """边界情况测试"""
        pass


if __name__ == "__main__":
    unittest.main()
'''
            
            return test_code
        
        return "# 不支持的语言"


# ============================================================================
# 第三部分：构建开发助手
# ============================================================================

class DevAssistant:
    """开发助手"""
    
    def __init__(self):
        self.skill_system = SkillSystem()
        self._register_skills()
    
    def _register_skills(self):
        """注册所有Skills"""
        
        # 代码分析
        self.skill_system.register(
            "analyze_code",
            lambda p: CodeProcessor.analyze(p.get("code", ""), p.get("language", "python")),
            description="分析代码结构",
            category="code",
            tags=["分析", "代码"]
        )
        
        # 代码格式化
        self.skill_system.register(
            "format_code",
            lambda p: CodeProcessor.format(p.get("code", ""), p.get("style", "python")),
            description="格式化代码",
            category="code",
            tags=["格式化", "代码"]
        )
        
        # 代码验证
        self.skill_system.register(
            "validate_code",
            lambda p: CodeProcessor.validate(p.get("code", ""), p.get("language", "python")),
            description="验证代码质量",
            category="code",
            tags=["验证", "代码"]
        )
        
        # 文档生成
        self.skill_system.register(
            "generate_docstring",
            lambda p: DocumentationGenerator.generate_docstring(p.get("code", ""), p.get("style", "google")),
            description="生成文档字符串",
            category="documentation",
            tags=["文档", "注释"]
        )
        
        # README生成
        self.skill_system.register(
            "generate_readme",
            lambda p: DocumentationGenerator.generate_readme(p.get("project_name", "project"), p.get("description", "")),
            description="生成README文件",
            category="documentation",
            tags=["文档", "README"]
        )
        
        # 测试生成
        self.skill_system.register(
            "generate_tests",
            lambda p: TestGenerator.generate_tests(p.get("code", ""), p.get("language", "python")),
            description="生成单元测试",
            category="testing",
            tags=["测试", "单元测试"]
        )
    
    def process(self, task: str, params: Dict) -> Dict:
        """处理任务"""
        task_mapping = {
            "分析代码": "analyze_code",
            "格式化代码": "format_code",
            "验证代码": "validate_code",
            "生成文档": "generate_docstring",
            "生成README": "generate_readme",
            "生成测试": "generate_tests"
        }
        
        skill_name = task_mapping.get(task)
        
        if not skill_name:
            return {"error": f"未知任务: {task}"}
        
        return self.skill_system.execute(skill_name, params)
    
    def help(self) -> str:
        """显示帮助"""
        skills = self.skill_system.list_all()
        
        help_text = "可用命令:\n\n"
        
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
        
        for category, skills_list in categories.items():
            help_text += f"【{category}】\n"
            for s in skills_list:
                help_text += f"  - {s.description} ({s.name})\n"
            help_text += "\n"
        
        return help_text


# ============================================================================
# 第四部分：演示
# ============================================================================

def demonstrate_code_analysis():
    """演示代码分析"""
    
    print("=" * 60)
    print("1. 代码分析演示")
    print("=" * 60)
    
    assistant = DevAssistant()
    
    code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self.result
'''
    
    print("\n原始代码:")
    print(code)
    
    result = assistant.process("分析代码", {"code": code})
    
    print("\n分析结果:")
    print(f"  总行数: {result['result']['total_lines']}")
    print(f"  代码行: {result['result']['code_lines']}")
    print(f"  注释行: {result['result']['comment_lines']}")
    print(f"  函数数量: {result['result']['functions']}")
    print(f"  类数量: {result['result']['classes']}")


def demonstrate_code_validation():
    """演示代码验证"""
    
    print("\n" + "=" * 60)
    print("2. 代码验证演示")
    print("=" * 60)
    
    assistant = DevAssistant()
    
    code = '''
def divide(a, b):
    try:
        return a / b
    except:
        return 0

API_KEY = "123456789"
'''
    
    print("\n待验证代码:")
    print(code)
    
    result = assistant.process("验证代码", {"code": code})
    
    print("\n验证结果:")
    print(f"  是否有效: {result['result']['valid']}")
    print("\n发现的问题:")
    for issue in result['result']['issues']:
        print(f"  [{issue['type']}] {issue['message']}")


def demonstrate_documentation():
    """演示文档生成"""
    
    print("\n" + "=" * 60)
    print("3. 文档生成演示")
    print("=" * 60)
    
    assistant = DevAssistant()
    
    code = "def process_data(data: list, options: dict = None) -> dict:"
    
    print("\n原始代码:")
    print(code)
    
    print("\n生成的文档字符串:")
    result = assistant.process("生成文档", {"code": code, "style": "google"})
    print(result['result'])


def demonstrate_readme_generation():
    """演示README生成"""
    
    print("\n" + "=" * 60)
    print("4. README生成演示")
    print("=" * 60)
    
    assistant = DevAssistant()
    
    result = assistant.process("生成README", {
        "project_name": "My Project",
        "description": "一个强大的Python库"
    })
    
    print("\n生成的README:")
    print(result['result'])


def demonstrate_test_generation():
    """演示测试生成"""
    
    print("\n" + "=" * 60)
    print("5. 测试生成演示")
    print("=" * 60)
    
    assistant = DevAssistant()
    
    code = "def calculate(a: int, b: int) -> int:"
    
    print("\n原始代码:")
    print(code)
    
    print("\n生成的测试:")
    result = assistant.process("生成测试", {"code": code})
    print(result['result'])


def demonstrate_help():
    """演示帮助"""
    
    print("\n" + "=" * 60)
    print("6. 帮助信息演示")
    print("=" * 60)
    
    assistant = DevAssistant()
    print(assistant.help())


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("Skills实战项目：智能开发助手")
    print("=" * 60)
    
    demonstrate_code_analysis()
    demonstrate_code_validation()
    demonstrate_documentation()
    demonstrate_readme_generation()
    demonstrate_test_generation()
    demonstrate_help()
    
    print("\n" + "=" * 60)
    print("项目总结")
    print("=" * 60)
    print("""
本项目实现了完整的Skill系统：智能开发助手

核心组件:

1. SkillSystem
   - Skill注册和管理
   - 统一执行接口
   - 元数据管理

2. CodeProcessor
   - 代码分析
   - 代码格式化
   - 代码验证

3. DocumentationGenerator
   - 文档字符串生成
   - README生成

4. TestGenerator
   - 单元测试生成

5. DevAssistant
   - 整合所有Skills
   - 任务路由
   - 用户友好接口

功能特点:

- 完整的Skill生命周期管理
- 代码质量检查和分析
- 自动文档生成
- 单元测试自动生成
- 可扩展的架构

使用方式:

assistant = DevAssistant()
result = assistant.process("分析代码", {"code": "..."})
result = assistant.process("生成文档", {"code": "..."})
result = assistant.process("生成测试", {"code": "..."})

扩展方向:

- 添加更多代码分析规则
- 集成AI进行智能建议
- 支持更多语言
- 添加代码修复功能
- 集成CI/CD
""")


# ============================================================================
# 真实Skill文件创建（在下一部分）
# ============================================================================

def create_real_skill_file():
    """创建真实的Skill文件"""
    import os
    
    # 确保目录存在
    skill_dir = ".trae/skills/code-assistant"
    os.makedirs(skill_dir, exist_ok=True)
    
    # 创建SKILL.md
    skill_content = """---
name: "code-assistant"
description: "AI coding assistant with code analysis, documentation generation, and testing capabilities. Invoke when user asks for code review, documentation, or test generation."
---

# Code Assistant

This skill provides comprehensive coding assistance including:

## Features

### Code Analysis
- Analyze code structure and complexity
- Detect potential issues and bugs
- Check code style and best practices

### Documentation Generation
- Generate docstrings in multiple styles (Google, NumPy, Sphinx)
- Create README files
- Generate inline comments

### Test Generation
- Create unit tests
- Generate test cases for edge cases
- Support multiple testing frameworks

## Usage

```python
# Analyze code
result = await skill.execute("analyze_code", {"code": "def foo(): pass"})

# Generate documentation
result = await skill.execute("generate_docstring", {"code": "def add(a, b): return a + b"})

# Generate tests
result = await skill.execute("generate_tests", {"code": "def add(a, b): return a + b"})
```

## Parameters

- `code`: Code to process (required)
- `language`: Programming language (optional, default: python)
- `style`: Documentation style (optional, default: google)

## Examples

**Code Review:**
```
User: Review this code
Skill: Analyzes code and provides detailed feedback
```

**Documentation:**
```
User: Generate docs for this function
Skill: Creates comprehensive docstring
```

**Testing:**
```
User: Write tests for this
Skill: Generates unit test cases
```
"""
    
    with open(f"{skill_dir}/SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_content)
    
    print(f"\n✓ 真实Skill文件已创建: {skill_dir}/SKILL.md")


if __name__ == "__main__":
    create_real_skill_file()
