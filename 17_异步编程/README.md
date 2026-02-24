# 第十七章：异步编程

## 本章目标
- 理解同步与异步的区别
- 掌握 asyncio 基础用法
- 学会使用 async/await
- 掌握异步任务管理

---

## 1. 同步 vs 异步

### 同步方式
代码依次执行，等待每个操作完成后才执行下一个。

```python
import requests

def fetch_data():
    r1 = requests.get("https://api.example.com/1")  # 等待完成
    r2 = requests.get("https://api.example.com/2")  # 等待完成
    r3 = requests.get("https://api.example.com/3")  # 等待完成
    return [r1.json(), r2.json(), r3.json()]
```

### 异步方式
同时发起多个操作，提高效率。

```python
import aiohttp
import asyncio

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get("https://api.example.com/1"),
            session.get("https://api.example.com/2"),
            session.get("https://api.example.com/3")
        ]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]
```

---

## 2. async/await 基础

### 定义异步函数

```python
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # 模拟异步操作
    print("World")

# 运行异步函数
asyncio.run(say_hello())
```

### await 关键字

`await` 用于等待异步操作完成，暂停当前协程。

```python
async def get_data():
    await asyncio.sleep(2)  # 模拟网络请求
    return "数据"

async def main():
    result = await get_data()
    print(result)

asyncio.run(main())
```

---

## 3. asyncio.gather 并发执行

同时运行多个异步任务。

```python
import asyncio

async def task1():
    await asyncio.sleep(2)
    return "任务1完成"

async def task2():
    await asyncio.sleep(1)
    return "任务2完成"

async def main():
    results = await asyncio.gather(task1(), task2())
    print(results)  # ['任务1完成', '任务2完成']

asyncio.run(main())
```

---

## 4. asyncio.create_task 任务管理

创建后台任务，不等待完成。

```python
import asyncio

async def background_task():
    await asyncio.sleep(3)
    print("后台任务完成")

async def main():
    task = asyncio.create_task(background_task())
    print("主程序继续执行")
    await task  # 等待任务完成

asyncio.run(main())
```

---

## 5. 异步上下文管理器

```python
import aiohttp

async def fetch_all():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com/data") as response:
            data = await response.json()
            return data
```

---

## 6. 异步迭代器

```python
import asyncio

async def async_generator():
    for i in range(3):
        await asyncio.sleep(1)
        yield i

async def main():
    async for item in async_generator():
        print(item)

asyncio.run(main())
```

---

## 7. 异步与同步代码的区别

| 特性 | 同步代码 | 异步代码 |
|------|----------|----------|
| 阻塞 | 阻塞整个线程 | 只暂停当前协程 |
| 并发 | 多线程/多进程 | 单线程事件循环 |
| 适用场景 | CPU 密集 | IO 密集（网络请求、文件读写） |

---

## 8. 常用异步库

- **aiohttp** - 异步 HTTP 客户端/服务器
- **aioredis** - 异步 Redis 客户端
- **asyncpg** - 异步 PostgreSQL 客户端
- **uvicorn** - 异步 ASGI 服务器

---

## 上一章 | 下一章

[第十六章：多线程与多进程](../16_多线程与多进程/README.md)
