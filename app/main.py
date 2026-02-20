from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.db import engine
from app.models.station import Base
from app.services.fetch_service import fetch_and_store_stations

from app.schemas import LocationRequest, AQIResponse

from app.services.spatial_services import get_weighted_aqi

from app.schemas import LocationRequest, AQIResponse

app = FastAPI(title="VAYUPUTRA ML API")

from app.services.spatial_services import get_nearest_station_data

# Initialize scheduler
scheduler = BackgroundScheduler()


@app.on_event("startup")
def startup_event():

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("Fetching initial AQI data...")
    fetch_and_store_stations()

    print("Starting scheduler...")
    scheduler.add_job(fetch_and_store_stations, "interval", hours=1)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


@app.post("/aqii")
def get_aqi(request: LocationRequest) :
    result = get_nearest_station_data(request.lat, request.lon)

    if not result:
        return {"error": "No station data available"}

    return {
        "latitude": request.lat,
        "longitude": request.lon,
        **result
    }

@app.post("/aqi")
def get_aqi(request: LocationRequest) :
    result = get_weighted_aqi(request.lat, request.lon)

    if not result:
        return {"error": "No station data available"}

    return {
        "latitude": request.lat,
        "longitude": request.lon,
        **result
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}