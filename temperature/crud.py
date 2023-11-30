import datetime
import httpx
import json
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas
from city.models import City

API_KEY = "c9793d04b61fff262cc39a32f02e565e"


async def get_all_cities_with_temperature(db: AsyncSession):
    query = select(models.Temperature).all()
    temperature_list = await db.execute(query)
    return [temperature for temperature in temperature_list.fetchall()]


# async def create_temperature(db: AsyncSession, temp_data: schemas.TemperatureBase):
#     query = insert(models.Temperature).values(
#         city_id=temp_data.city_id,
#         date_time=datetime.datetime.now(),
#         temperature=temp_data.temperature
#     )
#     result = await db.execute(query)
#     await db.commit()
#     resp = {**temp_data.model_dump(), "id": result.lastrowid}
#     return resp


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = select(models.Temperature).filter(models.Temperature.city_id == city_id)
    city_temperature = await db.execute(query)
    if city_temperature:
        return city_temperature.scalar()
    raise HTTPException(status_code=400, detail="We haven't such city in base")


async def update_temperatures(db: AsyncSession):
    cities = await db.execute(select(City))
    city_list = cities.scalars().all()
    async with httpx.AsyncClient() as client:
        for city in city_list:
            url = F"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={API_KEY}"
            response = await client.get(url)
            db_temperature = select(models.Temperature).filter(models.Temperature.city_id == city.id)
            if db_temperature is not None:
                db_temperature.temperature = response.json()["main"]["temp"]
            else:
                db_temperature = models.Temperature(
                    city_id=city.id,
                    date_time=datetime.datetime.now(),
                    temperature=response.json()["main"]["temp"]
                )
                db.add(db_temperature)
            await db.commit()
            # await db.refresh(db_temperature)
