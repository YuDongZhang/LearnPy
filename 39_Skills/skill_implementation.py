"""
Skill实现示例
=============

本文件展示如何实现具体的Skill：
- Skill处理函数
- 参数验证
- 错误处理
- 结果格式化
"""

from typing import Any, Dict, List, Optional
import re
import json

# ============================================================================
# 第一部分：代码审查Skill实现
# ============================================================================

class CodeReviewerSkill:
    """代码审查Skill"""
    
    name = "code-reviewer"
    description = "审查代码质量和安全问题"
    
    def analyze_syntax(self, code: str, language: str) -> Dict:
        """语法分析"""
        issues = []
        
        if language == "python":
            if "except:" in code:
                issues.append({
                    "type": "error",
                    "line": "未知",
                    "message": "使用裸except，应捕获具体异常"
                })
            
            if re.search(r"\s+=\s+\d+", code):
                issues.append({
                    "type": "warning",
                    "message": "检测到魔法数字，建议使用常量"
                })
        
        elif language == "javascript":
            if "var " in code:
                issues.append({
                    "type": "info",
                    "message": "建议使用let或const替代var"
                })
            
            if "==" in code and "!=" in code:
                issues.append({
                    "type": "warning",
                    "message": "建议使用===或!==进行严格比较"
                })
        
        return issues
    
    def analyze_style(self, code: str, language: str) -> Dict:
        """代码风格分析"""
        issues = []
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    "type": "warning",
                    "line": i,
                    "message": f"行长度{len(line)}超过120字符"
                })
            
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                if language == "python":
                    issues.append({
                        "type": "warning",
                        "line": i,
                        "message": "缩进不符合PEP8规范"
                    })
        
        return issues
    
    def analyze_security(self, code: str, language: str) -> Dict:
        """安全分析"""
        issues = []
        
        security_patterns = {
            "python": [
                (r"eval\s*\(", "使用eval存在安全风险"),
                (r"exec\s*\(", "使用exec存在安全风险"),
                (r"password\s*=\s*['\"]", "硬编码密码存在安全风险"),
                (r"os\.system\s*\(", "os.system存在命令注入风险"),
            ],
            "javascript": [
                (r"eval\s*\(", "使用eval存在安全风险"),
                (r"innerHTML\s*=", "innerHTML可能导致XSS"),
                (r"document\.write\s*\(", "document.write存在安全风险"),
            ]
        }
        
        patterns = security_patterns.get(language, [])
        for pattern, message in patterns:
            if re.search(pattern, code):
                issues.append({
                    "type": "error",
                    "message": message
                })
        
        return issues
    
    def calculate_score(self, issues: List[Dict]) -> int:
        """计算代码评分"""
        score = 100
        
        for issue in issues:
            if issue["type"] == "error":
                score -= 10
            elif issue["type"] == "warning":
                score -= 5
            elif issue["type"] == "info":
                score -= 2
        
        return max(0, score)
    
    def execute(self, params: Dict) -> Dict:
        """执行代码审查"""
        code = params.get("code", "")
        language = params.get("language", "python")
        
        all_issues = []
        all_issues.extend(self.analyze_syntax(code, language))
        all_issues.extend(self.analyze_style(code, language))
        all_issues.extend(self.analyze_security(code, language))
        
        score = self.calculate_score(all_issues)
        
        suggestions = []
        if score < 60:
            suggestions.append("代码需要重大改进")
        elif score < 80:
            suggestions.append("代码质量一般，建议优化")
        else:
            suggestions.append("代码质量良好")
        
        return {
            "score": score,
            "issues": all_issues,
            "suggestions": suggestions,
            "summary": {
                "errors": len([i for i in all_issues if i["type"] == "error"]),
                "warnings": len([i for i in all_issues if i["type"] == "warning"]),
                "infos": len([i for i in all_issues if i["type"] == "info"])
            }
        }


# ============================================================================
# 第二部分：文档生成Skill实现
# ============================================================================

