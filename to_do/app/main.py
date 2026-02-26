from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.tasks import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)


@app.get('/')
async def root():
    return {'message':'Hello World'}
