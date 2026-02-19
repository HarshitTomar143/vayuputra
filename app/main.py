from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.db import engine
from app.models.station import Base
from app.services.fetch_service import fetch_and_store_stations

from app.schemas import LocationRequest, AQIResponse
from app.services.spatial_services import predict_pollution

from app.schemas import LocationRequest, AQIResponse

app = FastAPI(title="VAYUPUTRA ML API")

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


@app.post("/aqi", response_model=AQIResponse)
def get_aqi(request: LocationRequest):
    result = predict_pollution(request.lat, request.lon)

    return {
        "latitude": request.lat,
        "longitude": request.lon,
        **result
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}