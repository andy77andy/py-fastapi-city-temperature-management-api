from fastapi import FastAPI

from temperature import router as temperature_router
from city import router as cities_router

app = FastAPI()

app.include_router(temperature_router.router)
app.include_router(cities_router.router)
