from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityBase])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.read_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city_data: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db=db, city_data=city_data)


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city:
        return await db_city
    raise HTTPException(status_code=400, detail="We haven't such book in base")


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    query = await crud.delete_city(db=db, city_id=city_id)
    return query


@router.patch("/cities/{city_id}/", response_model=schemas.CityUpdate)
async def update_city(city_data: schemas.CityUpdate, city_id: int, db: AsyncSession = Depends(get_db)):
    query = await crud.update_city(db=db, city_id=city_id, updated_city=city_data)
    return query

