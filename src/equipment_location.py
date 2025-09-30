# src/equipment_location.py
import pandas as pd

def generate_equipment_locations(path="data/equipment_location.csv"):
    records = [
        {"type": "Warehouse", "name": "Melbourne_Warehouse", "lat": -37.81, "lon": 144.96},
        {"type": "Warehouse", "name": "Sydney_Warehouse", "lat": -33.87, "lon": 151.21},
        {"type": "Site", "name": "Project_A", "lat": -37.75, "lon": 145.00},
        {"type": "Site", "name": "Project_B", "lat": -33.90, "lon": 151.25},
    ]
    df = pd.DataFrame(records)
    df.to_csv(path, index=False)
    return df

if __name__ == "__main__":
    print(generate_equipment_locations())
