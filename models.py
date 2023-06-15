from sqlalchemy import func
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Index(Base):
    __tablename__ = "index"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str]
    price: Mapped[str]
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())


async def insert_object(async_session,object):
    async with async_session() as session:
        async with session.begin():
            session.add(object)
