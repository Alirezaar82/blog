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


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class PostResponse(PostBase):
    id: int
    author: UserResponse
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponseUpdate(PostBase):
    id: int
    author: UserResponse
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
