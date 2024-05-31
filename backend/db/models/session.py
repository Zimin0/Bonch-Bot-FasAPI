from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.models.base_time_period import BaseTimePeriod
from db.base_class import Base 

class PC_Session(BaseTimePeriod, Base):
    """ Игровые сессии за ПК. """
    __tablename__ = "pc_sessions"
    tg_tag = Column(String, ForeignKey("users.tg_tag"), nullable=False)

    user = relationship("User")