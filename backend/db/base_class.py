from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str

    # @declared_attr # чтобы имя таблицы совпадало с именем класса
    # def __tablename__(cls) -> str:
    #     return cls.__name__.lower()