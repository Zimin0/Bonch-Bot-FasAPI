from db.base_class import Base
from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship

class BaseTimePeriod(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, unique=True)
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)
    computer_id = Column(Integer, ForeignKey("computers.id"), nullable=False)

    computer = relationship("Computer")