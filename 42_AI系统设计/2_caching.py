"""
2. 缓存策略 - 代码示例
演示精确缓存和语义缓存。
"""

import hashlib
import time
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


# ============================================================
# 1. 精确缓存
# ============================================================
class ExactCache:
    """基于hash的精确缓存"""

    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl

    def _key(self, text: str) -> str:
        return hashlib.md5(text.strip().lower().encode()).hexdigest()

    def get(self, question: str) -> str | None:
        key = self._key(question)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["time"] < self.ttl:
                return entry["answer"]
            del self.cache[key]
        return None

    def set(self, question: str, answer: str):
        self.cache[self._key(question)] = {"answer": answer, "time": time.time()}


# ============================================================
# 2. 语义缓存
# ============================================================
class SemanticCache:
    """基于Embedding相似度的语义缓存"""

    def __init__(self, threshold: float = 0.92):
        self.entries = []  # [(embedding, question, answer)]
        self.threshold = threshold
        self.embed_client = OpenAI()  # 用OpenAI Embedding

    def _embed(self, text: str) -> list[float]:
        resp = self.embed_client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return resp.data[0].embedding

    def _cosine_sim(self, a, b):
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get(self, question: str) -> str | None:
        if not self.entries:
            return None
        q_emb = self._embed(question)
        best_score, best_answer = 0, None
        for emb, q, answer in self.entries:
            score = self._cosine_sim(q_emb, emb)
            if score > best_score:
                best_score, best_answer = score, answer
        if best_score >= self.threshold:
            return best_answer
        return None

    def set(self, question: str, answer: str):
        emb = self._embed(question)
        self.entries.append((emb, question, answer))
