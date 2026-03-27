# 3. 并发与队列

## AI应用的并发挑战

- LLM推理慢（1-10秒/请求）
- GPU资源有限
- 突发流量可能打垮服务

## 并发控制

### 信号量限制并发数
限制同时进行的LLM调用数量：
```python
semaphore = asyncio.Semaphore(10)  # 最多10个并发
async with semaphore:
    result = await call_llm(...)
```

### 连接池
复用HTTP连接，减少开销：
```python
session = aiohttp.ClientSession()  # 复用
```

## 消息队列

将耗时任务异步化：
```
用户请求 → API → 放入队列 → 返回任务ID
                     ↓
              Worker消费 → 调用LLM → 存结果
                     ↓
用户轮询/WebSocket ← 获取结果
```

适用场景：
- 长文档处理
- 批量生成
- 不需要实时返回的任务

## 限流

| 层级 | 方式 | 工具 |
|------|------|------|
| 网关层 | Nginx限流 | limit_req |
| 应用层 | 中间件限流 | slowapi |
| 用户层 | 按用户限流 | Redis计数 |

## 优雅降级

当系统压力大时：
1. 优先服务VIP用户
2. 降低max_tokens
3. 使用更小的模型
4. 返回缓存结果
5. 排队等待
