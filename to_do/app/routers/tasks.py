from fastapi import APIRouter
from app.services.tasks import TaskService
from app.schemas.tasks import STaskAdd, STaskShow
from app.dependecies import DbDep
from typing import List


router = APIRouter(prefix='/tasks',tags=['Работа с задачами'])

@router.post('/add/')
async def add_task(new_task: STaskAdd, session: DbDep):
    check = await TaskService.add_one(session,**new_task.dict())
    if check:
        return {'message':f'Задача {new_task.task_name} для пользователя {new_task.user_id} добавлена'}
    return {'message':f'Ошибка при добавлении {new_task.task_name} для пользователя {new_task.user_id}'}

@router.get('/', response_model=List[STaskShow])
async def get_all(session: DbDep):
    tasks = await TaskService.get_all(session)
    return tasks