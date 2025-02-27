from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    biblia: Mapped[List["Biblion"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Biblion(Base):
    __tablename__ = "biblia"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(40))
    publisher: Mapped[str] = mapped_column(String(100))
    user: Mapped[User] = relationship(back_populates="biblia")

    def __repr__(self) -> str:
        return f"Biblion(id={self.id!r}, name={self.name!r}, author={self.author!r}, publisher={self.publisher!r})"

