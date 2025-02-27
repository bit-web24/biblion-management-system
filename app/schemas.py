from pydantic import BaseModel

class Base(BaseModel):
    pass

class BiblionResponse(Base):
    id: int
    name: str
    author: str
    publisher: str | None
    description: str | None

    class config:
        from_attributes = True

class BiblionCreate(Base):
    name: str
    author: str
    publisher: str | None
    description: str | None

