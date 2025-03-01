from typing import Optional
from fastapi import Form
from pydantic import BaseModel

class Base(BaseModel):
    pass

class BiblionResponse(Base):
    id: int
    name: str
    author: str
    publisher: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class BiblionCreate(Base):
    name: str
    author: str
    publisher: Optional[str] = None
    description: Optional[str] = None

def biblion_create(
    name: str = Form(...),
    author: str = Form(...),
    publisher: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
) -> BiblionCreate:
    return BiblionCreate(name=name, author=author, publisher=publisher, description=description)
