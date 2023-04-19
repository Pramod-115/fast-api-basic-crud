from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash

router = APIRouter()

@router.post('/user', response_model= schemas.ShowUser)
def create_user(body: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = body.name, email = body.email, password = Hash.encrypt(body.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/user/{id}', response_model=schemas.ShowUserBlog)
def get_single_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user