from app.db import SessionLocal
from app.models.station import Station
from app.utils.data_loader import fetch_station_data


def fetch_and_store_stations():
    print("Fetching station data...")

    df = fetch_station_data()

    db = SessionLocal()

    for _, row in df.iterrows():

        station = Station(
            name=row["name"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            aqi=row["aqi"],
            pm25=row["pm25"],
            pm10=row["pm10"],
            co=row["co"],
            no2=row["no2"],
            o3=row["o3"],
            humidity=row["humidity"]
        )

        db.add(station)

    db.commit()
    db.close()

    print("Stations stored in DB.")
