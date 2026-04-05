# app.py
# Main Streamlit application for Crop Yield Predictor

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_handler import get_sample_data, get_crop_info, STATES, CROPS, SEASONS
from predictor import train_model, predict_yield

# Page configuration
st.set_page_config(
    page_title="Crop Yield Predictor — India",
    page_icon="🌾",
    layout="wide"
)

# Title
st.title("🌾 Hyperlocal Crop Yield Predictor")
st.subheader("AI-powered crop yield prediction for Indian farmers")
st.markdown("---")

# Train model
@st.cache_resource
def load_model():
    return train_model()

with st.spinner("Loading AI Model..."):
    model, le_state, le_crop, le_season, r2, mae = load_model()

# Model accuracy
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Accuracy (R²)", f"{r2:.2%}")
with col2:
    st.metric("Mean Error", f"{mae:.2f} ton/ha")
with col3:
    st.metric("Total Crops", len(CROPS))

st.markdown("---")

# Two columns layout
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### 📍 Location & Crop Details")

    state = st.selectbox("Select State", STATES)
    crop = st.selectbox("Select Crop", CROPS)
    season = st.selectbox("Select Season", SEASONS)
    year = st.slider("Year", 2020, 2030, 2024)

with right_col:
    st.markdown("### 🌦️ Weather & Soil Conditions")

    rainfall = st.slider("Rainfall (mm)", 100, 2000, 800)
    temperature = st.slider("Temperature (°C)", 10, 45, 25)
    humidity = st.slider("Humidity (%)", 20, 100, 60)
    soil_ph = st.slider("Soil pH", 4.0, 9.0, 7.0)
    fertilizer = st.slider("Fertilizer (kg/ha)", 0, 500, 150)
    irrigation = st.slider("Irrigation (%)", 0, 100, 50)

st.markdown("---")

# Predict button
if st.button("🔮 Predict Crop Yield", use_container_width=True):

    prediction = predict_yield(
        model, le_state, le_crop, le_season,
        state, crop, season, year,
        rainfall, temperature, humidity,
        soil_ph, fertilizer, irrigation
    )

    if prediction:
        st.success(f"### 🌾 Predicted Yield: **{prediction} ton/hectare**")

        # Crop info
        crop_info = get_crop_info(crop)
        if crop_info:
            st.markdown("#### 📊 Ideal Conditions for " + crop)
            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.info(f"💧 Rainfall: {crop_info['ideal_rainfall']}")
            with info_col2:
                st.info(f"🌡️ Temperature: {crop_info['ideal_temp']}")
            with info_col3:
                st.info(f"📅 Season: {crop_info['season']}")

st.markdown("---")

# Data Analysis Section
st.markdown("### 📊 Crop Yield Analysis — India")

df = get_sample_data()

tab1, tab2, tab3 = st.tabs(["State-wise", "Crop-wise", "Season-wise"])

with tab1:
    state_data = df.groupby("State")["Yield_ton_per_ha"].mean().reset_index()
    fig1 = px.bar(
        state_data,
        x="State",
        y="Yield_ton_per_ha",
        title="Average Crop Yield by State",
        color="Yield_ton_per_ha",
        color_continuous_scale="Greens"
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    crop_data = df.groupby("Crop")["Yield_ton_per_ha"].mean().reset_index()
    fig2 = px.pie(
        crop_data,
        values="Yield_ton_per_ha",
        names="Crop",
        title="Yield Distribution by Crop",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    season_data = df.groupby("Season")["Yield_ton_per_ha"].mean().reset_index()
    fig3 = px.bar(
        season_data,
        x="Season",
        y="Yield_ton_per_ha",
        title="Average Yield by Season",
        color="Season",
        color_discrete_sequence=["#2d6a4f", "#52b788", "#95d5b2"]
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown("**Developer:** Ankita Choudhary | AI & Data Science — IIT Guwahati")