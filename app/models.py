from app.database import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    referral = relationship("Referral", uselist=False, back_populates='user')


class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(Integer, primary_key=True)
    referral_code = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rewards = Column(Integer, default=0)

    user = relationship(User, back_populates="referral")
