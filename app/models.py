from typing import Optional
from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(12))
    biblion_entries = relationship("Biblion", back_populates="owner")

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.username!r}, password={self.password!r})"
        )


class Biblion(Base):
    __tablename__ = "biblia"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(40))
    publisher: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="biblion_entries")

    def __repr__(self) -> str:
        return f"Biblion(id={self.id!r}, name={self.name!r}, author={self.author!r}, publisher={self.publisher!r})"
