from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enables ORM compatibility for Django models
