import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

from src.data_pipeline import generate_gps_data, generate_rental_history
from src.demand_model import forecast_demand
from src.route_vrp import optimize_route
from src.lifecycle import check_equipment_health
from src.external_data import get_external_data
from src.cctv_data import generate_cctv_data
from src.shared_pool import generate_shared_pool
from src.equipment_location import generate_equipment_locations
from src.sustainability import calculate_sustainability
from src.circular_economy import circular_recommendation


# === Page Config ===
st.set_page_config(page_title="RPM Hire AI Dashboard", layout="wide")

st.title("🚦 RPM Hire AI Dashboard")
st.markdown("A Hackathon Prototype for **AI-powered Fleet & Equipment Optimization**")


# --- Data Preparation ---
gps_df = generate_gps_data()
rental_df = generate_rental_history()
demand_forecast = forecast_demand("data/rental_history.csv")
route = optimize_route(use_mock=True)
lifecycle_status = check_equipment_health()
external = get_external_data()
cctv = generate_cctv_data()
pool = generate_shared_pool()
locs = generate_equipment_locations()
sustain = calculate_sustainability()
circular = circular_recommendation()


# --- Layout ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Demand Forecast", 
    "🛣️ Route Optimization", 
    "🔧 Lifecycle & CCTV", 
    "🌍 Sustainability", 
    "♻️ Circular Economy"
])


# --- Tab 1: Demand Forecast ---
with tab1:
    st.subheader("Forecasted Demand by Project Type")
    st.dataframe(demand_forecast)

    fig = px.bar(demand_forecast, x="project", y="demand_forecast_days", 
                 title="Forecasted Rental Demand (Days)", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)


# --- Tab 2: Route Optimization ---
with tab2:
    st.subheader("Optimized Equipment Delivery Route")
    st.write("Optimal Route Sequence:", " → ".join(route))

    # Plot route on map using pydeck
    st.map(gps_df[["lat", "lon"]], zoom=5)


# --- Tab 3: Lifecycle & CCTV ---
with tab3:
    st.subheader("Lifecycle Status")
    st.info(lifecycle_status)

    st.subheader("CCTV Traffic Data (Sample)")
    st.dataframe(cctv.head(10))

    fig_cctv = px.scatter(cctv, x="vehicle_flow", y="pedestrian_flow", 
                          color="vehicle_type", title="Traffic Patterns")
    st.plotly_chart(fig_cctv, use_container_width=True)


# --- Tab 4: Sustainability ---
with tab4:
    st.subheader("Sustainability Metrics")
    st.json(sustain)

    fig_sustain = px.pie(
        names=list(sustain.keys()),
        values=[float(sustain[k]) if isinstance(sustain[k], (int, float)) else 0 for k in sustain.keys()],
        title="Sustainability Distribution"
    )
    st.plotly_chart(fig_sustain, use_container_width=True)


# --- Tab 5: Circular Economy ---
with tab5:
    st.subheader("Circular Economy Recommendation")
    st.success(circular)

    st.subheader("Shared Equipment Pool")
    st.dataframe(pool)
