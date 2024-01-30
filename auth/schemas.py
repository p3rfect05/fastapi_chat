from pydantic import BaseModel, EmailStr
from sqlalchemy import UUID, TIMESTAMP


class SMessage(BaseModel):
    id: int
    text: str
    user_id: int
    chat_id: str
    time_created: str
class SUser(BaseModel):
    id: int
    hashed_password: str
    email: str

class SUserAuth(BaseModel):
    email: EmailStr
    password: str


