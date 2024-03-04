from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
async def read_temperatures(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities_with_temperature(db=db)


@router.post("/temperatures/", response_model=schemas.TemperatureBase)
async def update_temperature(
    db: AsyncSession = Depends(get_db),

):
    return await crud.create_update_temperatures(db=db)


@router.get("/temperatures/{city_id}/", response_model=schemas.TemperatureList)
async def update_temperature(
    city_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperature_by_city_id(db=db, city_id=city_id)
