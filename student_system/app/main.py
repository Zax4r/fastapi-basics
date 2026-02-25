from fastapi import FastAPI
import os
from app.students.router import students_router
from app.majors.router import majors_router
from app.users.router import users_router
from app.pages.router import pages_router


app = FastAPI()

app.include_router(students_router)
app.include_router(majors_router)
app.include_router(users_router)
app.include_router(pages_router)
