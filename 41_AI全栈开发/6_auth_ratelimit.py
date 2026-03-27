"""
6. 认证与限流 - 代码示例
演示JWT认证和简单限流。
"""

import time
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext

app = FastAPI(title="Auth & Rate Limit Demo")

# ========== JWT配置 ==========
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"])
security = HTTPBearer()

# 模拟用户数据库
USERS_DB = {}


# ========== 数据模型 ==========
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ========== JWT工具函数 ==========
def create_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(401, "无效Token")
        return username
    except JWTError:
        raise HTTPException(401, "Token已过期或无效")


# ========== 简单限流器 ==========
class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: dict[str, list[float]] = {}

    def check(self, key: str) -> bool:
        now = time.time()
        if key not in self.requests:
            self.requests[key] = []
        # 清理过期记录
        self.requests[key] = [t for t in self.requests[key] if now - t < self.window]
        if len(self.requests[key]) >= self.max_requests:
            return False
        self.requests[key].append(now)
        return True

limiter = RateLimiter(max_requests=10, window_seconds=60)


# ========== 路由 ==========
@app.post("/register")
async def register(req: RegisterRequest):
    if req.username in USERS_DB:
        raise HTTPException(400, "用户已存在")
    USERS_DB[req.username] = pwd_context.hash(req.password)
    return {"message": f"用户 {req.username} 注册成功"}


@app.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    pw_hash = USERS_DB.get(req.username)
    if not pw_hash or not pwd_context.verify(req.password, pw_hash):
        raise HTTPException(401, "用户名或密码错误")
    return TokenResponse(access_token=create_token(req.username))


@app.post("/chat")
async def chat(request: Request, user: str = Depends(get_current_user)):
    # 限流检查
    if not limiter.check(user):
        raise HTTPException(429, "请求过于频繁，请稍后重试")
    return {"answer": f"你好 {user}，这是一个需要认证的接口", "remaining": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
