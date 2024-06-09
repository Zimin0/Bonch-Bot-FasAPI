from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    tg_tag: str = Field(..., pattern=r"@\w+")
    password: str = Field(..., min_length=4)

class UserGet(BaseModel):
    id: int 
    email: EmailStr
    tg_tag: Optional[str]
    is_active: bool
    avatar: Optional[str]
    is_superuser: bool

    class Config(): # tells pydantic to convert even non dict obj to json
        orm_mode = True
        from_attributes = True