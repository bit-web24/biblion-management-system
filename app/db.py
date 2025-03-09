from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Annotated
from sqlalchemy.orm import declarative_base

SQLLITE_FILE_NAME = "database.db"
SQLLITE_URL = f"sqlite:///{SQLLITE_FILE_NAME}"
connect_args = {"check_same_thread": False}
engine = create_engine(SQLLITE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    with SessionLocal() as session:
        yield session


def create_db_and_tables():
    Base.metadata.create_all(engine)

def remove_db_and_tables():
    Base.metadata.drop_all(engine)

SessionDep = Annotated[Session, Depends(get_db)]
