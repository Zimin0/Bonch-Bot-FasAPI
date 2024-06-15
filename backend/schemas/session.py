from pydantic import BaseModel
from datetime import time

class SessionGet(BaseModel):
    id: int
    time_start: time
    time_end: time
    pc_physical_number: int
    tg_tag: str

    class Config:
        orm_mode = True

class SessionCreate(BaseModel):
    time_start: time
    time_end: time
    pc_physical_number: int
    tg_tag: str

    class Config:
        orm_mode = True

class SessionUpdate(BaseModel):
    time_start: time
    time_end: time
    pc_physical_number: int
    tg_tag: str

    class Config:
        orm_mode = True
