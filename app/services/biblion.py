from app.db import SessionDep
from app.schemas import BiblionCreate
from app.models import Biblion


def get_all(session: SessionDep):
    biblia = session.query(Biblion).all()
    return biblia

def get(session: SessionDep, biblion_id: int):
    biblion = session.query(Biblion).filter(Biblion.id == biblion_id).first()
    return biblion

def add(session: SessionDep, biblion: BiblionCreate):
    session_biblion = Biblion(name=biblion.name, author=biblion.author, publisher=biblion.publisher, description=biblion.description)
    session.add(session_biblion)
    session.commit()
    session.refresh(session_biblion)
    return session_biblion

def update(session: SessionDep, biblion_id: int, biblion: BiblionCreate):
    _biblion = session.query(Biblion).filter(Biblion.id == biblion_id).first()
    if not _biblion:
        return None

    _biblion.name = biblion.name
    _biblion.author = biblion.author
    _biblion.publisher = biblion.publisher
    _biblion.description = biblion.description

    session.commit()
    session.refresh(_biblion)
    return _biblion

def delete(session: SessionDep, biblion_id: int):
    _biblion = session.query(Biblion).filter(Biblion.id == biblion_id).first()
    if not _biblion:
        return None

    session.delete(_biblion)
    session.commit()
    return _biblion
