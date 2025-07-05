from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import PriorityEnum

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    deadline: Optional[str] = None
    icon: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    deadline: Optional[str] = None
    icon: Optional[str] = None

class Todo(TodoBase):
    id: int
    completed: bool
    google_calendar_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
