from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserAuth
from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token
from app.users.models import User
from app.users.dependecies import get_current_user, get_current_admin_user


users_router = APIRouter(prefix='/auth',tags=['Авторизация'])

@users_router.post('/register')
async def register_user(user_data: SUserRegister):
    user = await UserDAO.find_one_or_none_by_id(email = user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        ) 
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@users_router.get('/all_users/')
async def get_all_users(admin = Depends(get_current_admin_user)):
    if admin:
        return await UserDAO.find_all()
    return []

@users_router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(user_data.email,user_data.password)
    if not check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({'sub':str(check.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}

@users_router.get('/me')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@users_router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}