from pydantic import BaseModel, Field, validator

class PCCreate(BaseModel):
    physical_number: int
    ready_to_use: bool

    @validator("physical_number")
    def check_physical_number(cls, value):
        if value < 1:
            raise ValueError("Physical number cannot be negative")
        return value

class PCGet(BaseModel):
    id: int
    physical_number: int
    ready_to_use: bool