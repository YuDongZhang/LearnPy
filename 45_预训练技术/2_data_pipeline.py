"""
2. 数据收集与清洗 - 代码示例
演示预训练数据的去重、质量过滤、数据混合。
"""

import hashlib
import re
from collections import Counter


# ============================================================
# 1. 精确去重（Hash去重）
# ============================================================
def exact_dedup(documents: list[str]) -> list[str]:
    """基于MD5的精确去重"""
    seen = set()
    unique = []
    for doc in documents:
        h = hashlib.md5(doc.strip().encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(doc)
    print(f"精确去重: {len(documents)} → {len(unique)} (去除{len(documents)-len(unique)}条)")
    return unique


# ============================================================
# 2. 模糊去重（N-gram Jaccard相似度）
# ============================================================
def ngram_set(text: str, n: int = 3) -> set:
    words = text.split()
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))


def jaccard_sim(a: set, b: set) -> float:
    if not a or not b:
        return 0
    return len(a & b) / len(a | b)


def fuzzy_dedup(documents: list[str], threshold: float = 0.8) -> list[str]:
    """基于Jaccard相似度的模糊去重"""
    unique = []
    unique_ngrams = []
    for doc in documents:
        ng = ngram_set(doc)
        is_dup = any(jaccard_sim(ng, existing) > threshold for existing in unique_ngrams)
        if not is_dup:
            unique.append(doc)
            unique_ngrams.append(ng)
    print(f"模糊去重: {len(documents)} → {len(unique)}")
    return unique


# ============================================================
# 3. 质量过滤
# ============================================================
def quality_filter(documents: list[str]) -> list[str]:
    """基于规则的质量过滤"""
    filtered = []
    for doc in documents:
        # 长度过滤
        if len(doc) < 50 or len(doc) > 100000:
            continue
        # 特殊字符比例
        special_ratio = sum(1 for c in doc if not c.isalnum() and not c.isspace()) / len(doc)
        if special_ratio > 0.3:
            continue
        # 重复行比例
        lines = doc.split("\n")
        if len(lines) > 1:
            unique_lines = set(lines)
            if len(unique_lines) / len(lines) < 0.5:
                continue
        filtered.append(doc)
    print(f"质量过滤: {len(documents)} → {len(filtered)}")
    return filtered


# ============================================================
# 4. 敏感信息过滤
# ============================================================
def remove_pii(text: str) -> str:
    """移除个人信息"""
    text = re.sub(r'\b\d{11}\b', '[PHONE]', text)
    text = re.sub(r'\b[\w.+-]+@[\w-]+\.[\w.]+\b', '[EMAIL]', text)
    text = re.sub(r'\b\d{17}[\dXx]\b', '[ID_CARD]', text)
    return text


# ============================================================
# 5. 数据混合
# ============================================================
def mix_data(sources: dict[str, list[str]], ratios: dict[str, float]) -> list[str]:
    """按比例混合不同来源的数据"""
    total = sum(len(v) for v in sources.values())
    mixed = []
    for source, ratio in ratios.items():
        data = sources.get(source, [])
        n = int(total * ratio)
        mixed.extend(data[:n])
    print(f"数据混合: {dict((k, len(v)) for k, v in sources.items())} → {len(mixed)} 条")
    return mixed


# ============================================================
# 演示
# ============================================================
if __name__ == "__main__":
    docs = [
        "Python是一种高级编程语言，广泛用于Web开发和数据分析。",
        "Python是一种高级编程语言，广泛用于Web开发和数据分析。",  # 精确重复
        "Python是高级编程语言，广泛应用于Web开发和数据分析领域。",  # 模糊重复
        "Java是一种面向对象的编程语言，由Sun Microsystems开发。",
        "短",  # 太短
        "联系方式：13800138000，邮箱test@example.com",  # 含PII
    ]

    print("=" * 50)
    docs = exact_dedup(docs)
    docs = fuzzy_dedup(docs)
    docs = quality_filter(docs)
    print(f"\n最终: {len(docs)} 条")
    for d in docs:
        print(f"  {remove_pii(d)[:60]}...")
