"""
Skill定义与结构
=================

本文件详细介绍如何定义Skill：
- Skill的基本结构
- 元数据定义
- 参数和返回值
- Skill的分类
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json

# ============================================================================
# 第一部分：Skill基本结构
# ============================================================================

@dataclass
class SkillMetadata:
    """Skill元数据"""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = ""
    tags: List[str] = field(default_factory=list)
    examples: List[Dict] = field(default_factory=list)


@dataclass
class SkillParameter:
    """Skill参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum: List[Any] = None


@dataclass
class SkillOutput:
    """Skill输出定义"""
    type: str
    description: str
    schema: Dict = field(default_factory=dict)


class SkillCategory(Enum):
    """Skill分类"""
    CODE = "代码开发"
    DATA = "数据分析"
    DOCUMENT = "文档生成"
    TEST = "测试"
    DEVOPS = "运维"
    INTEGRATION = "集成"
    UTILITY = "工具"
    CUSTOM = "自定义"


@dataclass
class Skill:
    """Skill定义"""
    metadata: SkillMetadata
    category: SkillCategory
    parameters: List[SkillParameter] = field(default_factory=list)
    output: Optional[SkillOutput] = None
    handler: Optional[Callable] = None
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)


def create_skill_metadata(
    name: str,
    description: str,
    version: str = "1.0.0",
    author: str = "",
    tags: List[str] = None,
    examples: List[Dict] = None
) -> SkillMetadata:
    """创建Skill元数据"""
    return SkillMetadata(
        name=name,
        description=description,
        version=version,
        author=author,
        tags=tags or [],
        examples=examples or []
    )


# ============================================================================
# 第二部分：创建具体Skill示例
# ============================================================================

def create_code_reviewer_skill() -> Skill:
    """创建代码审查Skill"""
    
    metadata = create_skill_metadata(
        name="code-reviewer",
        description="审查代码质量和安全问题",
        version="1.0.0",
        author="Community",
        tags=["代码审查", "质量", "安全"],
        examples=[
            {
                "input": "审查这段Python代码: def add(a,b):return a+b",
                "output": "代码审查意见..."
            }
        ]
    )
    
    parameters = [
        SkillParameter(
            name="code",
            type="string",
            description="要审查的代码",
            required=True
        ),
        SkillParameter(
            name="language",
            type="string",
            description="编程语言",
            required=False,
            default="python"
        ),
        SkillParameter(
            name="strictness",
            type="string",
            description="审查严格程度",
            required=False,
            default="normal",
            enum=["strict", "normal", "lenient"]
        )
    ]
    
    output = SkillOutput(
        type="object",
        description="审查结果",
        schema={
            "score": "number",
            "issues": "array",
            "suggestions": "array"
        }
    )
    
    skill = Skill(
        metadata=metadata,
        category=SkillCategory.CODE,
        parameters=parameters,
        output=output
    )
    
    return skill


def create_document_generator_skill() -> Skill:
    """创建文档生成Skill"""
    
    metadata = create_skill_metadata(
        name="document-generator",
        description="生成API文档和代码注释",
        version="1.0.0",
        author="Community",
        tags=["文档", "API", "注释"]
    )
    
    parameters = [
        SkillParameter(
            name="code",
            type="string",
            description="要生成文档的代码",
            required=True
        ),
        SkillParameter(
            name="doc_style",
            type="string",
            description="文档风格",
            required=False,
            default="google",
            enum=["google", "numpy", "sphinx"]
        ),
        SkillParameter(
            name="include_examples",
            type="boolean",
            description="包含示例",
            required=False,
            default=True
        )
    ]
    
    output = SkillOutput(
        type="string",
        description="生成的文档"
    )
    
    return Skill(
        metadata=metadata,
        category=SkillCategory.DOCUMENT,
        parameters=parameters,
        output=output
    )


