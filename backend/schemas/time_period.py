from pydantic import BaseModel
from datetime import time

class TimePeriodBase(BaseModel):
    time_start: time
    time_end: time
    computer_id: int

class TimePeriodCreate(TimePeriodBase):
    pass

class TimePeriodUpdate(TimePeriodBase):
    pass

class TimePeriodGet(TimePeriodBase):
    id: int

    class Config:
        orm_mode = True
