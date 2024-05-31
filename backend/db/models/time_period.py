from db.models.base_time_period import BaseTimePeriod
from db.base_class import Base

class TimePeriod(BaseTimePeriod, Base):
    __tablename__ = "time_periods"