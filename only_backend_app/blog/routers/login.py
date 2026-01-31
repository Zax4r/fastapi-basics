from fastapi import APIRouter, Depends
from .. import schemas
from ..database import get_session
from sqlalchemy.orm import Session
from ..repository import loginr
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter(
    tags=['login']
)

@router.post('/login')
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    return loginr.login(request,session)