from app.schemas.user import SUserAdd
from fastapi import APIRouter

router = APIRouter(prefix='/users',tags=['Работа с пользователем'])

@router.post('/add/')
async def add_user(user: SUserAdd):
    return user