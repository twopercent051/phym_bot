from sqlalchemy import MetaData, inspect, Column, String, insert, select, Integer, Text, Boolean, Time, \
    DateTime, update, TIMESTAMP, delete, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker, as_declarative
from sqlalchemy.sql import expression

from create_bot import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    metadata = MetaData()

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class UsersDB(Base):
    """Пользователи"""
    __tablename__ = "users"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    smoking = Column(String, nullable=True)
    drinking = Column(String, nullable=True)
    timezone = Column(Integer, nullable=True)
    next_step = Column(String, nullable=True)
    dtime = Column(TIMESTAMP, nullable=True)


class FeedbacksDB(Base):
    """отзывы"""
    __tablename__ = "feedbacks"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = Column(String, nullable=False)
    week_id = Column(Integer, nullable=False)
    workout_id = Column(Integer, nullable=False)
    feedback_1 = Column(String, nullable=False)
    feedback_2 = Column(String, nullable=True)
    feedback_week = Column(String, nullable=True)


class TextsDB(Base):
    """Тексты сообщений бота"""
    __tablename__ = "texts"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    chapter = Column(String, nullable=False)
    photo_id = Column(String, nullable=True)
    text = Column(Text, nullable=True)


class BaseDAO:
    """Класс взаимодействия с БД"""
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_many(cls, **filter_by) -> list:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**data)
            await session.execute(stmt)
            await session.commit()


class UsersDAO(BaseDAO):
    model = UsersDB

    @classmethod
    async def update_user_id(cls, user_id: str, **data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(user_id=user_id)
            await session.execute(stmt)
            await session.commit()


class TextsDAO(BaseDAO):
    model = TextsDB

    @classmethod
    async def update(cls, chapter: str, **data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(chapter=chapter)
            await session.execute(stmt)
            await session.commit()


class FeedbacksDAO(BaseDAO):
    model = FeedbacksDB

    @classmethod
    async def update_workout_id(cls, user_id: str, week_id: int, workout_id: int, **data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(user_id=user_id, week_id=week_id, workout_id=workout_id)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update_week_id(cls, user_id: str, week_id: int, **data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(user_id=user_id, week_id=week_id)
            await session.execute(stmt)
            await session.commit()
