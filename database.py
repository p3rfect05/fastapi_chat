from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD, DB_HOST, DB_PORT

DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}?ssl=true'

engine = create_async_engine(DATABASE_URL, connect_args = {'sslmode' : 'disable'})

print('engine created')
async_sessionmaker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass