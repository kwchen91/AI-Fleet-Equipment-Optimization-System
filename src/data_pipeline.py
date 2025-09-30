# src/data_pipeline.py
import pandas as pd
import numpy as np

def generate_gps_data(num_records=100, path="data/gps_data.csv"):
    """
    Generate mock GPS data for equipment.
    """
    np.random.seed(42)
    data = {
        "equipment_id": np.arange(1, num_records + 1),
        "lat": np.random.uniform(-38, -33, num_records),
        "lon": np.random.uniform(144, 151, num_records),
        "mileage_km": np.cumsum(np.random.randint(1, 10, num_records)),
        "fuel_L_per_100km": np.random.uniform(15, 30, num_records)
    }
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    return df   


def generate_rental_history(num_records=50, path="data/rental_history.csv"):
    """
    Generate mock rental history data.
    """
    np.random.seed(24)
    data = {
        "equipment_id": np.random.randint(1, 20, num_records),
        "rental_days": np.random.randint(1, 30, num_records),
        "project": np.random.choice(["Highway", "Bridge", "Metro"], num_records)
    }
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    return df   
