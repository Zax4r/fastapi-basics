from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.tasks import router as task_router
from app.routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)


@app.get('/')
async def root():
    return {'message':'Hello World'}
