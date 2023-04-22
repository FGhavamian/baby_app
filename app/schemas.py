from typing import Optional

from datetime import datetime
from pydantic import BaseModel, EmailStr


class AmountBase(BaseModel):
    value: int
    baby_id: int


class AmountOut(AmountBase):
    id: int
    created_at: datetime


class AmountSum(BaseModel):
    created_at = datetime
    amount: int


class BabyBase(BaseModel):
    name: str


class BabyOut(BabyBase):
    id: int
    created_at: datetime
    user_id: int


class UserBase(BaseModel):
    email: EmailStr


class UserOut(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