class DocumentGeneratorSkill:
    """文档生成Skill"""
    
    name = "document-generator"
    description = "生成代码文档"
    
    def parse_function(self, code: str) -> Dict:
        """解析函数"""
        func_match = re.search(
            r"def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(\w+))?",
            code
        )
        
        if not func_match:
            return None
        
        func_name = func_match.group(1)
        params_str = func_match.group(2)
        return_type = func_match.group(3)
        
        params = []
        if params_str.strip():
            for param in params_str.split(","):
                param = param.strip()
                if param:
                    parts = param.split(":")
                    name = parts[0].strip()
                    ptype = parts[1].strip() if len(parts) > 1 else "Any"
                    params.append({"name": name, "type": ptype})
        
        return {
            "name": func_name,
            "params": params,
            "return_type": return_type
        }
    
    def generate_google_style(self, func_info: Dict) -> str:
        """生成Google风格的文档"""
        lines = ['    """']
        lines.append(f"    {func_info['name']}的详细说明。")
        lines.append("")
        
        if func_info["params"]:
            lines.append("    Args:")
            for param in func_info["params"]:
                lines.append(f"        {param['name']} ({param['type']}): 参数说明")
            lines.append("")
        
        if func_info["return_type"]:
            lines.append(f"    Returns:")
            lines.append(f"        {func_info['return_type']}: 返回值说明")
        else:
            lines.append("    Returns:")
            lines.append("        None")
        
        lines.append('    """')
        
        return "\n".join(lines)
    
    def generate_numpy_style(self, func_info: Dict) -> str:
        """生成NumPy风格的文档"""
        lines = ['    """']
        lines.append(f"    {func_info['name']}的详细说明。")
        lines.append("")
        
        if func_info["params"]:
            lines.append("    Parameters")
            lines.append("    ----------")
            for param in func_info["params"]:
                lines.append(f"    {param['name']} : {param['type']}")
                lines.append(f"        参数说明")
            lines.append("")
        
        if func_info["return_type"]:
            lines.append("    Returns")
            lines.append("    -------")
            lines.append(f"    {func_info['return_type']}")
            lines.append("        返回值说明")
        
        lines.append('    """')
        
        return "\n".join(lines)
    
    def execute(self, params: Dict) -> Dict:
        """执行文档生成"""
        code = params.get("code", "")
        style = params.get("doc_style", "google")
        
        func_info = self.parse_function(code)
        
        if not func_info:
            return {
                "success": False,
                "error": "无法解析函数定义"
            }
        
        if style == "google":
            doc = self.generate_google_style(func_info)
        elif style == "numpy":
            doc = self.generate_numpy_style(func_info)
        else:
            doc = self.generate_google_style(func_info)
        
        full_code = code + "\n" + doc
        
        return {
            "success": True,
            "document": doc,
            "full_code": full_code,
            "function_info": func_info
        }


# ============================================================================
# 第三部分：测试生成Skill实现
# ============================================================================

class TestGeneratorSkill:
    """测试生成Skill"""
    
    name = "test-generator"
    description = "生成单元测试代码"
    
    def generate_python_tests(self, code: str) -> str:
        """生成Python测试"""
        func_match = re.search(
            r"def\s+(\w+)\s*\(([^)]*)\)",
            code
        )
        
        if not func_match:
            return "# 无法解析函数"
        
        func_name = func_match.group(1)
        params_str = func_match.group(2)
        
        params = []
        if params_str.strip():
            for param in params_str.split(","):
                param = param.strip()
                if param and param != "self":
                    params.append(param.split(":")[0].strip())
        
        test_code = f'''import unittest
from your_module import {func_name}


class Test{func_name.title()}(unittest.TestCase):
    """测试 {func_name} 函数"""
'''
        
        if params:
            test_code += f'''
    def test_{func_name}_basic(self):
        """基本功能测试"""
        result = {func_name}({', '.join([f'{p}=None' for p in params])})
        self.assertIsNotNone(result)
'''
        
        test_code += f'''
    def test_{func_name}_edge_cases(self):
        """边界情况测试"""
        # 添加你的边界情况测试
        pass


if __name__ == "__main__":
    unittest.main()
'''
        
        return test_code
    
    def generate_javascript_tests(self, code: str) -> str:
        """生成JavaScript测试"""
        func_match = re.search(
            r"function\s+(\w+)\s*\(([^)]*)\)|const\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)",
            code
        )
        
        if not func_match:
            return "// 无法解析函数"
        
        func_name = func_match.group(1) or func_match.group(3)
        
        test_code = f'''const {func_name} = require('./your-module');

describe('{func_name}', () => {{
    test('basic functionality', () => {{
        const result = {func_name}();
        expect(result).toBeDefined();
    }});

    test('edge cases', () => {{
        // 添加边界情况测试
    }});
}});
'''
        
        return test_code
    
    def execute(self, params: Dict) -> Dict:
        """执行测试生成"""
        code = params.get("code", "")
        language = params.get("language", "python")
        
        if language == "python":
            tests = self.generate_python_tests(code)
        elif language == "javascript":
            tests = self.generate_javascript_tests(code)
        else:
            return {
                "success": False,
                "error": f"不支持的语言: {language}"
            }
        
        return {
            "success": True,
            "tests": tests,
            "language": language
        }


