import uuid
from sqlalchemy import DateTime, Float, String, Text, func, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Генератор рандомного id
def random_id():
    return int(f"100{uuid.uuid4().int >> (128 - 32)}")


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())  # UTC
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(100))


class Progress_users(Base):
    __tablename__ = "progress_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    ref_id: Mapped[str] = mapped_column(String(100))
    direction: Mapped[str] = mapped_column(String(100))
    progress: Mapped[int] = mapped_column()
    active: Mapped[int] = mapped_column()
    condition: Mapped[int] = mapped_column()
    payment_status: Mapped[int] = mapped_column()
    page: Mapped[int] = mapped_column()
    current_promo: Mapped[int] = mapped_column()
    promocode: Mapped[str] = mapped_column(String(100))
    date: Mapped[str] = mapped_column(String(100))


class Promocodes(Base):
    __tablename__ = "promocodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    promocode: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(100))
    excur_id: Mapped[int] = mapped_column()

class Excursions(Base):
    __tablename__ = "excursions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    excur_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    photo: Mapped[str] = mapped_column(Text)
