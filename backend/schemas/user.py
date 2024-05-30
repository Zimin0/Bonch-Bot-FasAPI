from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    tg_tag: str = None
    password: str = Field(..., min_length=4)

class ShowUser(BaseModel):
    id: int 
    email: EmailStr
    tg_tag: Optional[str]
    is_active: bool
    is_superuser: bool

    class Config(): # tells pydantic to convert even non dict obj to json
        orm_mode = True
        from_attributes = True