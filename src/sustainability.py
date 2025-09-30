import pandas as pd

def calculate_sustainability(
    gps_path="data/gps_data.csv", 
    usage_time=120, 
    idle_time=30, 
    emission_factor=2.31, 
    fuel_cost_per_L=1.8
):
    df = pd.read_csv(gps_path)
    distance = int(df["mileage_km"].iloc[-1])
    fuel_used = (distance / 100) * df["fuel_L_per_100km"].mean()
    carbon_emission = fuel_used * emission_factor
    utilization = usage_time / (usage_time + idle_time)
    cost = fuel_used * fuel_cost_per_L
    time_saved = round((idle_time * 0.1), 2)  

    return {
        "distance_km": distance,
        "fuel_used_L": round(float(fuel_used), 2),
        "carbon_emission_kg": round(float(carbon_emission), 2),
        "utilization_rate": round(float(utilization), 2),
        "cost_AUD": round(float(cost), 2),
        "time_saved_hr": time_saved
    }

if __name__ == "__main__":
    print(calculate_sustainability())

