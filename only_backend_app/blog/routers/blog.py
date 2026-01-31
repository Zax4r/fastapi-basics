from fastapi import APIRouter, Depends, status
from .. import schemas
from typing import List, Annotated
from ..database import get_session
from ..repository import blog
from ..oauth2 import get_current_user

router = APIRouter(prefix='/blog', tags=['blog'])


@router.post('/', status_code=201)
def post_blog(current_user: Annotated[schemas.User, Depends(get_current_user)],request: schemas.Blog,session=Depends(get_session)):
    new_blog = blog.create(request,session, current_user)
    return new_blog

@router.get('/', response_model=List[schemas.ShowBlog])  
def get_all_blogs(session=Depends(get_session)):
    return blog.get_all(session)

@router.get('/{id}',status_code=200, response_model=schemas.ShowBlog)
def get_blog_by_id(current_user: Annotated[schemas.User, Depends(get_current_user)],id: int,session=Depends(get_session)):
    new_blog = blog.get_by_id(id,session)
    return new_blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_by_id(current_user: Annotated[schemas.User, Depends(get_current_user)], id: int, session = Depends(get_session)):
    return blog.delete_blog(id,session)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def put_blog_by_id(current_user: Annotated[schemas.User, Depends(get_current_user)], id: int,request: schemas.Blog, session = Depends(get_session)):
    return blog.update_blog(id,request,session)