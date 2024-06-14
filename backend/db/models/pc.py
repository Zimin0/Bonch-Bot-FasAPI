from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

class PC(Base):
    __tablename__ = "pcs"
    id = Column(Integer, primary_key=True)
    physical_number = Column(Integer, unique=True, index=True)
    ready_to_use = Column(Boolean, default=True)

    time_periods = relationship("TimePeriod", back_populates="computer")
    pc_sessions = relationship("PC_Session", back_populates="computer")