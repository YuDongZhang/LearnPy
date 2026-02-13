"""
自定义迭代器
===========
"""

print("=" * 40)
print("1. 倒计时迭代器")
print("=" * 40)

class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print("倒计时 5:")
for num in CountDown(5):
    print(f"  {num}")

print()
print("=" * 40)
print("2. 平方数迭代器")
print("=" * 40)

class Squares:
    def __init__(self, n):
        self.n = n
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.n:
            raise StopIteration
        result = self.current ** 2
        self.current += 1
        return result

print("前5个平方数:")
for square in Squares(5):
    print(f"  {square}")

print()
print("=" * 40)
print("3. 斐波那契迭代器")
print("=" * 40)

class Fibonacci:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.n:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

print("前10个斐波那契数:")
for fib in Fibonacci(10):
    print(f"  {fib}")

print()
print("=" * 40)
print("4. 无限循环迭代器")
print("=" * 40)

class Cycle:
    def __init__(self, iterable):
        self.iterable = iterable
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.iterable:
            raise StopIteration
        result = self.iterable[self.index]
        self.index = (self.index + 1) % len(self.iterable)
        return result

colors = Cycle(["红", "绿", "蓝"])
print("循环颜色 7 次:")
for i, color in enumerate(colors):
    if i >= 7:
        break
    print(f"  {color}")

print()
print("=" * 40)
print("5. 范围迭代器")
print("=" * 40)

class MyRange:
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        self.current = start
        self.stop = stop
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration
        if self.step < 0 and self.current <= self.stop:
            raise StopIteration
        result = self.current
        self.current += self.step
        return result

print("MyRange(5):")
for num in MyRange(5):
    print(f"  {num}")

print()
print("MyRange(1, 10, 2):")
for num in MyRange(1, 10, 2):
    print(f"  {num}")

print()
print("=" * 40)
print("6. 字符串单词迭代器")
print("=" * 40)

class WordIterator:
    def __init__(self, text):
        self.words = text.split()
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.words):
            raise StopIteration
        word = self.words[self.index]
        self.index += 1
        return word

text = "Python 是一门优雅的编程语言"
print(f"原文: {text}")
print("单词迭代:")
for word in WordIterator(text):
    print(f"  '{word}'")
