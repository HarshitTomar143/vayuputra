from pydantic import BaseModel
from typing import Optional


class LocationRequest(BaseModel):
    lat: float
    lon: float


class AQIResponse(BaseModel):
    latitude: float
    longitude: float

    predicted_aqi: float
    nearest_station: str

    pm25: Optional[float]
    pm10: Optional[float]
    co: Optional[float]
    no2: Optional[float]
    o3: Optional[float]
    humidity: Optional[float]
