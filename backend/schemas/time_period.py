from pydantic import BaseModel
from datetime import time
from enum import Enum

class StatusEnum(str, Enum):
    booked = "booked"
    free = "free"
    break_between_bookings = "break_between_bookings"

class TimePeriodBase(BaseModel):
    time_start: time
    time_end: time
    computer_id: int
    status: StatusEnum = StatusEnum.free

    class Config:
        orm_mode = True

class TimePeriodCreate(TimePeriodBase):
    pass

class TimePeriodUpdate(TimePeriodBase):
    pass

class TimePeriodGet(TimePeriodBase):
    id: int
