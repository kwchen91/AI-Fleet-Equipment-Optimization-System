# src/cctv_data.py
import pandas as pd
import random

def generate_cctv_data(n=50):
    vehicle_types = ["Car", "Truck", "Bus", "Motorbike"]
    rows = []
    for _ in range(n):
        rows.append({
            "vehicle_type": random.choice(vehicle_types),
            "vehicle_flow": random.randint(20, 200),
            "pedestrian_flow": random.randint(5, 50)
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print(generate_cctv_data().head())
