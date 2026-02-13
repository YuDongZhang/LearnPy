"""
多进程
======

使用 multiprocessing 模块实现多进程。
"""

import multiprocessing
import time

print("=" * 40)
print("1. 创建进程")
print("=" * 40)

def worker(name):
    print(f"  {name} 开始")
    time.sleep(1)
    print(f"  {name} 完成")

process = multiprocessing.Process(target=worker, args=("进程1",))
process.start()
process.join()
print("主进程继续")

print()
print("=" * 40)
print("2. 进程池")
print("=" * 40)

from multiprocessing import Pool

def square(n):
    return n ** 2

if __name__ == "__main__":
    with Pool(processes=3) as pool:
        results = pool.map(square, [1, 2, 3, 4, 5])
    print(f"计算结果: {results}")

print()
print("=" * 40)
print("3. 进程间通信")
print("=" * 40)

def producer(queue):
    for i in range(3):
        queue.put(i)
    queue.put(None)

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"  消费: {item}")

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=producer, args=(queue,))
    p2 = multiprocessing.Process(target=consumer, args=(queue,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    print("通信完成")

print()
print("=" * 40)
print("4. 共享内存")
print("=" * 40)

def worker(counter, lock):
    for _ in range(100000):
        with lock:
            counter.value += 1

if __name__ == "__main__":
    counter = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    
    processes = [multiprocessing.Process(target=worker, args=(counter, lock)) for _ in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    
    print(f"计数器: {counter.value}")

print()
print("=" * 40)
print("5. 线程 vs 进程选择")
print("=" * 40)

print("IO 密集型任务（网络请求、文件读写）:")
print("  - 推荐使用多线程")
print("  - 示例：爬虫、API 调用")

print()
print("CPU 密集型任务（计算、图像处理）:")
print("  - 推荐使用多进程")
print("  - 示例：数据分析、机器学习")
