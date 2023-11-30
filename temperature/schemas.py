import datetime

from pydantic import BaseModel
from typing_extensions import List

from city.schemas import CityBase


class TemperatureBase(BaseModel):
    date_time: str
    temperature: float
    city_id: int


class TemperatureList(TemperatureBase):
    city: CityBase

#
# class TemperatureList(TemperatureBase):
#     city: CityBase
#
#
# class TemperatureCreate(TemperatureBase):
#     id: int
#     city_id: int
