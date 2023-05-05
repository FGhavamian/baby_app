from typing import Optional

from datetime import datetime
from pydantic import BaseModel, EmailStr


class Amount(BaseModel):
    id: int
    value: int
    baby_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AmountSum(BaseModel):
    created_at = datetime
    value: int


class BabyCreate(BaseModel):
    name: str


class Baby(BaseModel):
    id: int
    name: str
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
