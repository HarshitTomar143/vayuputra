from pydantic import BaseModel

class LocationRequest(BaseModel):
    lat: float
    lon: float

class AQIResponse(BaseModel):
    latitude: float
    longitude: float
    predicted_pm25: float
