from fastapi import FastAPI
import blog.models as models
from blog.database import engine
from blog.routers import blog,user,login


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)
models.Base.metadata.create_all(bind=engine)

@app.get('/')
def root():
    return {'hello':'world'}