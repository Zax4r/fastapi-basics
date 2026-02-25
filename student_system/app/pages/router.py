from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.templating import Jinja2Templates
from app.students.router import get_all_students, get_student_by_id
from app.users.router import get_me
import shutil


pages_router = APIRouter(prefix='/pages', tags=['Страницы'])
templates = Jinja2Templates(directory='app/templates')

@pages_router.get('/students')
async def get_students(request: Request, all_students = Depends(get_all_students)):
    return templates.TemplateResponse(name='students.html',context={'request':request,
                                                                    'students': all_students})

@pages_router.post('/add_photo')
async def add_student_photo(file: UploadFile, image_name:str):
    with open(f'app/static/images/{image_name}.webp','wb+') as photo_file:
        shutil.copyfileobj(file.file, photo_file)

@pages_router.get('/students/{student_id}')
async def get_students_html(request: Request, student=Depends(get_student_by_id)):
    return templates.TemplateResponse(name='student.html',
                                      context={'request': request, 'student': student})
@pages_router.get('/register')
async def get_register(request: Request):
    return templates.TemplateResponse(name='register.html', context={'request': request})

@pages_router.get('/login')
async def get_login(request: Request):
    return templates.TemplateResponse(name='login.html', context={'request': request})

@pages_router.get('/profile')
async def get_my_profile(request: Request, profile=Depends(get_me)):
    return templates.TemplateResponse(name='profile.html',
                                      context={'request': request, 'profile': profile})