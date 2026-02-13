# 第十五章：网络请求

## 本章目标
- 理解 HTTP 请求
- 掌握 requests 库使用
- 学会处理 API 响应

---

## 1. requests 库

```python
import requests

response = requests.get("https://api.example.com/data")
print(response.json())
```

---

## 2. 常用方法

| 方法 | 说明 |
|------|------|
| `requests.get()` | GET 请求 |
| `requests.post()` | POST 请求 |
| `requests.put()` | PUT 请求 |
| `requests.delete()` | DELETE 请求 |

---

## 上一章 | 下一章

[第十四章：数据库操作](../14_数据库操作/README.md) | [第十六章：多线程与多进程](../16_多线程与多进程/README.md)
