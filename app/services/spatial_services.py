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

    # Get only latest hour snapshot
    result = db.query(Station).order_by(Station.timestamp.desc()).all()

    db.close()

    if not result:
        return pd.DataFrame()

    df = pd.DataFrame([
        {
            "latitude": r.latitude,
            "longitude": r.longitude,
            "value": r.aqi
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
            return float(row["value"])

        weight = 1 / (row["distance"] ** 2)
        weights.append(weight)
        weighted_values.append(weight * row["value"])

    predicted = sum(weighted_values) / sum(weights)

    return round(float(predicted), 2)
