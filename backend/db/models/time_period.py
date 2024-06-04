from sqlalchemy import Column, Enum
from db.models.base_time_period import BaseTimePeriod
from db.base_class import Base
from enum import Enum as PyEnum

class StatusEnum(PyEnum):
    booked = "booked"
    free = "free"
    break_between_bookings = "break_between_bookings"

class TimePeriod(BaseTimePeriod, Base):
    __tablename__ = "time_periods"
    
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.free)
