from fastapi import FastAPI
import os
import logging
from app.students.router import router_students
from app.majors.router import router_majors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
path_to_json = os.path.join(parent_dir,'students.json')

app = FastAPI()

app.include_router(router_students)
app.include_router(router_majors)

