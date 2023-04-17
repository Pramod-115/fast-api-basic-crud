from fastapi import FastAPI
from pydantic import BaseModel

class Blog(BaseModel):
    name: str
    content: str

app = FastAPI()

@app.put('/blogs')
def create_blog(blog: Blog):
    return {"message": 'Blog created', "data": blog}

@app.get('/blogs')
def get_Blogs():
    return {"blogs": 'Lists of Blogs'}