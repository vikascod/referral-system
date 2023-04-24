from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas, models
from fastapi.security import OAuth2PasswordRequestForm
from app.oauth2 import create_access_token
from werkzeug.security import check_password_hash


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login/", response_model=schemas.Token)
async def login_for_access_token(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not found")
    
    if not check_password_hash(user.password, user_credential.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

