from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    tg_tag: str = None
    password: str = Field(..., min_length=4)

class ShowUser(BaseModel):
    id: int 
    email: EmailStr
    is_active: bool

    class Config(): # tells pydantic to convert even non dict obj to json
        orm_mode = True