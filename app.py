import streamlit as st
import pandas as pd
import plotly.express as px

# Import your modules
from src.data_pipeline import generate_gps_data, generate_rental_history
from src.demand_model import forecast_demand
from src.route_vrp import optimize_route
from src.lifecycle import check_equipment_health
from src.cctv_data import generate_cctv_data
from src.shared_pool import generate_shared_pool
from src.equipment_location import generate_equipment_locations
from src.sustainability import calculate_sustainability
from src.circular_economy import circular_recommendation
from src.demand_model import region_trend
from src.external_api import get_weather_forecast
from src.report_generator import generate_report
from src.kpi import KPIWeights

# --- Fake login ---
def login_page():
    st.set_page_config(page_title="RPM Hire AI System", layout="centered")
    st.title("🔒 RPM Hire Internal System")
    st.markdown("Please log in to access the AI optimization dashboard.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# --- Main dashboard ---
def dashboard():
    st.set_page_config(page_title="RPM Hire AI System", layout="wide")

    with st.sidebar:
        st.markdown("### ⚙️ User-defined KPI Weights")
        w_dist = st.slider("Distance weight", 0.0, 3.0, 1.0, 0.1)
        w_time = st.slider("Time weight",     0.0, 3.0, 1.0, 0.1)
        w_co2  = st.slider("CO₂ weight",      0.0, 3.0, 1.0, 0.1)
        w_cong = st.slider("Congestion weight",0.0, 3.0, 1.0, 0.1)
        kpi_w = KPIWeights(distance=w_dist, time=w_time, co2=w_co2, congestion=w_cong)

    # ===== Custom CSS for KPI Cards =====
    st.markdown(
        """
        <style>
        .card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px;
        }
        .card h3 {
            margin: 0;
            font-size: 18px;
            color: #4A5A70;
        }
        .card p {
            margin: 5px 0 0 0;
            font-size: 26px;
            font-weight: bold;
            color: #0057B8;
        }
        .trend-up {
            color: green;
            font-size: 16px;
        }
        .trend-down {
            color: red;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='color:#0057B8;'>🚦 RPM Hire AI Fleet Management</h1>", unsafe_allow_html=True)
    st.markdown("---")


    gps_df = generate_gps_data()
    demand_forecast = forecast_demand("data/rental_history.csv")
    route, route_metrics = optimize_route(use_mock=True, weights=kpi_w)
    lifecycle_status = check_equipment_health()
    cctv = generate_cctv_data()
    pool = generate_shared_pool()
    sustain = calculate_sustainability()
    circular = circular_recommendation()

    # === KPI Summary Cards ===
    total_demand = demand_forecast["demand_forecast_days"].sum()
    total_assets = len(pool)
    co2_saved = sustain.get("CO2_saved", 0)
    healthy_ratio = sustain.get("Healthy_Assets", 0) / total_assets if total_assets else 0

  
    prev_total_demand = total_demand * 0.9   
    prev_total_assets = total_assets * 1.05  
    prev_co2_saved = co2_saved * 0.8         
    prev_healthy_ratio = healthy_ratio * 1.1 

    demand_trend = "up" if total_demand >= prev_total_demand else "down"
    assets_trend = "up" if total_assets >= prev_total_assets else "down"
    co2_trend = "up" if co2_saved >= prev_co2_saved else "down"
    health_trend = "up" if healthy_ratio >= prev_healthy_ratio else "down"

    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.markdown(
            f"<div class='card'><h3>📊 Total Forecasted Demand</h3>"
            f"<p>{total_demand} days</p>"
            f"<span class='trend-{demand_trend}'>"
            f"{'📈 Up' if demand_trend=='up' else '📉 Down'} vs last period</span></div>",
            unsafe_allow_html=True
        )
    with colB:
        st.markdown(
            f"<div class='card'><h3>🔧 Total Assets in Pool</h3>"
            f"<p>{total_assets}</p>"
            f"<span class='trend-{assets_trend}'>"
            f"{'📈 Up' if assets_trend=='up' else '📉 Down'} vs last period</span></div>",
            unsafe_allow_html=True
        )
    with colC:
        st.markdown(
            f"<div class='card'><h3>🌍 CO₂ Saved</h3>"
            f"<p>{co2_saved} kg</p>"
            f"<span class='trend-{co2_trend}'>"
            f"{'📈 Up' if co2_trend=='up' else '📉 Down'} vs last period</span></div>",
            unsafe_allow_html=True
        )
    with colD:
        st.markdown(
            f"<div class='card'><h3>💡 Healthy Equipment Ratio</h3>"
            f"<p>{healthy_ratio:.0%}</p>"
            f"<span class='trend-{health_trend}'>"
            f"{'📈 Up' if health_trend=='up' else '📉 Down'} vs last period</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["📊 Demand Forecast", "🛣️ Route Optimization", "🔧 Lifecycle & CCTV",
     "🌍 Sustainability", "♻️ Circular Economy", "📈 Region Trends", "☁️ Weather Impact"]
    )


    # --- Demand Forecast ---
    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Forecasted Demand (Table)")
            st.dataframe(demand_forecast, use_container_width=True)
        with col2:
            st.subheader("Forecasted Demand (Chart)")
            fig = px.bar(demand_forecast, x="project", y="demand_forecast_days",
                         title="Forecasted Rental Demand (Days)", text_auto=True,
                         color_discrete_sequence=["#0057B8"])
            st.plotly_chart(fig, use_container_width=True)

    # --- Route Optimization ---
    with tab2:
        st.subheader("Optimized Route")
        st.write("Optimal Route:", " → ".join(route))

        m = route_metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Distance (km)", m["distance_km"])
        c2.metric("Time (hr)",     m["time_hr"])
        c3.metric("CO₂ (kg)",      m["co2_kg"])
        c4.metric("Congestion idx",m["congestion_index"])

        st.caption("Tip: Tip: Adjust the KPI weights on the left to instantly change the route and metrics.")
        st.map(gps_df[["lat", "lon"]], zoom=5)

    # --- Lifecycle & CCTV ---
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Lifecycle Status")
            lifecycle_df = check_equipment_health()
            st.dataframe(lifecycle_df, use_container_width=True)
        with c2:
            st.subheader("CCTV Traffic Data")

            chart_type = st.radio(
                "Choose chart type:",
                ["📊 Vehicle Flow by Type (Bar)", "⚖️ Vehicle vs Pedestrian Flow (Scatter)"]
            )

        if chart_type == "📊 Vehicle Flow by Type (Bar)":
            agg_cctv = cctv.groupby("vehicle_type", as_index=False)["vehicle_flow"].sum()

            fig_cctv = px.bar(
                agg_cctv,
                x="vehicle_type",
                y="vehicle_flow",
                color="vehicle_type",
                text="vehicle_flow",  
                title="Vehicle Flow by Type"
            )
            fig_cctv.update_traces(textposition="outside")
            fig_cctv.update_layout(
                xaxis_title="Vehicle Type",
                yaxis_title="Total Vehicle Flow"
            )
        else:
            fig_cctv = px.scatter(
                cctv,
                x="vehicle_flow",
                y="pedestrian_flow",
                color="vehicle_type",
                size="vehicle_flow",
                hover_data=["vehicle_type"],
                title="Traffic Correlation: Vehicle vs Pedestrian Flow"
            )
            fig_cctv.update_layout(
                xaxis_title="Vehicle Flow",
                yaxis_title="Pedestrian Flow"
            )

        st.plotly_chart(fig_cctv, use_container_width=True)


    # --- Sustainability ---
    with tab4:
        st.subheader("Sustainability Dashboard")

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🚗 Distance (km)", f"{sustain['distance_km']}")
        col2.metric("⛽ Fuel Used (L)", f"{sustain['fuel_used_L']}")
        col3.metric("🌍 CO₂ Emission (kg)", f"{sustain['carbon_emission_kg']}")
        col4.metric("📈 Utilization Rate", f"{sustain['utilization_rate']:.0%}")

        st.markdown("---")

        # Breakdown 
        fig_sustain = px.bar(
            x=["Distance (km)", "Fuel Used (L)", "CO₂ Emission (kg)", "Utilization Rate"],
            y=[
                sustain["distance_km"],
                sustain["fuel_used_L"],
                sustain["carbon_emission_kg"],
                sustain["utilization_rate"] * 100  
            ],
            text=[
                sustain["distance_km"],
                sustain["fuel_used_L"],
                sustain["carbon_emission_kg"],
                f"{sustain['utilization_rate']:.0%}"
            ],
            color=["Distance", "Fuel", "CO₂", "Utilization"],
            color_discrete_sequence=px.colors.sequential.Blues,
            title="Sustainability Metrics Breakdown"
        )
        fig_sustain.update_traces(textposition="outside")
        st.plotly_chart(fig_sustain, use_container_width=True)

    # --- Circular Economy ---
    with tab5:
        st.subheader("Shared Equipment Pool (Cross-Company)")
        st.dataframe(pool, use_container_width=True)

        fig_company = px.bar(
            pool.groupby(["company", "status"])["equipment_id"].count().reset_index(),
            x="company", y="equipment_id", color="status",
            title="Shared Equipment Availability by Company",
            text_auto=True,
            barmode="group"
        )
        st.plotly_chart(fig_company, use_container_width=True)

        if isinstance(circular, list):
            circular_df = pd.DataFrame(circular)
            st.dataframe(circular_df, use_container_width=True)

            fig_circular = px.bar(
                circular_df,
                x="recommendation",
                title="Circular Economy Action Distribution",
                color="recommendation",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_circular, use_container_width=True)
        else:
            st.success(circular)

        st.subheader("Shared Equipment Pool")
        st.dataframe(pool, use_container_width=True)

    # --- Region Trends ---
    with tab6:
        st.subheader("Historical Rental Trends by Region")
        region_df = region_trend("data/rental_history.csv")
        st.dataframe(region_df, use_container_width=True)


        x_col = "region" if "region" in region_df.columns else "project"

        fig_region = px.bar(
            region_df,
            x=x_col,
            y="total_days",
            title=f"Demand by {x_col.capitalize()}",
            text_auto=True,
            color_discrete_sequence=["#00C0E3"]
        )
        st.plotly_chart(fig_region, use_container_width=True)


    # --- Weather Impact ---
    with tab7:
        st.subheader("Weather Forecast Impact on Demand")
        weather = get_weather_forecast()
        st.dataframe(weather, use_container_width=True)


        weather["day"] = pd.Categorical(
            weather["day"],
            categories=["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
            ordered=True
        )    

        custom_colors = {
            "Sunny": "#FFD700",   
            "Cloudy": "#A9A9A9",  
            "Rain": "#1E90FF",    
            "Storm": "#00008B"    
        }

        fig_weather = px.bar(
            weather,
            x="day",
            y="demand_factor",
            color="condition",
            title="Impact of Weather on Demand",
            category_orders={"day": ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"]},
            color_discrete_map=custom_colors
        )

        st.plotly_chart(fig_weather, use_container_width=True)


    # --- Report Download ---
    st.markdown("### 📥 Download Report")
    pdf_buffer = generate_report(
        {"Total Demand": total_demand, "Assets": total_assets},
        sustain,
        circular
    )
    st.download_button(
        "Download Sustainability Report",
        data=pdf_buffer,
        file_name="sustainability_report.pdf",
        mime="application/pdf"
    )


    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:gray;'>© 2025 RPM Hire – Hackathon AI Prototype</p>",
        unsafe_allow_html=True
    )

# --- App Execution ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    dashboard()
