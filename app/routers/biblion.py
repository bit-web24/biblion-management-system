from fastapi import APIRouter, HTTPException
from typing import List
from app.db import SessionDep
from app.services import biblion
from app.schemas import BiblionResponse, BiblionCreate

router = APIRouter(prefix='/biblion')

@router.get('/', response_model=List[BiblionResponse])
async def get_all(session: SessionDep):
    biblia = biblion.get_all(session)
    return [BiblionResponse.model_validate(_biblion) for _biblion in biblia]

@router.get('/{biblion_id}')
def get(biblion_id: int, session: SessionDep):
    _biblion = biblion.get(session, biblion_id)
    if _biblion is None:
        raise HTTPException(status_code=404, detail="Biblion Not Found")

@router.post('/', response_model=BiblionResponse)
async def add(_biblion: BiblionCreate, session: SessionDep):
    _biblion = biblion.add(session, _biblion)
    return BiblionResponse.model_validate(_biblion)


@router.put('/{biblion_id}', response_model=BiblionResponse)
async def update(biblion_id: int, _biblion: BiblionCreate, session: SessionDep):
    updated_biblion = biblion.update(session, biblion_id, _biblion)
    if updated_biblion is None:
        raise HTTPException(status_code=404, detail="Biblion Not Found")
    return BiblionResponse.model_validate(updated_biblion)

@router.delete('/{biblion_id}')
async def delete(biblion_id: int, session: SessionDep):
    deleted_biblion = biblion.delete(session, biblion_id)
    if deleted_biblion is None:
        raise HTTPException(status_code=404, detail="Biblion Not Found")
    return {
        "message": "Biblion Deleted Successfully"
    }
