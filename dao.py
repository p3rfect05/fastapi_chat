from sqlalchemy import insert, select

from database import async_sessionmaker


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **kwargs):
        async with async_sessionmaker() as session:
            query = insert(cls.model).values(**kwargs).returning(cls.model)
            obj = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            # print(obj.time_created)
            return obj

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, obj_id: int):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(id=obj_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().all()
