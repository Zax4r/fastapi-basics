from app.services.base import BaseService
from app.models.tasks import Task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


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
