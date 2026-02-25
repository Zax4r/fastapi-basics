from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.schemas import SStudent, SStudentAdd, SStudentUpdAddr
from app.students.rb import RBStudent
from typing import List

router_students = APIRouter(prefix='/students', tags=['Работа со студентами'])

@router_students.post('/add', response_model = dict)
async def add_student(student: SStudentAdd):
    check = await StudentDAO.add_student(student.dict())
    if check:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}

@router_students.delete('/delete/{student_id}')
async def delete_student(student_id: int):
    check = await StudentDAO.delete_student_by_id(student_id)
    if check:
        return {'message':f'Студент с id {student_id} удалён'}
    else:
        return {'message':'Такой студент не найден'}

@router_students.put('/update')
async def update_student(student: SStudentUpdAddr):
    check = await StudentDAO.put(filter_by={'first_name':student.first_name,
                                            'last_name':student.last_name,
                                            'phone_number':student.phone_number},
                                            address = student.address)
    if check:
        return {'message':'Студент обновлён'}
    else:
        return {'message':'Такого студента не найдено'}

@router_students.get('/', response_model=List[SStudent])
async def get_all_students(request_body: RBStudent = Depends()):
    students = await StudentDAO.find_all(**request_body.to_dict())
    return students


@router_students.get('/by_filter', response_model=SStudent | dict)
async def get_student_by_filter(request_body: RBStudent= Depends()):
    res = await StudentDAO.find_one_or_none_by_id(**request_body.to_dict())
    if res is None:
        return {'message':f'Студент с такими параметрами не найден'}
    return res


@router_students.get('/{id}', response_model=SStudent | dict)
async def get_student_by_id(student_id: int):
    res = await StudentDAO.find_full_data(student_id)
    if res is None:
        return {'message':f'Студент с ID:   {student_id} не найден'}
    return res