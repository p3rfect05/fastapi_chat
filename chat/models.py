import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from database import Base



class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    time_created = Column(TIMESTAMP, default=func.now())
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="messages", lazy='selectin')

    chat_id = Column(String, ForeignKey('chats.id'))
    chat = relationship('Chat', back_populates='messages', lazy='selectin')
    def __str__(self):
        return f'{self.text} from {self.user.email}'


# users_chats_table = Table(
#     "users_chats_table",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("chat_id", ForeignKey("chats.id"), primary_key=True),
# )

class UserAndChatsTable(Base):
    __tablename__ = 'users_chats_table'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    chat_id = Column(String, ForeignKey("chats.id"), primary_key=True)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    # username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    messages = relationship("Message", back_populates="user", lazy='selectin')

    chats = relationship(
        "Chat", secondary='users_chats_table', back_populates="users", lazy='selectin'
    )

    def __str__(self):
        return f'{self.email}'
class Chat(Base):
    __tablename__ = 'chats'
    id = Column(String, primary_key=True)
    time_created = Column(TIMESTAMP, default=func.now())
    messages = relationship("Message", back_populates="chat", lazy='selectin')
    users = relationship(
        "User", secondary='users_chats_table', back_populates="chats", lazy='selectin'
    )




