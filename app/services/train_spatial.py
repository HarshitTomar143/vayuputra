import os
import joblib
import numpy as np
from pykrige.ok import OrdinaryKriging
from app.utils.data_loader import fetch_station_data
from app.config import MODEL_PATH


def train_spatial_model():

    print("Fetching station data...")
    df = fetch_station_data()

    print("Stations used:", len(df))

    lats = df["latitude"].values
    lons = df["longitude"].values
    values = df["value"].values

    print("Mean AQI:", values.mean())

    # IMPORTANT FIX: geographic coordinates + exponential variogram
    model = OrdinaryKriging(
        lons,
        lats,
        values,
        variogram_model="exponential",
        coordinates_type="geographic"
    )

    os.makedirs("app/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Spatial model trained and saved.")


if __name__ == "__main__":
    train_spatial_model()
