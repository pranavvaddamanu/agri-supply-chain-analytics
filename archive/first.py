import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.insights import generate_insights

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Agriculture Supply Chain Intelligence",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

prod = pd.read_csv("data/Fact_Production.csv")
log = pd.read_csv("data/Fact_Logistics.csv")
inv = pd.read_csv("data/Fact_Inventory.csv")

# Convert dates
prod["Date"] = pd.to_datetime(prod["Date"])
log["Date"] = pd.to_datetime(log["Date"])
inv["Date"] = pd.to_datetime(inv["Date"])

# Extract Year
prod["Year"] = prod["Date"].dt.year
log["Year"] = log["Date"].dt.year
inv["Year"] = inv["Date"].dt.year

# Extract Month Name
prod["MonthName"] = prod["Date"].dt.month_name()
log["MonthName"] = log["Date"].dt.month_name()
inv["MonthName"] = inv["Date"].dt.month_name()
# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title(" Agriculture Supply Chain Intelligence Platform")

st.markdown(
    """
Integrated analytics platform for monitoring agricultural production,
logistics efficiency, and inventory spoilage risk.
"""
)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🔎 Filters")

selected_states = st.sidebar.multiselect(
    "Select State",
    options=prod["State"].unique(),
    default=prod["State"].unique()
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(prod["Year"].unique()),
    default=sorted(prod["Year"].unique())
)

selected_crops = st.sidebar.multiselect(
    "Select Crop",
    options=prod["Crop"].unique(),
    default=prod["Crop"].unique()
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_prod = prod[
    (prod["State"].isin(selected_states)) &
    (prod["Year"].isin(selected_years)) &
    (prod["Crop"].isin(selected_crops))
]

filtered_log = log[
    (log["State"].isin(selected_states)) &
    (log["Year"].isin(selected_years))
]

filtered_inv = inv[
    (inv["State"].isin(selected_states)) &
    (inv["Year"].isin(selected_years)) &
    (inv["Crop"].isin(selected_crops))
]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("📊 Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Production",
    f"{filtered_prod['Production_MT'].sum():,.0f}"
)

col2.metric(
    "Avg Logistics Risk",
    f"{filtered_log['LogisticsRisk'].mean():.2f}"
)

col3.metric(
    "Avg Spoilage Loss",
    f"{filtered_inv['StorageLoss'].mean():.2f}"
)

col4.metric(
    "Avg Delay Hours",
    f"{filtered_log['DelayHours'].mean():.2f}"
)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🌾 Production",
    "🚚 Logistics",
    "📦 Inventory",
    "🤖 AI Insights"
])

# ===================================================
# TAB 1 — PRODUCTION
# ===================================================

