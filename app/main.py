from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, blog

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Blog")

app.include_router(user.router)
app.include_router(blog.router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Blog!"}
