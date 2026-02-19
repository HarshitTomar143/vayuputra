from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    aqi = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
