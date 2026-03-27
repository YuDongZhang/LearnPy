"""
3. Tokenizer设计 - 代码示例
演示BPE原理和HuggingFace Tokenizer的使用。
"""

from collections import Counter


# ============================================================
# 1. 简易BPE实现
# ============================================================
class SimpleBPE:
    """最简BPE实现，理解原理用"""

    def __init__(self, vocab_size: int = 50):
        self.vocab_size = vocab_size
        self.merges = []

    def _get_pairs(self, tokens_list):
        """统计所有相邻token对的频率"""
        pairs = Counter()
        for tokens in tokens_list:
            for i in range(len(tokens) - 1):
                pairs[(tokens[i], tokens[i+1])] += 1
        return pairs

    def _merge(self, tokens_list, pair):
        """合并指定的token对"""
        new_token = pair[0] + pair[1]
        result = []
        for tokens in tokens_list:
            merged = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                    merged.append(new_token)
                    i += 2
                else:
                    merged.append(tokens[i])
                    i += 1
            result.append(merged)
        return result

    def train(self, texts: list[str], num_merges: int = 20):
        """训练BPE"""
        # 初始化：字符级token
        tokens_list = [list(text) for text in texts]
        vocab = set(c for text in texts for c in text)
        print(f"初始词表大小: {len(vocab)}")

        for i in range(num_merges):
            pairs = self._get_pairs(tokens_list)
            if not pairs:
                break
            best_pair = pairs.most_common(1)[0][0]
            tokens_list = self._merge(tokens_list, best_pair)
            new_token = best_pair[0] + best_pair[1]
            vocab.add(new_token)
            self.merges.append(best_pair)
            if i < 5:
                print(f"  合并{i+1}: '{best_pair[0]}' + '{best_pair[1]}' → '{new_token}'")

        print(f"最终词表大小: {len(vocab)}")
        return tokens_list


# ============================================================
# 2. HuggingFace Tokenizer使用
# ============================================================
def demo_hf_tokenizer():
    """使用HuggingFace的Tokenizer"""
    from transformers import AutoTokenizer

    models = ["Qwen/Qwen2.5-0.5B", "meta-llama/Llama-2-7b-hf"]
    text = "Python是一种高级编程语言，Hello World!"

    for model_name in models:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            tokens = tokenizer.encode(text)
            decoded = tokenizer.convert_ids_to_tokens(tokens)
            print(f"\n{model_name}:")
            print(f"  词表大小: {tokenizer.vocab_size}")
            print(f"  Token数: {len(tokens)}")
            print(f"  Tokens: {decoded[:15]}...")
        except Exception as e:
            print(f"\n{model_name}: 加载失败 ({e})")


# ============================================================
# 3. 对比不同Tokenizer的编码效率
# ============================================================
def demo_encoding_efficiency():
    """对比同一文本在不同Tokenizer下的Token数"""
    from transformers import AutoTokenizer

    texts = [
        "Python是一种高级编程语言",
        "The quick brown fox jumps over the lazy dog",
        "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
    ]

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B", trust_remote_code=True)
    print("编码效率（Qwen2.5 Tokenizer）:")
    for text in texts:
        tokens = tokenizer.encode(text)
        ratio = len(text) / len(tokens)
        print(f"  {len(tokens):3d} tokens | {ratio:.1f} 字符/token | {text[:40]}")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("1. 简易BPE")
    print("=" * 60)
    bpe = SimpleBPE()
    texts = ["low lower lowest", "new newer newest", "low new low"]
    bpe.train(texts, num_merges=10)

    print("\n" + "=" * 60)
    print("2. HuggingFace Tokenizer")
    print("=" * 60)
    demo_hf_tokenizer()

    print("\n" + "=" * 60)
    print("3. 编码效率")
    print("=" * 60)
    demo_encoding_efficiency()
