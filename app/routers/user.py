from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from werkzeug.security import generate_password_hash

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

@router.post('/signup/', status_code=status.HTTP_201_CREATED)
async def create_user(user:schemas.UserCreate, db:Session=Depends(database.get_db)):
    hashed_password = generate_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


