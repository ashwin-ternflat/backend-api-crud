from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: Optional[str]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