def create_data_analyzer_skill() -> Skill:
    """创建数据分析Skill"""
    
    metadata = create_skill_metadata(
        name="data-analyzer",
        description="分析数据并生成报告",
        version="1.0.0",
        author="Community",
        tags=["数据", "分析", "统计"]
    )
    
    parameters = [
        SkillParameter(
            name="data",
            type="object",
            description="输入数据",
            required=True
        ),
        SkillParameter(
            name="analysis_type",
            type="string",
            description="分析类型",
            required=False,
            default="basic",
            enum=["basic", "statistical", "predictive"]
        ),
        SkillParameter(
            name="visualize",
            type="boolean",
            description="生成可视化",
            required=False,
            default=False
        )
    ]
    
    return Skill(
        metadata=metadata,
        category=SkillCategory.DATA,
        parameters=parameters
    )


# ============================================================================
# 第三部分：Skill注册和管理
# ============================================================================

class SkillRegistry:
    """Skill注册表"""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.categories: Dict[SkillCategory, List[str]] = {}
    
    def register(self, skill: Skill) -> None:
        """注册Skill"""
        self.skills[skill.metadata.name] = skill
        
        category = skill.category
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(skill.metadata.name)
        
        print(f"✓ 已注册Skill: {skill.metadata.name}")
    
    def get(self, name: str) -> Optional[Skill]:
        """获取Skill"""
        return self.skills.get(name)
    
    def list_all(self) -> List[str]:
        """列出所有Skill"""
        return list(self.skills.keys())
    
    def list_by_category(self, category: SkillCategory) -> List[str]:
        """按分类列出Skill"""
        return self.categories.get(category, [])
    
    def search(self, query: str) -> List[str]:
        """搜索Skill"""
        results = []
        query_lower = query.lower()
        
        for name, skill in self.skills.items():
            if query_lower in name.lower():
                results.append(name)
            elif query_lower in skill.metadata.description.lower():
                results.append(name)
            elif any(query_lower in tag.lower() for tag in skill.metadata.tags):
                results.append(name)
        
        return results


# ============================================================================
# 第四部分：Skill执行
# ============================================================================

class SkillExecutor:
    """Skill执行器"""
    
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.execution_history: List[Dict] = []
    
    def validate_parameters(self, skill: Skill, params: Dict) -> tuple[bool, List[str]]:
        """验证参数"""
        errors = []
        
        for param in skill.parameters:
            if param.required and param.name not in params:
                errors.append(f"缺少必需参数: {param.name}")
        
        return len(errors) == 0, errors
    
    def execute(self, skill_name: str, params: Dict) -> Dict:
        """执行Skill"""
        skill = self.registry.get(skill_name)
        
        if not skill:
            return {
                "success": False,
                "error": f"Skill不存在: {skill_name}"
            }
        
        valid, errors = self.validate_parameters(skill, params)
        if not valid:
            return {
                "success": False,
                "error": "; ".join(errors)
            }
        
        if skill.handler:
            try:
                result = skill.handler(params)
                self.execution_history.append({
                    "skill": skill_name,
                    "params": params,
                    "success": True
                })
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        else:
            return {
                "success": False,
                "error": "Skill未实现处理函数"
            }


# ============================================================================
# 演示
# ============================================================================

def demonstrate_skill_definition():
    """演示Skill定义"""
    
    print("=" * 60)
    print("Skill定义演示")
    print("=" * 60)
    
    # 创建代码审查Skill
    skill = create_code_reviewer_skill()
    
    print(f"\n技能名称: {skill.metadata.name}")
    print(f"描述: {skill.metadata.description}")
    print(f"版本: {skill.metadata.version}")
    print(f"分类: {skill.category.value}")
    print(f"标签: {', '.join(skill.metadata.tags)}")
    
    print("\n参数列表:")
    for param in skill.parameters:
        required_mark = "✓" if param.required else "○"
        print(f"  [{required_mark}] {param.name} ({param.type})")
        print(f"      {param.description}")
        if param.enum:
            print(f"      可选值: {param.enum}")
        if param.default is not None:
            print(f"      默认值: {param.default}")
    
    if skill.output:
        print(f"\n输出类型: {skill.output.type}")
        print(f"输出描述: {skill.output.description}")


