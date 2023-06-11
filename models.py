from sqlalchemy import func
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Btc(Base):
    __tablename__ = "btc"
    price: Mapped[str]=mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())


class Eth(Base):
    __tablename__ = "eth"
    price: Mapped[str]=mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())