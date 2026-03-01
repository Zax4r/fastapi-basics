from app.services.base import BaseService
from app.models.tasks import Task
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, event, update


class TaskService(BaseService):
    model=Task


    @classmethod
    async def delete_task(cls, session: AsyncSession, task_id: int, user_id: int):
        result = await session.execute(select(cls.model)
                                    .where(cls.model.id==task_id))
        task = result.scalar_one_or_none()
        if not task:
            return None
        
        if task.user_id != user_id:
            return None
        try:
            await session.delete(task)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            return None

    @event.listens_for(Task,'after_delete')
    def update_after_deletion(mapper,connection,target):
        user_id = target.user_id
        if target.is_checked:
            connection.execute(
                update(User)
                .where(User.id==user_id)
                .values(completed_tasks = User.completed_tasks-1)
            )
        else:
            connection.execute(
                update(User)
                .where(User.id==user_id)
                .values(active_tasks = User.active_tasks-1)
            )

    @event.listens_for(Task,'after_insert')
    def update_after_insert(mapper,connection,target):
        user_id = target.user_id
        connection.execute(
            update(User)
            .where(User.id==user_id)
            .values(active_tasks = User.active_tasks+1))
