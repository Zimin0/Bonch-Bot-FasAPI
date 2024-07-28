from sqlalchemy import Column, Enum
from db.models.base_time_period import BaseTimePeriod
from db.base_class import Base
from enum import Enum as PyEnum
from datetime import time
from sqlalchemy.orm import Session
from datetime import datetime

class StatusEnum(PyEnum):
    booked = "booked"
    free = "free"
    break_between_bookings = "break_between_bookings"

class TimePeriod(BaseTimePeriod, Base):
    __tablename__ = "time_periods"
    
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.free)

    # @property.setter
    # def status(self, value:str):
    #     all_statuses = [stat.value for stat in StatusEnum]
    #     if value not in all_statuses:
    #         raise ValueError(f"Invalid status for TimePeriod. Valid are: {', '.join(all_statuses)}")
    #     self._status = value

    @property
    def is_free(self):
        """ Свободен ли временной промежуток. """
        return self.status == StatusEnum.free

    def is_it_in_time_gap(self, start_session:time, end_session:time) -> bool:
        """ Проверяет, входит ли временной промежуток в сессию. """
        return (self.time_start >= start_session) and (self.time_end <= end_session) 
    
    @staticmethod
    def count_session_length(time_start: time, time_end: time) -> int:
        """Вычисляет длину промежутка в секундах."""
        time_format = '%H:%M'
        
        # Convert time objects to strings
        time_start_str = time_start.strftime(time_format)
        time_end_str = time_end.strftime(time_format)
        
        start = datetime.strptime(time_start_str, time_format)
        end = datetime.strptime(time_end_str, time_format)
        delta = end - start
        return int(delta.total_seconds())

    @staticmethod
    def set_status_to_time_periods(db:Session, time_periods:list["TimePeriod"], status:str, start:time, end:time, mark_post_last_as_break:bool=False) -> None:
        """
        Устанавливает нужный статус всем промежутками из промежутка start:end. 
        status: [free, booked, break_between_bookings]
        mark_post_last_as_break: поставит статус break_between_bookings промежутку следующему после последнего промежутка.
        """
        all_statuses = [stat.value for stat in StatusEnum]
        if status not in all_statuses:
            raise ValueError(f"Invalid status for TimePeriod. Valid are: {', '.join(all_statuses)}")

        is_session_started = False
        for period in time_periods:
            if period.is_it_in_time_gap(start, end):
                is_session_started = True
                period.status = status
                db.commit()
                db.refresh(period)
            else:
                if is_session_started:
                    if mark_post_last_as_break: # Занимаем последний промежут для перерыва только когда бронируем.
                        period.status = "break_between_bookings"
                    db.commit()
                    db.refresh(period)
                    break

            
