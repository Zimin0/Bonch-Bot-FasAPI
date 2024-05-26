from sqlalchemy import Column, String, Integer
from db.base_class import Base 

class Setting(Base):
    """ Кастомные настройки приложения. """
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)

 