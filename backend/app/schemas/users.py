from pydantic import BaseModel, EmailStr, Field
from datetime import *


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserShort(BaseModel):
    id: int
    username: str
    avatar: str
    is_active: bool
    rating: float

class UserFull(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    full_name: str
    avatar: str
    bio: str
    rating: float
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    avatar: str
    bio: str

class UserUpdatePassword(BaseModel):
    password: str