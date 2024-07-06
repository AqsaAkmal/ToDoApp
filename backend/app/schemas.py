# backend/app/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# Todo schemas
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoInDBBase(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class Todo(TodoInDBBase):
    pass

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    todos: List[Todo] = []

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
