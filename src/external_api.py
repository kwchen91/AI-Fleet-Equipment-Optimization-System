# src/external_data.py
import pandas as pd
import random

def get_weather_forecast(n=7):
    conditions = ["Sunny", "Rain", "Storm", "Cloudy"]
    rows = []
    for day in range(1, n+1):
        condition = random.choice(conditions)
        demand_factor = 1.2 if condition == "Rain" else 1.0
        rows.append({
            "day": f"Day {day}",
            "condition": condition,
            "demand_factor": demand_factor
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print(get_weather_forecast())
