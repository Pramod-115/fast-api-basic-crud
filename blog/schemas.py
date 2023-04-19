from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str
    user_id: int

class UserBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True


class UpdateBlog(Blog):
    class Config():
        total = False

# UpdateBlog = Blog.partial_model()

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True

class ShowUserBlog(BaseModel):
    name: str
    email: str
    blogs: List[UserBlog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        orm_mode = True

class login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
