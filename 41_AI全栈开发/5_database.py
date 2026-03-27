"""
5. 数据库 - 代码示例
用SQLAlchemy实现用户和对话历史的持久化。
"""

import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./chat_app.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# 1. 数据模型
# ============================================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), default="新对话")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String(20), nullable=False)  # user / assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")


# 建表
Base.metadata.create_all(engine)


# ============================================================
# 2. CRUD操作
# ============================================================
class ChatDB:
    """对话数据库操作"""

    def __init__(self):
        self.session = SessionLocal()

    def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self, username: str) -> User | None:
        return self.session.query(User).filter_by(username=username).first()

    def create_conversation(self, user_id: int, title: str = "新对话") -> Conversation:
        conv = Conversation(user_id=user_id, title=title)
        self.session.add(conv)
        self.session.commit()
        return conv

    def add_message(self, conversation_id: int, role: str, content: str) -> Message:
        msg = Message(conversation_id=conversation_id, role=role, content=content)
        self.session.add(msg)
        self.session.commit()
        return msg

    def get_messages(self, conversation_id: int) -> list[Message]:
        return (self.session.query(Message)
                .filter_by(conversation_id=conversation_id)
                .order_by(Message.created_at).all())

    def get_conversations(self, user_id: int) -> list[Conversation]:
        return (self.session.query(Conversation)
                .filter_by(user_id=user_id)
                .order_by(Conversation.created_at.desc()).all())


# ============================================================
# 演示
# ============================================================
if __name__ == "__main__":
    db = ChatDB()

    # 创建用户
    user = db.get_user("demo") or db.create_user("demo", "hashed_pw")
    print(f"用户: {user.username}")

    # 创建会话
    conv = db.create_conversation(user.id, "Python问答")
    print(f"会话: {conv.title}")

    # 添加消息
    db.add_message(conv.id, "user", "什么是装饰器？")
    db.add_message(conv.id, "assistant", "装饰器是修改函数行为的语法糖。")

    # 查询
    messages = db.get_messages(conv.id)
    for msg in messages:
        print(f"  [{msg.role}] {msg.content}")