# ============================================================================
# 第四部分：数据处理Skill实现
# ============================================================================

class DataProcessorSkill:
    """数据处理Skill"""
    
    name = "data-processor"
    description = "处理和分析数据"
    
    def process_json(self, data: Dict) -> Dict:
        """处理JSON数据"""
        return {
            "record_count": len(data) if isinstance(data, (list, dict)) else 1,
            "keys": list(data.keys()) if isinstance(data, dict) else None,
            "type": type(data).__name__
        }
    
    def process_csv(self, data: List[Dict]) -> Dict:
        """处理CSV数据"""
        if not data or not isinstance(data, list):
            return {"error": "无效的CSV数据"}
        
        return {
            "record_count": len(data),
            "columns": list(data[0].keys()) if data else [],
            "sample": data[0] if data else None
        }
    
    def analyze_numeric(self, values: List[float]) -> Dict:
        """数值分析"""
        if not values:
            return {"error": "无数据"}
        
        sorted_values = sorted(values)
        n = len(values)
        
        return {
            "count": n,
            "sum": sum(values),
            "mean": sum(values) / n,
            "median": sorted_values[n // 2] if n % 2 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values)
        }
    
    def execute(self, params: Dict) -> Dict:
        """执行数据处理"""
        data = params.get("data", {})
        operation = params.get("operation", "analyze")
        
        if operation == "analyze":
            if isinstance(data, dict):
                result = self.process_json(data)
            elif isinstance(data, list):
                result = self.process_csv(data)
            else:
                result = {"error": "不支持的数据类型"}
        
        elif operation == "numeric_stats":
            if isinstance(data, list):
                values = [float(x) for x in data if isinstance(x, (int, float))]
                result = self.analyze_numeric(values)
            else:
                result = {"error": "需要数值列表"}
        
        else:
            result = {"error": f"未知操作: {operation}"}
        
        return result


# ============================================================================
# 第五部分：Skill执行器
# ============================================================================

class SkillManager:
    """Skill管理器"""
    
    def __init__(self):
        self.skills = {
            "code-reviewer": CodeReviewerSkill(),
            "document-generator": DocumentGeneratorSkill(),
            "test-generator": TestGeneratorSkill(),
            "data-processor": DataProcessorSkill()
        }
    
    def execute(self, skill_name: str, params: Dict) -> Dict:
        """执行Skill"""
        if skill_name not in self.skills:
            return {
                "success": False,
                "error": f"Skill不存在: {skill_name}"
            }
        
        skill = self.skills[skill_name]
        
        try:
            result = skill.execute(params)
            result["skill"] = skill_name
            return {"success": True, **result}
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "skill": skill_name
            }
    
    def list_skills(self) -> List[Dict]:
        """列出所有Skill"""
        return [
            {"name": name, "description": skill.description}
            for name, skill in self.skills.items()
        ]


