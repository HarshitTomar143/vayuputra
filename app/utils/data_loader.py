import requests
import pandas as pd
from app.config import WAQI_TOKEN
from app.data.stations import STATION_ENDPOINTS

def fetch_station_data():

    stations_data = []

    for slug in STATION_ENDPOINTS:
        url = f"http://api.waqi.info/feed/{slug}/?token={WAQI_TOKEN}"

        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if data["status"] != "ok":
                continue

            geo = data["data"]["city"]["geo"]
            aqi = data["data"]["aqi"]

            if aqi and aqi != "-":
                stations_data.append({
                    "latitude": geo[0],
                    "longitude": geo[1],
                    "value": float(aqi)
                })

        except:
            continue

    df = pd.DataFrame(stations_data)

    if df.empty:
        raise ValueError("No AQI data fetched.")

    print("Stations fetched:", len(df))

    return df

if __name__ == "__main__":
    df = fetch_station_data()
    print("Total stations fetched:", len(df))
    print(df.head())