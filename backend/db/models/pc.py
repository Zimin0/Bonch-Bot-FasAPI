from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

class PC(Base):
    __tablename__ = "pcs"
    id = Column(Integer, primary_key=True, index=True)
    physical_number = Column(Integer, unique=True)
    ready_to_use = Column(Boolean, default=True)