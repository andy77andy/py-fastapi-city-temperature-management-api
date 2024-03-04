import datetime
import httpx
import json
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from city.crud import read_all_cities
from temperature.models import Temperature

load_dotenv()

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas
from city.models import City

# API_KEY = "c9793d04b61fff262cc39a32f02e565e"
API_KEY = "4b01e11299a94190b73121724230108"


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


# async def get_all_cities(db: AsyncSession):
#     cities = await db.execute(select(City))
#
#     city_list = cities.scalars().all()
#     return city_list


async def create_update_temperatures(db: AsyncSession):
    # cities = await db.execute(select(City))
    #
    # city_list = cities.scalars().all()
    # # city_list = await get_all_cities(db)
    query = select(City)
    city_list = await db.execute(query)
    print(city_list)
    async with httpx.AsyncClient() as client:
        # # cities = await read_all_cities(db)
        # print(cities)
        for city in city_list:
            # url = F"https://api.openweathermap.org/data/2.5/weather?q={city[0].name}&appid={API_KEY}"
            url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city[0].name}&aqi=no"
            response = await client.get(url)
            # db_temperature = models.Temperature(
            #     city_id=city[0].id,
            #     date_time=datetime.datetime.now(),
            #     temperature=response.json()["main"]["temp"]
            # )
            # db.add(db_temperature)
            # await db.commit()
            # await db.refresh(db_temperature)
            # if response.status_code == 200:
            #     db_temperature = await db.execute(select(models.Temperature).filter(models.Temperature.city_id == city[0].id))
            #     if db_temperature is not None:
            #         db_temperature.temperature = response.json()["main"]["temp"]
            #         await db.commit()
            #         await db.refresh(db_temperature)
            #     else:
            #         db_temperature = models.Temperature(
            #             city_id=city.id,
            #             date_time=datetime.datetime.now(),
            #             temperature=response.json()["main"]["temp"]
            #         )
            #         db.add(db_temperature)
            #         await db.commit()
            if response.status_code == 200:
                data = response.json()
                temperature = data["current"]["temp_c"]
                temperature_instance = models.Temperature(
                    city_id=city[0].id,
                    temperature=temperature,
                    date_time=datetime.datetime.now()
                )
                db.add(temperature_instance)
            else:
                return f"We haven't {city.name} in our base."
            await db.commit()
            await db.refresh(temperature_instance)
