from pydantic import BaseModel
from datetime import time

class SessionGet(BaseModel):
    id: int
    time_start: time
    time_end: time
    computer_id: int

    class Config:
        orm_mode = True

class SessionCreate(BaseModel):
    time_start: time
    time_end: time
    computer_id: int
    tg_tag: str

    class Config:
        orm_mode = True
