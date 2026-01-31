from .. import models, schemas
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..utils import verify_password
from ..token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

def login(request: OAuth2PasswordRequestForm, session: Session):
    stmt = select(models.User).where(models.User.email == request.username)
    user = session.scalars(stmt).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'No such username {request.username}')
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Incorrect password')

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

    