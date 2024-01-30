import datetime

from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from chat.dao import UserDAO
from chat.models import User
from config import SECRET_KEY, HS_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_token(request: Request):
    token: str = request.cookies.get('chat_access_token')
    return token

async def validate_token(token: str = Depends(get_token)) -> int | None:
    try:
        if not token:
            raise JWTError
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HS_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(detail='User unauthenticated', status_code=status.HTTP_401_UNAUTHORIZED)

    except JWTError:
        raise HTTPException(detail='Invalid token', status_code=status.HTTP_401_UNAUTHORIZED)
    exp: str = payload.get('exp')
    if not exp or int(exp) < datetime.datetime.utcnow().timestamp():
        raise HTTPException(detail='Token expired', status_code=status.HTTP_401_UNAUTHORIZED)
    return int(user_id)
async def get_current_user(response: Response, user_id: int = Depends(validate_token)) -> User:
    #user_id = await validate_token()
    user = await UserDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(detail='User is not registered', status_code=status.HTTP_401_UNAUTHORIZED)
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, HS_ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    print(user)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user