from pydantic import BaseModel

class SettingBase(BaseModel):
    """ Родительская схема. """
    name: str
    slug: str
    value: str

class SettingCreate(SettingBase):
    ...

class SettingUpdate(SettingBase):
    ...

class SettingGet(SettingBase):
    id: int
