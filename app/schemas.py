from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Union, Optional


class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str

class User(UserCreate):
    id:int
    created_on:datetime
    class Config:
        orm_mode=True


class ReferralCreate(BaseModel):
    referral_code: str


class Referral(ReferralCreate):
    id: int
    is_active: Optional[bool] = True
    created_on: Optional[datetime] = None

    class Config:
        orm_mode = True


class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
