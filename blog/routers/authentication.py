from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..token import create_access_token

router = APIRouter(
    tags=["Athentication"]
)

@router.post('/login')
def login(body: schemas.login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with email {body.username} not found")
    if not Hash.verify(user.password, body.password):
        raise HTTPException(status_code= status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Invalid password for {body.username}")
    token = create_access_token( data={"sub": body.username}, expires_delta=None)
    return {"bearer" : token}
