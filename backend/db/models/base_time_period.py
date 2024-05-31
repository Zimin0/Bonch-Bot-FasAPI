# db/models/base_time_period.py
from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import declared_attr, relationship, declarative_mixin

@declarative_mixin
class BaseTimePeriod:
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True, unique=True)

    @declared_attr
    def time_start(cls):
        return Column(Time, nullable=False)

    @declared_attr
    def time_end(cls):
        return Column(Time, nullable=False)

    @declared_attr
    def computer_id(cls):
        return Column(Integer, ForeignKey("pcs.id"), nullable=False)

    @declared_attr
    def computer(cls):
        return relationship("PC")
