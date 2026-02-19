import math
import pandas as pd
from app.db import SessionLocal
from app.models.station import Station


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_latest_station_snapshot():
    db = SessionLocal()

    latest_time = (
        db.query(Station.timestamp)
        .order_by(Station.timestamp.desc())
        .limit(1)
        .scalar()
    )

    if not latest_time:
        db.close()
        return pd.DataFrame()

    result = (
        db.query(Station)
        .filter(Station.timestamp == latest_time)
        .all()
    )

    db.close()

    df = pd.DataFrame([
        {
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "aqi": r.aqi,
            "pm25": r.pm25,
            "pm10": r.pm10,
            "co": r.co,
            "no2": r.no2,
            "o3": r.o3,
            "humidity": r.humidity
        }
        for r in result
    ])

    return df


def predict_pollution(lat: float, lon: float):
    df = get_latest_station_snapshot()

    if df.empty:
        return None

    df["distance"] = df.apply(
        lambda row: haversine(lat, lon, row["latitude"], row["longitude"]),
        axis=1
    )

    nearest = df.sort_values("distance").head(3)

    weights = []
    weighted_values = []

    for _, row in nearest.iterrows():

        if row["distance"] == 0:
            return {
                "predicted_aqi": float(row["aqi"]),
                "nearest_station": row["name"],
                "pm25": row["pm25"],
                "pm10": row["pm10"],
                "co": row["co"],
                "no2": row["no2"],
                "o3": row["o3"],
                "humidity": row["humidity"]
            }

        weight = 1 / (row["distance"] ** 2)
        weights.append(weight)
        weighted_values.append(weight * row["aqi"])

    predicted = sum(weighted_values) / sum(weights)

    nearest_station = nearest.iloc[0]

    return {
        "predicted_aqi": round(float(predicted), 2),
        "nearest_station": nearest_station["name"],
        "pm25": nearest_station["pm25"],
        "pm10": nearest_station["pm10"],
        "co": nearest_station["co"],
        "no2": nearest_station["no2"],
        "o3": nearest_station["o3"],
        "humidity": nearest_station["humidity"]
    }
