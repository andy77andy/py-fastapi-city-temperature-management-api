import datetime

from pydantic import BaseModel
from typing_extensions import List


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    additional_info: str


class CityDetail(CityBase):
    id: int
    additional_info: str


class Config:
    from_attributes = True


class CityUpdate(CityBase):
    name: str
    additional_info: str | None = None
