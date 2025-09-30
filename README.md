# 🚦 RPM Hire - AI Fleet & Equipment Optimization System

This repository contains a **Hackathon prototype** simulating RPM Hire’s AI-driven fleet & equipment management platform.  
The system integrates **mock data generation, demand forecasting, route optimization, equipment lifecycle management, dashboard visualization, and automated reporting**.

---

## 📂 Project Structure
```text
📦 AnyAI-main
├── data/
│   ├── cctv_data.csv
│   ├── equipment_location.csv
│   ├── gps_data.csv
│   ├── rental_history.csv
│   ├── report.pdf
│   ├── shared_pool.csv
├── src/
│   ├── cctv_data.py
│   ├── circular_economy.py
│   ├── dashboard.py
│   ├── data_pipeline.py
│   ├── demand_model.py
│   ├── equipment_location.py
│   ├── external_api.py
│   ├── lifecycle.py
│   ├── report_generator.py
│   ├── route_vrp.py
│   ├── shared_pool.py
│   ├── sustainability.py
├── README.md
├── app.py
├── requirements.txt


```

---

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-repo>/rpm-hire-ai.git
cd rpm-hire-ai
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Run the full pipeline
```bash
python app.py
```

This will:
- Generate mock GPS, rental, and weather data  
- Forecast equipment demand  
- Optimize vehicle route  
- Check equipment lifecycle  
- Output a sustainability report (`data/report.pdf`)  

### 2. Launch the Dashboard
```bash
streamlit run src/dashboard.py
```

The dashboard shows:
- 📊 Demand forecast (bar chart by state)  
- 🛣️ Optimal route  
- 🔧 Equipment health status  
- ⚖️ KPI customization sliders (cost / time / carbon)  

---

## 📊 Example Outputs

**Data (data/gps_data.csv)**
```csv
timestamp,latitude,longitude,mileage_km,fuel_L_per_100km
2025-09-29 12:00:00,-37.80,145.02,10,8.4
2025-09-29 12:05:00,-37.85,145.05,14,7.9
...
```

**Dashboard (Streamlit)**  
Interactive UI with charts and KPIs  

**Generated Report (data/report.pdf)**  
Includes:
- Optimal route  
- Demand forecast  
- Equipment health status  

---

## 🧩 Tech Stack
📊 Data & Analysis → pandas, numpy, scikit-learn  
📈 Visualisation → plotly, streamlit-option-menu  
🖥️ App / Dashboard → streamlit  
🛠️ Optimisation → ortools  
📄 Reporting → reportlab  
🔗 API & Utilities → requests  

---

## 💡 Future Extensions
- Integrate real GPS & IoT data instead of mock data  
- Connect to live weather/traffic APIs  
- Use ML models (LSTM, Prophet) for demand forecasting  
- Advanced Remaining Useful Life (RUL) prediction  
- Cross-company shared equipment pools  
- ESG-compliant sustainability reporting  

---

## 👥 Team
Hackathon project for RPM Hire – Sustainable Fleet & Equipment Management