# ============================================================================
# 演示
# ============================================================================

def demonstrate_code_reviewer():
    """演示代码审查"""
    
    print("=" * 60)
    print("代码审查Skill演示")
    print("=" * 60)
    
    skill = CodeReviewerSkill()
    
    test_code = """
def process_data(items):
    for item in items:
        try:
            eval(item)
        except:
            pass
    password = "secret123"
    return items
"""
    
    result = skill.execute({
        "code": test_code,
        "language": "python"
    })
    
    print(f"\n代码评分: {result['score']}/100")
    print(f"\n问题统计:")
    print(f"  错误: {result['summary']['errors']}")
    print(f"  警告: {result['summary']['warnings']}")
    print(f"  信息: {result['summary']['infos']}")
    
    print("\n发现的问题:")
    for issue in result["issues"]:
        print(f"  [{issue['type']}] {issue['message']}")
    
    print("\n建议:")
    for suggestion in result["suggestions"]:
        print(f"  - {suggestion}")


def demonstrate_document_generator():
    """演示文档生成"""
    
    print("\n" + "=" * 60)
    print("文档生成Skill演示")
    print("=" * 60)
    
    skill = DocumentGeneratorSkill()
    
    test_code = "def calculate_sum(numbers: list, multiplier: int = 1) -> int:"
    
    print("\n原始代码:")
    print(test_code)
    
    print("\nGoogle风格文档:")
    result = skill.execute({"code": test_code, "doc_style": "google"})
    print(result["document"])
    
    print("\nNumPy风格文档:")
    result = skill.execute({"code": test_code, "doc_style": "numpy"})
    print(result["document"])


def demonstrate_test_generator():
    """演示测试生成"""
    
    print("\n" + "=" * 60)
    print("测试生成Skill演示")
    print("=" * 60)
    
    skill = TestGeneratorSkill()
    
    test_code = "def calculate_sum(a, b): return a + b"
    
    print("\n生成的Python测试:")
    result = skill.execute({"code": test_code, "language": "python"})
    print(result["tests"])


def demonstrate_data_processor():
    """演示数据处理"""
    
    print("\n" + "=" * 60)
    print("数据处理Skill演示")
    print("=" * 60)
    
    skill = DataProcessorSkill()
    
    # 数值分析
    print("\n数值分析:")
    result = skill.execute({
        "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "operation": "numeric_stats"
    })
    print(f"  平均值: {result['mean']}")
    print(f"  中位数: {result['median']}")
    print(f"  总和: {result['sum']}")
    
    # JSON分析
    print("\nJSON分析:")
    result = skill.execute({
        "data": {"name": "test", "value": 100},
        "operation": "analyze"
    })
    print(f"  记录数: {result['record_count']}")
    print(f"  键: {result['keys']}")


def demonstrate_skill_manager():
    """演示Skill管理器"""
    
    print("\n" + "=" * 60)
    print("Skill管理器演示")
    print("=" * 60)
    
    manager = SkillManager()
    
    print("\n可用Skills:")
    for skill in manager.list_skills():
        print(f"  - {skill['name']}: {skill['description']}")
    
    print("\n执行代码审查:")
    result = manager.execute("code-reviewer", {
        "code": "def test(): pass",
        "language": "python"
    })
    print(f"  成功: {result['success']}")
    if result["success"]:
        print(f"  评分: {result['score']}")


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    demonstrate_code_reviewer()
    demonstrate_document_generator()
    demonstrate_test_generator()
    demonstrate_data_processor()
    demonstrate_skill_manager()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
Skill实现要点:

1. 代码审查Skill
   - 语法分析
   - 风格检查
   - 安全扫描
   - 评分系统

2. 文档生成Skill
   - 函数解析
   - 多风格支持
   - 完整文档

3. 测试生成Skill
   - 自动生成测试用例
   - 边界情况覆盖
   - 多种语言支持

4. 数据处理Skill
   - 多种数据格式
   - 统计分析
   - 数据验证

5. Skill管理器
   - 统一执行入口
   - 错误处理
   - 列表和搜索
""")
