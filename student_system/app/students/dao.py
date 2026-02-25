from app.dao.base import BaseDAO
from app.students.models import Student
from app.majors.models import Major
from app.database import async_session_maker
from sqlalchemy import select, delete, update, insert, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload


class StudentDAO(BaseDAO):

    model = Student
    
    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id = student_id)
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            if student_info is None:
                return None
            
            student_dict = student_info.to_dict()
            student_dict['major'] = student_info.major.major_name
            return student_dict
        
    @classmethod
    async def add_student(cls, student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = Student(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id
        
    @event.listens_for(Student,'after_insert')
    def recieve_after_insert(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(students_count = Major.students_count + 1)
        )


    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = select(Student).where(Student.id == student_id)
                result = await session.execute(stmt)
                student_to_delete = result.scalar_one_or_none()
                
                if student_to_delete is None:
                    return None
                
                await session.delete(student_to_delete)
                
                await session.commit()
                return student_id
    
    @event.listens_for(Student,'after_delete')
    def recieve_after_delete(mapper,connection,target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(students_count = Major.students_count-1)
        )
