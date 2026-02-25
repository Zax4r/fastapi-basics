from fastapi import APIRouter
from app.majors.dao import MajorDAO
from app.majors.schemas import SMajorAdd, SMajorUpdDesc, SMajor
from typing import List

router_majors = APIRouter(prefix='/majors',tags = ['Работа с факультетами'] )


@router_majors.get('/', response_model = List[SMajor])
async def get_all():
    majors = await MajorDAO.find_all()
    return majors

@router_majors.post('/add', response_model=dict)
async def add_major(major: SMajorAdd):
    check = await MajorDAO.add(**major.dict())
    if check:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        return {"message": "Ошибка при добавлении факультета!"} 
    
@router_majors.put('/update_description/', response_model=dict)
async def update_description(major: SMajorUpdDesc):
    rows_updated = await MajorDAO.put(filter_by={'major_name': major.major_name},
                                      major_description = major.major_description)
    if rows_updated:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        return {"message": "Ошибка при обновлении описания факультета!"}
    
@router_majors.delete('/delete/{major_id}')
async def delete_major(major_id: int)-> dict:
    check = await MajorDAO.delete(id=major_id)
    if check:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        return {"message": "Ошибка при удалении факультета!"}