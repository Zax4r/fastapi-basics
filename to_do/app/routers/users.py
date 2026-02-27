from app.schemas.users import SUserAdd, SUserAnswer
from fastapi import APIRouter
from app.models.dependecies import DbDep
from typing import List
from app.services.users import UserService
from app.core.security import hash_password


router = APIRouter(prefix='/users',tags=['Работа с пользователем'])

@router.post('/add/')
async def add_user(user: SUserAdd, session: DbDep):
    new_user_dict = user.dict()
    new_user_dict['password'] = hash_password(new_user_dict['password'])
    check = await UserService.add_one(session,**new_user_dict)
    if check:
        return {'message':f'Пользователь добавлен:{user}'}
    return {'message':f'Ошибка добавления пользователя:{user}'}

@router.get('/', response_model=List[SUserAnswer])
async def get_users(session: DbDep):
    users = await UserService.get_all(session)
    return users

@router.get('/{user_id}', response_model=SUserAnswer)
async def get_user(user_id:int, session: DbDep):
    user = await UserService.get_one_or_none_by_field(session,id=user_id)
    return user

@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, session: DbDep):
    check = await UserService.delete_one_by_id(session, user_id)
    if check:
        return {'message':f'Пользователь с id {user_id} удалён'}
    else:
        return {'message':'Такой пользователь не найден'}