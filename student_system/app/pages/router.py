from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.students.router import get_all_students


pages_router = APIRouter(prefix='/pages', tags=['Страницы'])
templates = Jinja2Templates(directory='app/templates')

@pages_router.get('/students')
async def get_students(request: Request, all_students = Depends(get_all_students)):
    return templates.TemplateResponse(name='students.html',context={'request':request,
                                                                    'students': all_students})

