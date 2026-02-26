from app.schemas.users import SUserAdd, SUserAnswer
from fastapi import APIRouter
from app.dependecies import DbDep
from typing import List
from app.services.users import UserService


router = APIRouter(prefix='/users',tags=['Работа с пользователем'])

@router.post('/add/')
async def add_user(user: SUserAdd):
    return user

@router.get('/', response_model=List[SUserAnswer])
async def get_users(session: DbDep):
    users = await UserService.get_all(session)
    return users