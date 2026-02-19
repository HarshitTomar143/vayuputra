import requests
import pandas as pd
from app.config import WAQI_TOKEN
from app.data.stations import STATION_ENDPOINTS


def safe_get_iaqi(iaqi_dict, key):
    """
    Safely extract pollutant value.
    Returns None if missing.
    """
    try:
        value = iaqi_dict.get(key, {}).get("v")
        if value is None:
            return None
        return float(value)
    except:
        return None


def fetch_station_data():

    stations_data = []

    for slug in STATION_ENDPOINTS:

        url = f"http://api.waqi.info/feed/{slug}/?token={WAQI_TOKEN}"

        try:
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                continue

            data = response.json()

            if data.get("status") != "ok":
                continue

            city_data = data.get("data", {})
            geo = city_data.get("city", {}).get("geo", None)

            if not geo:
                continue

            raw_aqi = city_data.get("aqi")

            # Skip invalid AQI
            if raw_aqi is None or raw_aqi == "-" or raw_aqi == "":
                continue

            iaqi = city_data.get("iaqi", {})

            station_entry = {
                "name": city_data.get("city", {}).get("name"),
                "latitude": float(geo[0]),
                "longitude": float(geo[1]),
                "aqi": float(raw_aqi),
                "pm25": safe_get_iaqi(iaqi, "pm25"),
                "pm10": safe_get_iaqi(iaqi, "pm10"),
                "co": safe_get_iaqi(iaqi, "co"),
                "no2": safe_get_iaqi(iaqi, "no2"),
                "o3": safe_get_iaqi(iaqi, "o3"),
                "humidity": safe_get_iaqi(iaqi, "h"),
            }

            stations_data.append(station_entry)

        except Exception as e:
            print(f"Error fetching {slug}: {e}")
            continue

    if not stations_data:
        raise ValueError("No AQI data fetched.")

    df = pd.DataFrame(stations_data)

    print("Stations fetched:", len(df))

    return df


if __name__ == "__main__":
    df = fetch_station_data()
    print("Total stations fetched:", len(df))
    print(df.head())
