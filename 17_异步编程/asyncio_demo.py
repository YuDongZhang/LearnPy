"""
异步编程
========

使用 asyncio 模块实现异步编程。
"""

import asyncio
import time

print("=" * 40)
print("1. 定义异步函数")
print("=" * 40)

async def say_hello():
    print("  Hello")
    await asyncio.sleep(1)
    print("  World")

asyncio.run(say_hello())

print()
print("=" * 40)
print("2. await 关键字")
print("=" * 40)

async def get_data():
    await asyncio.sleep(1)
    return "数据获取完成"

async def main():
    result = await get_data()
    print(f"  {result}")

asyncio.run(main())

print()
print("=" * 40)
print("3. asyncio.gather 并发执行")
print("=" * 40)

async def task1():
    await asyncio.sleep(2)
    return "任务1"

async def task2():
    await asyncio.sleep(1)
    return "任务2"

async def main():
    start = time.time()
    results = await asyncio.gather(task1(), task2())
    elapsed = time.time() - start
    print(f"  结果: {results}")
    print(f"  耗时: {elapsed:.2f}秒")

asyncio.run(main())

print()
print("=" * 40)
print("4. create_task 创建后台任务")
print("=" * 40)

async def background_task():
    await asyncio.sleep(2)
    print("  后台任务完成")

async def main():
    task = asyncio.create_task(background_task())
    print("  主程序继续执行")
    await task

asyncio.run(main())

print()
print("=" * 40)
print("5. 异步生成器")
print("=" * 40)

async def async_generator():
    for i in range(3):
        await asyncio.sleep(0.5)
        yield i

async def main():
    async for item in async_generator():
        print(f"  收到: {item}")

asyncio.run(main())

print()
print("=" * 40)
print("6. 异步任务组")
print("=" * 40)

async def fetch_url(url):
    await asyncio.sleep(0.5)
    return f"响应: {url}"

async def main():
    urls = ["api/user", "api/order", "api/product"]
    tasks = [fetch_url(url) for url in urls]
    
    results = await asyncio.gather(*tasks)
    for url, result in zip(urls, results):
        print(f"  {url} -> {result}")

asyncio.run(main())

print()
print("=" * 40)
print("7. 异步池 Executor")
print("=" * 40)

def sync_task(n):
    time.sleep(1)
    return n * n

async def main():
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, sync_task, 5)
    print(f"  结果: {results}")

asyncio.run(main())

print()
print("=" * 40)
print("8. 完整示例：并发请求")
print("=" * 40)

async def fake_request(url, delay):
    await asyncio.sleep(delay)
    return f"{url} OK"

async def main():
    tasks = [
        fake_request("请求A", 1),
        fake_request("请求B", 0.5),
        fake_request("请求C", 0.8),
    ]
    results = await asyncio.gather(*tasks)
    print("  所有请求完成:")
    for r in results:
        print(f"    - {r}")

asyncio.run(main())

print()
print("=" * 40)
print("示例结束")
print("=" * 40)
