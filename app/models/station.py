from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    aqi = Column(Float)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    co = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
