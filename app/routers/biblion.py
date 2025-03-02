from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.auth import get_current_user
from app.db import SessionDep
from app.models import User
from app.services import biblion
from app.schemas import BiblionResponse, BiblionCreate, biblion_create

router = APIRouter(prefix='/biblion')

@router.get('/', response_model=List[BiblionResponse])
async def get_all_books(session: SessionDep, _current_user: User = Depends(get_current_user)):
    biblia = biblion.get_all_by_user(session, _current_user.id)
    return [BiblionResponse.model_validate(_biblion) for _biblion in biblia]

@router.get('/{biblion_id}', response_model=BiblionResponse)
def get_a_book(
        biblion_id: int,
        session: SessionDep,
        _current_user: User = Depends(get_current_user)
):
    _biblion = biblion.get(session, biblion_id, _current_user.id)
    if _biblion is None:
        raise HTTPException(status_code=404, detail="Biblion Not Found")
    return BiblionResponse.model_validate(_biblion)


@router.post('/', response_model=BiblionResponse)
async def add_new_book(
        session: SessionDep,
        _biblion: BiblionCreate = Depends(biblion_create),
        _current_user: User = Depends(get_current_user)
):
    _biblion = biblion.add(session, _biblion, _current_user.id)
    return BiblionResponse.model_validate(_biblion)


@router.put('/{biblion_id}', response_model=BiblionResponse)
async def update_a_book(
        biblion_id: int, session: SessionDep,
        _biblion: BiblionCreate = Depends(biblion_create),
        _current_user: User = Depends(get_current_user)
):
    updated_biblion = biblion.update(session, biblion_id, _biblion, _current_user.id)
    if updated_biblion is None:
        raise HTTPException(status_code=404, detail="Biblion Not Found")
    return BiblionResponse.model_validate(updated_biblion)

@router.delete('/{biblion_id}')
async def delete_a_book(
        biblion_id: int,
        session: SessionDep,
        _current_user: User = Depends(get_current_user)
):
    deleted_biblion = biblion.delete(session, biblion_id, _current_user.id)
    if deleted_biblion is None:
        raise HTTPException(status_code=404, detail="Biblion Not Found")
    return {
        "message": "Biblion Deleted Successfully"
    }
