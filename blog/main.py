from fastapi import FastAPI
from . import schemas,models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.put('/blogs')
def create_blog(blog: schemas.Blog):
    return {"message": 'Blog created', "data": blog}

@app.get('/blogs')
def get_Blogs():
    return {"blogs": 'Lists of Blogs'}