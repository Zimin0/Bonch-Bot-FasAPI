from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base_time_period import BaseTimePeriod

class Session(BaseTimePeriod):
    __tablename__ = "sessions"
    tg_tag = Column(Integer, ForeignKey("user.tg_tag"), nullable=False)

    user = relationship("User")