from fastapi import APIRouter
from app.services.tasks import TaskService
from app.schemas.tasks import STaskAdd, STaskShow, STaskUpd
from app.models.dependecies import DbDep
from app.core.dependecies import CUDep
from typing import List


router = APIRouter(prefix='/tasks',tags=['Работа с задачами'])

@router.post('/add/')
async def add_task(add_task: STaskAdd, session: DbDep, current_user: CUDep):
    new_task = add_task.model_dump()
    new_task['user_id'] = current_user.id
    check = await TaskService.add_one(session,**new_task)
    if check:
        return {'message':f'Задача {new_task['task_name']} для пользователя {new_task['user_id']} добавлена'}
    return {'message':f'Ошибка при добавлении {new_task['task_name']} для пользователя {new_task['user_id']}'}

@router.put('/update/{task_id}')
async def update_task(task_id: int, task_upd: STaskUpd, session: DbDep):
    new_task = task_upd.model_dump()
    check = await TaskService.update_one(session, task_id, **new_task)
    if check:
        return {'message':f'Задача {new_task['task_name']} обновлена'}
    return {'message':f'Ошибка при обновлении {new_task['task_name']}'}



@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, session: DbDep, current_user: CUDep):
    check = await TaskService.delete_task(session, task_id, current_user.id)
    if check:
        return {'message':f'Задача успешно удалена'}
    return {'message':f'Задача не удалена удалена'}


@router.get('/', response_model=List[STaskShow])
async def get_all(session: DbDep, user: CUDep):
    tasks = await TaskService.get_all(session, user_id = user.id)
    return tasks