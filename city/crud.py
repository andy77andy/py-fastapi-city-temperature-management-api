from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def read_all_cities(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def create_city(db: AsyncSession, city_data: schemas.CityCreate):
    query = insert(models.City).values(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city_data.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db=db, city_id=city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return {"message": "City deleted successfully"}
    raise HTTPException(status_code=400, detail="We haven't such book in base")


async def update_city(db: AsyncSession, city_id: int, updated_city: schemas.CityUpdate):

    city = await get_city_by_id(db=db, city_id=city_id)
    if city:
        for attr, value in updated_city.model_dump().items():
            setattr(city, attr, value)
        await db.commit()
        await db.refresh(city)
        return city
    raise HTTPException(status_code=400, detail="We haven't such book in base")
