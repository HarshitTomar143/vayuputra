from app.utils.data_loader import fetch_station_data
from app.db import SessionLocal
from app.models.station import Station


def fetch_and_store_stations():

    print("Fetching station data...")

    df = fetch_station_data()

    db = SessionLocal()

    for _, row in df.iterrows():
        station = Station(
            latitude=row["latitude"],
            longitude=row["longitude"],
            aqi=row["value"]
        )
        db.add(station)

    db.commit()
    db.close()

    print("Stations stored in DB.")
