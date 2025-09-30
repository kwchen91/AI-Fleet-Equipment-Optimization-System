import pandas as pd

import pandas as pd

def forecast_demand(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower() 
    
    print("Cleaned columns:", df.columns.tolist())  # Debug
    

    if "equipment" in df.columns:
        group_col = "equipment"
    elif "project" in df.columns:
        group_col = "project"
    else:
        raise KeyError("CSV must contain either 'equipment' or 'project' column")
    
    summary = df.groupby(group_col)["rental_days"].sum().reset_index()
    summary.rename(columns={"rental_days": "demand_forecast_days"}, inplace=True)
    summary.rename(columns={group_col: "project"}, inplace=True)  
    
    return summary

def region_trend(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()


    if "region" in df.columns:
        summary = df.groupby("region")["rental_days"].sum().reset_index()
        summary.rename(columns={"rental_days": "total_days"}, inplace=True)
        return summary
   
    elif "project" in df.columns:
        summary = df.groupby("project")["rental_days"].sum().reset_index()
        summary.rename(columns={"rental_days": "total_days"}, inplace=True)
        return summary
    else:
        raise KeyError("CSV must have 'region' or 'project'")


# === Debug Test ===
if __name__ == "__main__":
    result = forecast_demand()
    print(result)
