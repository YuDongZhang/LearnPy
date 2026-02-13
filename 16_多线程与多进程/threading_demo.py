"""
多线程
======

使用 threading 模块实现多线程。
"""

import threading
import time

print("=" * 40)
print("1. 创建线程")
print("=" * 40)

def worker(name):
    print(f"  {name} 开始工作")
    time.sleep(1)
    print(f"  {name} 完成工作")

thread = threading.Thread(target=worker, args=("线程1",))
thread.start()
thread.join()
print("主线程继续执行")

print()
print("=" * 40)
print("2. 多线程并行")
print("=" * 40)

def task(task_id):
    print(f"  任务 {task_id} 开始")
    time.sleep(0.5)
    print(f"  任务 {task_id} 完成")

threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print("所有任务完成")

print()
print("=" * 40)
print("3. 线程池")
print("=" * 40)

from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n ** 2

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(square, [1, 2, 3, 4, 5]))
print(f"计算结果: {results}")

print()
print("=" * 40)
print("4. 线程同步")
print("=" * 40)

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"计数器: {counter}")

print()
print("=" * 40)
print("5. 守护线程")
print("=" * 40)

def daemon_task():
    print("  守护线程运行中...")
    time.sleep(2)
    print("  守护线程结束")

daemon = threading.Thread(target=daemon_task, daemon=True)
daemon.start()
print("主线程即将退出")
time.sleep(0.5)
print("主线程退出")
