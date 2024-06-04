from sqlalchemy import Column, Enum
from db.models.base_time_period import BaseTimePeriod
from db.base_class import Base
from enum import Enum as PyEnum
from datetime import time
from sqlalchemy.orm import Session

class StatusEnum(PyEnum):
    booked = "booked"
    free = "free"
    break_between_bookings = "break_between_bookings"

class TimePeriod(BaseTimePeriod, Base):
    __tablename__ = "time_periods"
    
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.free)

    def is_it_in_time_gap(self, start_session:time, end_session:time) -> bool:
        """ Проверяет, входит ли временной промежуток в сессию. """
        return (self.time_start >= start_session) and (self.time_end <= end_session) 

    @staticmethod
    def set_status_to_time_periods(db:Session, time_periods:list, status:str, start:time, end:time):
        """
        Устанавливает нужный статус всем промежутками из промежутка start:end. 
        status: [free, booked, break_between_bookings]
        """
        all_statuses = [stat.value for stat in StatusEnum]
        if status not in all_statuses:
            raise ValueError(f"Invalid status for TimePeriod. Valid are: {', '.join(all_statuses)}")
        
        for period in time_periods:
            if period.is_it_in_time_gap(start, end):
                period.status = status
                db.commit()
                db.refresh(period)

            