with tab1:

    st.subheader("Production by State")

    state_prod = (
        filtered_prod.groupby("State")["Production_MT"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        state_prod,
        x="State",
        y="Production_MT",
        color="Production_MT",
        title="Production by State"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Production by Crop")

    crop_prod = (
        filtered_prod.groupby("Crop")["Production_MT"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        crop_prod,
        names="Crop",
        values="Production_MT",
        title="Crop Contribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Rainfall vs Production")

    fig3 = px.scatter(
        filtered_prod,
        x="Rainfall",
        y="Production_MT",
        color="Crop",
        hover_data=["State"]
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Production Trend")

    monthly_prod = (
        filtered_prod.groupby("MonthName")["Production_MT"]
        .sum()
        .reset_index()
    )

    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    monthly_prod["MonthName"] = pd.Categorical(
        monthly_prod["MonthName"],
        categories=month_order,
        ordered=True
    )

    monthly_prod = monthly_prod.sort_values("MonthName")

    fig4 = px.line(
        monthly_prod,
        x="MonthName",
        y="Production_MT",
        markers=True
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("🌍 Production Distribution Map")

    state_prod_map = (
    filtered_prod.groupby("State")["Production_MT"]
    .sum()
    .reset_index()
)
    state_coords = {
    "Andhra Pradesh": [15.9129, 79.7400],
    "Arunachal Pradesh": [28.2180, 94.7278],
    "Assam": [26.2006, 92.9376],
    "Bihar": [25.0961, 85.3131],
    "Chhattisgarh": [21.2787, 81.8661],
    "Goa": [15.2993, 74.1240],
    "Gujarat": [22.2587, 71.1924],
    "Haryana": [29.0588, 76.0856],
    "Himachal Pradesh": [31.1048, 77.1734],
    "Jharkhand": [23.6102, 85.2799],
    "Karnataka": [15.3173, 75.7139],
    "Kerala": [10.8505, 76.2711],
    "Madhya Pradesh": [22.9734, 78.6569],
    "Maharashtra": [19.7515, 75.7139],
    "Manipur": [24.6637, 93.9063],
    "Meghalaya": [25.4670, 91.3662],
    "Mizoram": [23.1645, 92.9376],
    "Nagaland": [26.1584, 94.5624],
    "Odisha": [20.9517, 85.0985],
    "Punjab": [31.1471, 75.3412],
    "Rajasthan": [27.0238, 74.2179],
    "Sikkim": [27.5330, 88.5122],
    "Tamil Nadu": [11.1271, 78.6569],
    "Telangana": [18.1124, 79.0193],
    "Tripura": [23.9408, 91.9882],
    "Uttar Pradesh": [26.8467, 80.9462],
    "Uttarakhand": [30.0668, 79.0193],
    "West Bengal": [22.9868, 87.8550]
}
    state_prod_map["lat"] = state_prod_map["State"].map(
    lambda x: state_coords.get(x, [None, None])[0]
)
    state_prod_map["lon"] = state_prod_map["State"].map(
    lambda x: state_coords.get(x, [None, None])[1]
)
    state_prod_map = state_prod_map.dropna()

    # SCATTER GEO MAP
# ---------------------------------------------------

    fig_map = px.scatter_geo(
    state_prod_map,
    lat="lat",
    lon="lon",
    size="Production_MT",
    color="Production_MT",
    hover_name="State",
    projection="natural earth",
    color_continuous_scale="Greens",
    title="Production by State"
)
    fig_map.update_geos(
    visible=False,
    showcountries=True,
    countrycolor="Black",
    lataxis_range=[6, 38],
    lonaxis_range=[68, 98]
)
    fig_map.update_layout(
    height=600
)
    
    st.plotly_chart(fig_map, use_container_width=True)



   


# ===================================================
# TAB 2 — LOGISTICS
# ===================================================

with tab2:

    st.subheader("Logistics Risk by State")

    risk_state = (
        filtered_log.groupby("State")["LogisticsRisk"]
        .mean()
        .reset_index()
    )

    fig5 = px.bar(
        risk_state,
        x="State",
        y="LogisticsRisk",
        color="LogisticsRisk"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Delay Hours by Vehicle Type")

    delay_vehicle = (
        filtered_log.groupby("VehicleType")["DelayHours"]
        .mean()
        .reset_index()
    )

    fig6 = px.bar(
        delay_vehicle,
        x="VehicleType",
        y="DelayHours",
        color="DelayHours"
    )

    st.plotly_chart(fig6, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Distance vs Delay")

    fig7 = px.scatter(
        filtered_log,
        x="Distance",
        y="DelayHours",
        color="VehicleType"
    )

    st.plotly_chart(fig7, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Fuel Cost by Vehicle Type")

    fuel_vehicle = (
        filtered_log.groupby("VehicleType")["FuelCost"]
        .mean()
        .reset_index()
    )

    fig8 = px.bar(
        fuel_vehicle,
        x="VehicleType",
        y="FuelCost",
        color="FuelCost"
    )

    st.plotly_chart(fig8, use_container_width=True)

    


            
# ===================================================
# TAB 3 — INVENTORY
# ===================================================

with tab3:

    st.subheader("Storage Type vs Spoilage")

    spoil_storage = (
        filtered_inv.groupby("StorageType")["StorageLoss"]
        .mean()
        .reset_index()
    )

    fig9 = px.bar(
        spoil_storage,
        x="StorageType",
        y="StorageLoss",
        color="StorageLoss"
    )

    st.plotly_chart(fig9, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Crop vs Spoilage")

    crop_spoil = (
        filtered_inv.groupby("Crop")["StorageLoss"]
        .mean()
        .reset_index()
    )

    fig10 = px.bar(
        crop_spoil,
        x="Crop",
        y="StorageLoss",
        color="StorageLoss"
    )

    st.plotly_chart(fig10, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Delay vs Storage Loss")

    fig11 = px.scatter(
        filtered_inv,
        x="DelayHours",
        y="StorageLoss",
        color="StorageType"
    )

    st.plotly_chart(fig11, use_container_width=True)

    # ---------------------------------------------

    st.subheader("Spoilage Trend")

    spoil_trend = (
        filtered_inv.groupby("MonthName")["StorageLoss"]
        .mean()
        .reset_index()
    )

    spoil_trend["MonthName"] = pd.Categorical(
        spoil_trend["MonthName"],
        categories=month_order,
        ordered=True
    )

    spoil_trend = spoil_trend.sort_values("MonthName")

    fig12 = px.line(
        spoil_trend,
        x="MonthName",
        y="StorageLoss",
        markers=True
    )

    st.plotly_chart(fig12, use_container_width=True)

    st.subheader("📦 Cold Storage Efficiency")
    cold_loss = filtered_inv[
         filtered_inv["StorageType"] == "Cold"
         ]["StorageLoss"].mean()
    efficiency_score = max(0, 100 - (cold_loss * 5))
    fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=efficiency_score,
        title={'text': "Cold Storage Efficiency"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [0, 50]},
                {'range': [50, 75]},
                {'range': [75, 100]}
            ]
        }
    )
)
    st.plotly_chart(fig_gauge, use_container_width=True)
    



# ===================================================
# TAB 4 — AI INSIGHTS
# ===================================================

with tab4:

    st.subheader("📈 Production vs Spoilage Over Time")
    prod_month = (
    filtered_prod.groupby("MonthName")["Production_MT"]
    .sum()
    .reset_index()
)
    spoil_month = (
    filtered_inv.groupby("MonthName")["StorageLoss"]
    .mean()
    .reset_index()
)
    month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]
    prod_month["MonthName"] = pd.Categorical(
    prod_month["MonthName"],
    categories=month_order,
    ordered=True
)
    spoil_month["MonthName"] = pd.Categorical(
    spoil_month["MonthName"],
    categories=month_order,
    ordered=True
)
    prod_month = prod_month.sort_values("MonthName")
    spoil_month = spoil_month.sort_values("MonthName")
    fig_combo = go.Figure()
    fig_combo.add_trace(
     go.Bar(
        x=prod_month["MonthName"],
        y=prod_month["Production_MT"],
        name="Production"
    )
)
    # Spoilage Line
    fig_combo.add_trace(
     go.Scatter(
        x=spoil_month["MonthName"],
        y=spoil_month["StorageLoss"],
        mode="lines+markers",
        name="Spoilage",
        yaxis="y2"
    )
)
    

    fig_combo.update_layout(
    title="Production vs Spoilage Trend",

    xaxis=dict(
        title="Month"
    ),

    yaxis=dict(
        title="Production_MT"
    ),

    yaxis2=dict(
        title="Storage Loss",
        overlaying="y",
        side="right"
    ),

    legend=dict(
        x=0.01,
        y=0.99
    ),

    height=600
)
    st.plotly_chart(fig_combo, use_container_width=True)

    st.subheader("🤖 AI Insight Engine")

    st.markdown(
        """
Generate automated operational insights based on
production, logistics, and inventory analytics.
"""
    )

    if st.button("Generate AI Insights"):

        insights = generate_insights(
            filtered_prod,
            filtered_log,
            filtered_inv
        )

        st.markdown(insights)