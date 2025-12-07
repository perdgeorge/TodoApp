from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, TimestampMixin


class Todo(Base, TimestampMixin):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
