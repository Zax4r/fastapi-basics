from sqlalchemy import select,update,delete
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status, Request

def get_all(session: Session):
    stmt = select(models.Blog)
    blogs = session.scalars(stmt).all()
    return blogs

def create(request: Request,session: Session, current_user: schemas.User):
    stmt = select(models.User).where(models.User.email == current_user.email)
    user = session.scalars(stmt).first()
    new_blog = models.Blog(title=request.title,body=request.body,user_id=user.id)
    session.add(new_blog)
    session.commit()
    session.refresh(new_blog)
    return new_blog

def get_by_id(id: int, session: Session):
    stmt = select(models.Blog).where(models.Blog.id==id)
    blog = session.scalars(stmt).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    return blog

def delete_blog(id: int, session: Session):
    blog = session.scalars(select(models.Blog).where(models.Blog.id==id)).first()
    if not blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    
    stmt = delete(models.Blog).where(models.Blog.id == id)
    session.execute(stmt)
    session.commit()
    return {'deleted'}

def update_blog(id:int, request:Request, session:Session):
    blog = session.scalars(select(models.Blog).where(models.Blog.id==id)).first()
    if not blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    
    stmt = update(models.Blog).where(models.Blog.id == id).values(title=request.title, body=request.body)
    session.execute(stmt)
    session.commit()
    blog = session.scalars(select(models.Blog).where(models.Blog.id==id)).first()
    return blog