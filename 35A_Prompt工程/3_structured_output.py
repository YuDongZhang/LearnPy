"""
3. 结构化输出 - 代码示例
演示JSON输出、Pydantic校验、LangChain OutputParser。
"""

import json
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
MODEL = "gpt-4o"


# ============================================================
# 1. 强制JSON输出
# ============================================================
def demo_json_output():
    """使用response_format强制JSON输出"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个情感分析助手，用JSON格式输出。"},
            {"role": "user", "content":
                '分析以下文本的情感，输出格式：\n'
                '{"sentiment": "正面/负面/中性", "confidence": 0.0-1.0, "keywords": ["关键词"]}\n\n'
                '文本：这个产品质量很好，物流也快，下次还会买'}
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    result = json.loads(response.choices[0].message.content)
    print(f"JSON输出: {json.dumps(result, ensure_ascii=False, indent=2)}")
    return result


# ============================================================
# 2. Pydantic校验输出
# ============================================================
class SentimentResult(BaseModel):
    sentiment: str
    confidence: float
    keywords: list[str]


def demo_pydantic_validation():
    """用Pydantic校验LLM的JSON输出"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content":
                '分析情感，输出JSON：{"sentiment":"...","confidence":0.0-1.0,"keywords":[...]}\n'
                '文本：服务态度太差了，等了一个小时'}
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    raw = json.loads(response.choices[0].message.content)

    # Pydantic校验
    try:
        result = SentimentResult(**raw)
        print(f"校验通过: sentiment={result.sentiment}, confidence={result.confidence}")
    except Exception as e:
        print(f"校验失败: {e}")


# ============================================================
# 3. LangChain OutputParser
# ============================================================
def demo_langchain_parser():
    """使用LangChain的结构化输出解析器"""
    from langchain_openai import ChatOpenAI
    from langchain.output_parsers import PydanticOutputParser
    from langchain.prompts import ChatPromptTemplate

    class CodeReview(BaseModel):
        score: int
        issues: list[str]
        suggestion: str

    parser = PydanticOutputParser(pydantic_object=CodeReview)

    prompt = ChatPromptTemplate.from_template(
        "审查以下Python代码，{format_instructions}\n\n代码:\n{code}"
    )

    llm = ChatOpenAI(model=MODEL, temperature=0)
    chain = prompt | llm | parser

    result = chain.invoke({
        "code": "def add(a, b): return a + b",
        "format_instructions": parser.get_format_instructions()
    })
    print(f"代码审查: score={result.score}, issues={result.issues}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. JSON输出")
    print("=" * 60)
    demo_json_output()

    print("\n" + "=" * 60)
    print("2. Pydantic校验")
    print("=" * 60)
    demo_pydantic_validation()

    print("\n" + "=" * 60)
    print("3. LangChain OutputParser")
    print("=" * 60)
    demo_langchain_parser()
