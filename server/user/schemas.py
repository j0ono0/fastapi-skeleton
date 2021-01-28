from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .models import User, Group
    

#######################################
# User

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    #groups: List[Group] = []

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


#######################################
# Group
class GroupInDb(BaseModel):
    id: int
    name: str
    members: List[User] = []
    class Config:
        orm_mode = True

class Group(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class GroupCreate(BaseModel):
    name: str

class GroupUser(BaseModel):
    group_id: int
    user_id: int