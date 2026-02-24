# 第十六章：多线程与多进程

## 本章目标
- 理解线程和进程的概念
- 掌握 threading 模块
- 掌握 multiprocessing 模块
- 学会选择合适的并发方式

---

## 1. 线程 vs 进程

| 特性 | 线程 | 进程 |
|------|------|------|
| 内存共享 | 共享 | 独立 |
| 创建开销 | 小 | 大 |
| 适用场景 | IO 密集 | CPU 密集 |

---

## 2. 多线程

```python
import threading

def worker():
    print("工作线程")

thread = threading.Thread(target=worker)
thread.start()
```

---

## 上一章 | 下一章

[第十五章：网络请求](../15_网络请求/README.md) | [第十七章：异步编程](../17_异步编程/README.md)