def demonstrate_skill_registry():
    """演示Skill注册"""
    
    print("\n" + "=" * 60)
    print("Skill注册演示")
    print("=" * 60)
    
    registry = SkillRegistry()
    
    # 注册Skills
    print("\n注册Skill:")
    registry.register(create_code_reviewer_skill())
    registry.register(create_document_generator_skill())
    registry.register(create_data_analyzer_skill())
    
    # 列出所有
    print("\n所有Skill:")
    for name in registry.list_all():
        skill = registry.get(name)
        print(f"  - {name}: {skill.metadata.description}")
    
    # 按分类列出
    print("\n按分类列出:")
    for category, names in registry.categories.items():
        for name in names:
            print(f"    - {name}")
    
    # 搜索
    print("\n搜索 '代码':")
    results = registry.search("代码")
    for name in results:
        print(f"  - {name}")


def demonstrate_skill_execution():
    """演示Skill执行"""
    
    print("\n" + "=" * 60)
    print("Skill执行演示")
    print("=" * 60)
    
    registry = SkillRegistry()
    registry.register(create_code_reviewer_skill())
    
    executor = SkillExecutor(registry)
    
    # 定义处理函数
    def code_review_handler(params: Dict) -> Dict:
        code = params.get("code", "")
        language = params.get("language", "python")
        
        issues = []
        if len(code) > 100:
            issues.append({"type": "warning", "message": "代码过长"})
        
        if "TODO" not in code and "FIXME" not in code:
            issues.append({"type": "info", "message": "没有TODO或FIXME注释"})
        
        return {
            "score": 85,
            "issues": issues,
            "suggestions": ["考虑添加更多注释", "可以提取一些函数"]
        }
    
    # 设置处理函数
    skill = registry.get("code-reviewer")
    skill.handler = code_review_handler
    
    # 执行
    print("\n执行代码审查Skill:")
    result = executor.execute("code-reviewer", {
        "code": "def hello(): print('hello world') # TODO: add more",
        "language": "python"
    })
    
    if result["success"]:
        print("  执行成功!")
        print(f"  得分: {result['result']['score']}")
        print(f"  问题数: {len(result['result']['issues'])}")
    else:
        print(f"  执行失败: {result['error']}")
    
    # 测试参数验证
    print("\n测试参数验证:")
    result = executor.execute("code-reviewer", {})
    if not result["success"]:
        print(f"  正确捕获错误: {result['error']}")


def demonstrate_skill_json():
    """演示Skill的JSON表示"""
    
    print("\n" + "=" * 60)
    print("Skill JSON表示")
    print("=" * 60)
    
    skill = create_code_reviewer_skill()
    
    skill_json = {
        "name": skill.metadata.name,
        "description": skill.metadata.description,
        "version": skill.metadata.version,
        "category": skill.category.value,
        "parameters": [
            {
                "name": p.name,
                "type": p.type,
                "description": p.description,
                "required": p.required,
                "default": p.default,
                "enum": p.enum
            }
            for p in skill.parameters
        ],
        "output": {
            "type": skill.output.type,
            "description": skill.output.description
        } if skill.output else None
    }
    
    print("\nSkill JSON:")
    print(json.dumps(skill_json, indent=2, ensure_ascii=False))


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    demonstrate_skill_definition()
    demonstrate_skill_registry()
    demonstrate_skill_execution()
    demonstrate_skill_json()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
Skill定义要点:

1. 元数据
   - name: 唯一标识
   - description: 描述用途
   - version: 版本管理
   - tags: 分类标签

2. 参数定义
   - name: 参数名称
   - type: 数据类型
   - description: 说明
   - required: 是否必需
   - default: 默认值
   - enum: 可选值列表

3. 输出定义
   - type: 输出类型
   - description: 说明
   - schema: 结构定义

4. 分类
   - 代码开发
   - 数据分析
   - 文档生成
   - 测试
   - 运维
   - 集成

5. 管理
   - 注册表管理
   - 搜索和发现
   - 执行和验证
""")
