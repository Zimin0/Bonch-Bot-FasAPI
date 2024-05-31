from sqlalchemy import Column, Enum
from db.models.base_time_period import BaseTimePeriod
from db.base_class import Base
import enum

class StatusEnum(enum.Enum):
    booked = "Забронировано"
    free = "Свободно"
    break_between_bookings = "Перерыв между бронями"

class TimePeriod(BaseTimePeriod, Base):
    __tablename__ = "time_periods"
    
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.free)
