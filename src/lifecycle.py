# src/lifecycle.py
import pandas as pd
import numpy as np

def _health_score(usage_hours, move_count, mileage_km):
    score = 100
    score -= 0.02 * usage_hours        
    score -= 0.5  * move_count         
    score -= 0.01 * mileage_km         
    return float(np.clip(score, 0, 100))

def _estimate_rul_days(health_score):
    return int(round((health_score / 100.0) * 365))

def check_equipment_health(usage_path=None, gps=None):
    try:
        usage = pd.read_csv(usage_path)  # columns: equipment_id, usage_hours, move_count
    except Exception:
        # fallback 
        usage = pd.DataFrame({
            "equipment_id": [f"EQT{i:03d}" for i in range(1, 11)],
            "usage_hours":  np.random.randint(100, 4000, 10),
            "move_count":   np.random.randint(5, 120, 10),
        })

    try:
        if gps is None or "equipment_id" not in gps.columns:
            total_km = 1000
            if gps is not None and "mileage_km" in gps.columns:
                total_km = int(gps["mileage_km"].iloc[-1])
            gps = pd.DataFrame({
                "equipment_id": usage["equipment_id"],
                "mileage_km": np.random.randint(200, 20000, len(usage)) if gps is None else total_km
            })
        else:
            gps = gps[["equipment_id","mileage_km"]].groupby("equipment_id", as_index=False).max()
    except Exception:
        gps = pd.DataFrame({
            "equipment_id": usage["equipment_id"],
            "mileage_km": np.random.randint(200, 20000, len(usage))
        })

    # merge usage + gps
    df = usage.merge(gps, on="equipment_id", how="left")
    df["mileage_km"].fillna(df["mileage_km"].median(), inplace=True)

    # health score & RUL
    df["health_score"] = df.apply(
        lambda r: _health_score(r["usage_hours"], r["move_count"], r["mileage_km"]), axis=1
    )
    df["RUL_days"] = df["health_score"].apply(_estimate_rul_days)

    # recommendation
    def _recommend(h):
        if h > 80:  return "✅ Continue using"
        if h > 60:  return "🔧 Schedule maintenance"
        if h > 40:  return "🔧 Refurbish soon"
        return "♻️ Recycle/Decommission"

    df["recommendation"] = df["health_score"].apply(_recommend)

    return df[["equipment_id","usage_hours","move_count","mileage_km","health_score","RUL_days","recommendation"]]
