from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserInDb(UserBase):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    hashed_password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    email: Optional[EmailStr]
    