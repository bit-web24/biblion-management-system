from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Annotated
from app.models import Base

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    Base.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]
