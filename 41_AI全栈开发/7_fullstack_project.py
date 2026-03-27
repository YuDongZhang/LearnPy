"""
7. 全栈实战 - AI聊天助手后端
集成：FastAPI + SQLite + JWT认证 + 流式输出 + 对话历史

运行: uvicorn 7_fullstack_project:app --port 8080
文档: http://localhost:8080/docs
"""

import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from openai import OpenAI
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# ========== 配置 ==========
SECRET_KEY = "change-me-in-production"
DATABASE_URL = "sqlite:///./fullstack_app.db"
LLM_BASE = "http://localhost:11434/v1"
MODEL = "qwen2.5:7b"

# ========== 初始化 ==========
app = FastAPI(title="AI Chat Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

llm_client = OpenAI(base_url=LLM_BASE, api_key="ollama")
pwd_context = CryptContext(schemes=["bcrypt"])
security = HTTPBearer(auto_error=False)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ========== 数据模型 ==========
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(128))

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), default="新对话")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String(20))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)


# ========== 请求模型 ==========
class AuthRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


# ========== 认证 ==========
def create_token(username: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY)

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if not cred:
        raise HTTPException(401, "需要登录")
    try:
        payload = jwt.decode(cred.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(401, "Token无效")


# ========== 路由：认证 ==========
@app.post("/api/register")
async def register(req: AuthRequest):
    db = SessionLocal()
    if db.query(User).filter_by(username=req.username).first():
        raise HTTPException(400, "用户已存在")
    db.add(User(username=req.username, password_hash=pwd_context.hash(req.password)))
    db.commit()
    return {"message": "注册成功"}

@app.post("/api/login")
async def login(req: AuthRequest):
    db = SessionLocal()
    user = db.query(User).filter_by(username=req.username).first()
    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(401, "用户名或密码错误")
    return {"token": create_token(req.username)}


# ========== 路由：对话 ==========
@app.post("/api/chat")
async def chat(req: ChatRequest, username: str = Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()

    # 获取或创建会话
    if req.conversation_id:
        conv = db.query(Conversation).get(req.conversation_id)
    else:
        conv = Conversation(user_id=user.id, title=req.message[:30])
        db.add(conv)
        db.commit()

    # 加载历史消息
    history = db.query(Message).filter_by(conversation_id=conv.id).order_by(Message.created_at).all()
    messages = [{"role": m.role, "content": m.content} for m in history[-10:]]  # 最近10条
    messages.append({"role": "user", "content": req.message})

    # 保存用户消息
    db.add(Message(conversation_id=conv.id, role="user", content=req.message))

    # 调用LLM
    response = llm_client.chat.completions.create(model=MODEL, messages=messages)
    answer = response.choices[0].message.content

    # 保存助手回复
    db.add(Message(conversation_id=conv.id, role="assistant", content=answer))
    db.commit()

    return {"answer": answer, "conversation_id": conv.id}


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest, username: str = Depends(get_current_user)):
    """流式对话"""
    messages = [{"role": "user", "content": req.message}]

    def generate():
        stream = llm_client.chat.completions.create(model=MODEL, messages=messages, stream=True)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/conversations")
async def list_conversations(username: str = Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    convs = db.query(Conversation).filter_by(user_id=user.id).order_by(Conversation.created_at.desc()).all()
    return [{"id": c.id, "title": c.title, "created_at": str(c.created_at)} for c in convs]


if __name__ == "__main__":
    import uvicorn
    print("启动: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
