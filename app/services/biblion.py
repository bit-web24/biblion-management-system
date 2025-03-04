from app.db import SessionDep
from app.schemas import BiblionCreate
from app.models import Biblion


def get_all_by_user(session: SessionDep, user_id: int):
    return session.query(Biblion).filter(Biblion.user_id == user_id).all()


def get(session: SessionDep, biblion_id: int, user_id: int):
    return (
        session.query(Biblion)
        .filter(Biblion.id == biblion_id, Biblion.user_id == user_id)
        .first()
    )


def add(session: SessionDep, biblion: BiblionCreate, user_id: int):
    session_biblion = Biblion(
        name=biblion.name,
        author=biblion.author,
        publisher=biblion.publisher,
        description=biblion.description,
        user_id=user_id,
    )
    session.add(session_biblion)
    session.commit()
    session.refresh(session_biblion)
    return session_biblion


def update(session: SessionDep, biblion_id: int, biblion: BiblionCreate, user_id: int):
    _biblion = (
        session.query(Biblion)
        .filter(Biblion.id == biblion_id, Biblion.user_id == user_id)
        .first()
    )
    if not _biblion:
        return None

    _biblion.name = biblion.name
    _biblion.author = biblion.author
    _biblion.publisher = biblion.publisher
    _biblion.description = biblion.description

    session.commit()
    session.refresh(_biblion)
    return _biblion


def delete(session: SessionDep, biblion_id: int, user_id: int):
    _biblion = (
        session.query(Biblion)
        .filter(Biblion.id == biblion_id, Biblion.user_id == user_id)
        .first()
    )
    if not _biblion:
        return None

    session.delete(_biblion)
    session.commit()
    return _biblion
