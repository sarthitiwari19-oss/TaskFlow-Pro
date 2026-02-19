from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class TaskSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    published: bool = True # Pehle yahan 'completed' tha, ab 'published' hai
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr 
    password: str = Field(..., min_length=6, max_length=50)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True