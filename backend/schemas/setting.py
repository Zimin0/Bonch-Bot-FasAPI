from pydantic import BaseModel

class SettingCreate(BaseModel):
    name: str
    slug: str
    value: str

class SettingUpdate(BaseModel):
    name: str
    slug: str 
    value: str