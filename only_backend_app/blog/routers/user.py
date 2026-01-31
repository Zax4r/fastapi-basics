from fastapi import APIRouter, Depends
from .. import schemas
from ..database import get_session
from ..repository import user

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/',response_model=schemas.ShowUser)
def create_user(request:schemas.User, session=Depends(get_session)):
    return user.create_user(request, session)

@router.get('/{id}',response_model=schemas.ShowUser)
def get_user_by_id(id:int, session=Depends(get_session)):
    return user.get_user_by_id(id, session)