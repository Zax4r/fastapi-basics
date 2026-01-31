from .. import models, schemas
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..utils import get_password_hash

def create_user(request:schemas.User, session: Session):
    new_user = models.User(name=request.name,email=request.email,password=get_password_hash(request.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_id(id:int, session: Session):
    stmt = select(models.User).where(models.User.id==id)
    user = session.scalars(stmt).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    
    return user

def get_user_by_email(email:str, session: Session):
    stmt = select(models.User).where(models.User.email==email)
    user = session.scalars(stmt).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    
    return user