from sqlalchemy import select as sqlalchemy_select, insert as sqlalchemy_insert

class BaseService:
    model = None

    @classmethod
    async def get_all(cls,session, **filters):
        query = sqlalchemy_select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        res = result.scalars()
        return res

    @classmethod
    async def get_one_or_none_by_id(cls, session, id):
        query = sqlalchemy_select(cls.model).where(cls.model.id == id)
        result = await session.execute(query)
        res = result.one_or_none()
        return res