from pydantic import BaseModel, Field, validator

class PCCreate(BaseModel):
    physical_number: int = Field(..., gt=0)
    ready_to_use: bool

    # @validator("physical_number")
    # def check_physical_number(cls, value):
    #     if value < 1:
    #         raise ValueError("Physical number cannot be negative")
    #     return value

class PCGet(BaseModel):
    id: int
    physical_number: int = Field(..., gt=0)
    ready_to_use: bool

    class Config:
        orm_mode = True

class PCUpdate(BaseModel):
    physical_number: int = Field(None, gt=0, description="The physical number of the PC")
    ready_to_use: bool = Field(None, description="The availability status of the PC")

    @validator("physical_number", pre=True, always=True)
    def check_physical_number(cls, value):
        if value is not None and value < 1:
            raise ValueError("Physical number cannot be negative")
        return value
