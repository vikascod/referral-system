from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app import models, schemas
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user
import string
import secrets


router = APIRouter(
    tags=['Referral'],
)


def generate_random_code(length=7):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

@router.get('/referral-code')
async def generate_referral_code(db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    user = db.query(models.User).filter_by(id=current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    if user.referral:
        return {'referral_code':user.referral.referral_code}
    referral_code = generate_random_code()
    new_referral = models.Referral(referral_code=referral_code, user_id=user.id)
    db.add(new_referral)
    db.commit()
    return {'referral_code':referral_code}




@router.post('/referral')
async def redeem_referral_code(referral:schemas.ReferralCreate, db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    referral_db = db.query(models.Referral).filter_by(referral_code=referral.referral_code).first()

    if not referral_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referral not found")

    referrer = db.query(models.User).filter(models.User.referral.has(id=referral_db.id)).first()

    if not referrer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referrer not found")

    referred_user = db.query(models.User).filter_by(email=current_user.email).first()

    if not referred_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referred user not found")

    referral_db.rewards += 100
    referred_user.referral.rewards += 50
    # referral_db.is_active = False
    db.commit()
    return {"message": "Referral successfully"}


@router.post('/check-referral-code')
async def check_referral_code(referral_code:str, db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    referral_db = db.query(models.Referral).filter_by(referral_code=referral_code).first()

    if not referral_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid referral code")
    
    return {"Message":"Referral code is valid"}