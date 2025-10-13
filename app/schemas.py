from pydantic import BaseModel, Field,EmailStr
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True

