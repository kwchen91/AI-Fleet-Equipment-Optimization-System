# src/shared_pool.py
import pandas as pd
import random
import os

def generate_shared_pool(n=20):
    companies = ["RPM Hire", "CoHire", "BuildMate"]
    equipment_types = ["Excavator", "Bulldozer", "Crane", "Truck", "Forklift"]
    status_options = ["Available", "In Use", "Maintenance"]

    rows = []
    for i in range(n):
        rows.append({
            "equipment_id": f"EQT{i+1:03d}",
            "company": random.choice(companies),
            "equipment_type": random.choice(equipment_types),
            "status": random.choice(status_options)
        })
    return pd.DataFrame(rows)

def load_shared_pool(path="data/shared_pool.csv", n=20):
    """Load from CSV if available, else generate mock data"""
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return generate_shared_pool(n)

if __name__ == "__main__":
    df = generate_shared_pool(10)
    print("Generated Pool:")
    print(df)

    df2 = load_shared_pool()
    print("Loaded Pool:")
    print(df2)
