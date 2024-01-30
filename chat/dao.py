from chat.models import User, Message, Chat
from dao import BaseDAO


class UserDAO(BaseDAO):
    model = User

class MessageDAO(BaseDAO):
    model = Message

class ChatDAO(BaseDAO):
    model = Chat