"""
网络请求
========

使用 requests 库发送 HTTP 请求。
"""

print("=" * 40)
print("1. 安装 requests")
print("=" * 40)

print("pip install requests")

print()
print("=" * 40)
print("2. GET 请求")
print("=" * 40)

import requests

print("""
import requests

response = requests.get("https://httpbin.org/get")
print(response.status_code)
print(response.text)
print(response.json())
""")

print()
print("=" * 40)
print("3. POST 请求")
print("=" * 40)

print("""
data = {"username": "test", "password": "123456"}
response = requests.post("https://httpbin.org/post", data=data)
print(response.json())
""")

print()
print("=" * 40)
print("4. 请求参数")
print("=" * 40)

print("""
params = {"key": "value", "search": "python"}
response = requests.get("https://httpbin.org/get", params=params)

headers = {"User-Agent": "my-app"}
response = requests.get("https://httpbin.org/headers", headers=headers)
""")

print()
print("=" * 40)
print("5. 响应处理")
print("=" * 40)

print("""
response = requests.get("https://httpbin.org/get")

print(response.status_code)   # 状态码
print(response.headers)       # 响应头
print(response.text)         # 文本内容
print(response.json())       # JSON 解析
print(response.content)      # 原始字节
""")

print()
print("=" * 40)
print("6. 错误处理")
print("=" * 40)

print("""
try:
    response = requests.get("https://httpbin.org/status/404")
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
""")

print()
print("=" * 40)
print("7. 会话保持")
print("=" * 40)

print("""
session = requests.Session()
session.headers.update({"User-Agent": "my-app"})

response1 = session.get("https://httpbin.org/cookies/set", params={"cookie": "value"})
response2 = session.get("https://httpbin.org/cookies")
print(response2.json())
""")

print()
print("=" * 40)
print("8. 实际应用示例")
print("=" * 40)

print("""
import requests

def fetch_user_data(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

user = fetch_user_data(1)
if user:
    print(f"用户名: {user['name']}")
    print(f"邮箱: {user['email']}")
""")
