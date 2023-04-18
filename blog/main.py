from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.post('/blogs', status_code=status.HTTP_201_CREATED)
def create_blog(body: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=body.title, body=body.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_Blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

@app.get('/blogs/{id}', response_model=schemas.ShowBlog, status_code=200)
def get_blog(id: int, db: Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} id not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return blog

@app.put('/blogs/{id}',  status_code=status.HTTP_200_OK)
def update_blog(id: int, body: schemas.UpdateBlog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} id not found.")
    blog.update(body)
    db.commit()
    return 'Updated'


@app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} id not found.")
    blog.delete(synchronize_session=False)
    db.commit()

@app.post('/user', response_model= schemas.ShowUser)
def create_user(body: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = body.name, email = body.email, password = body.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user