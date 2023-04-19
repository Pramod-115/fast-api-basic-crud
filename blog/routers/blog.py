from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_Blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

@router.post('/blogs', status_code=status.HTTP_201_CREATED)
def create_blog(body: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=body.title, body=body.body, user_id=body.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blogs/{id}', response_model=schemas.ShowBlog, status_code=200)
def get_blog(id: int, db: Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} id not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return blog

@router.put('/blogs/{id}',  status_code=status.HTTP_200_OK)
def update_blog(id: int, body: schemas.UpdateBlog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} id not found.")
    blog.update(body)
    db.commit()
    return 'Updated'


@router.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} id not found.")
    blog.delete(synchronize_session=False)
    db.commit()

