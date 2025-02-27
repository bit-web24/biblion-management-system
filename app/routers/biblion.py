from fastapi import APIRouter
from app.services import biblion

router = APIRouter(prefix='/biblion')

@router.get('/')
async def get_all():
    return biblion.get_all()

@router.get('/{biblion_id}')
def get(biblion_id: int):
    return biblion.get(biblion_id)

@router.post('/')
async def add(_biblion):
    return biblion.add(_biblion)

@router.put('/{biblion_id}')
async def update(biblion_id: int):
    return biblion.update(biblion_id)

@router.delete('/{biblion_id}')
async def delete(biblion_id: int):
    return biblion.delete(biblion_id)
