from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class UpdateBlog(Blog):
    class Config():
        partial = True

# UpdateBlog = Blog.partial_model()

class ShowBlog(BaseModel):
    title: str
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str