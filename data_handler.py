# data_handler.py
# Handles crop and weather data for Indian districts

import pandas as pd
import numpy as np

# Indian states and districts data
STATES = [
    "Andhra Pradesh", "Bihar", "Gujarat", "Haryana",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
    "Punjab", "Rajasthan", "Tamil Nadu", "Uttar Pradesh",
    "West Bengal", "Odisha", "Assam"
]

CROPS = [
    "Rice", "Wheat", "Maize", "Cotton", "Sugarcane",
    "Soybean", "Groundnut", "Mustard", "Barley", "Jowar"
]

SEASONS = ["Kharif", "Rabi", "Zaid"]

def get_sample_data():
    """
    Generates sample crop yield data for Indian districts
    """
    np.random.seed(42)
    n_samples = 1000

    data = {
        "State": np.random.choice(STATES, n_samples),
        "Crop": np.random.choice(CROPS, n_samples),
        "Season": np.random.choice(SEASONS, n_samples),
        "Year": np.random.randint(2015, 2024, n_samples),
        "Rainfall_mm": np.random.uniform(200, 1500, n_samples),
        "Temperature_C": np.random.uniform(15, 42, n_samples),
        "Humidity_%": np.random.uniform(30, 90, n_samples),
        "Soil_pH": np.random.uniform(5.5, 8.5, n_samples),
        "Fertilizer_kg_per_ha": np.random.uniform(50, 300, n_samples),
        "Irrigation_%": np.random.uniform(0, 100, n_samples),
        "Yield_ton_per_ha": np.random.uniform(0.5, 8.0, n_samples)
    }

    return pd.DataFrame(data)

def get_crop_info(crop):
    """
    Returns information about a specific crop
    """
    crop_info = {
        "Rice": {"ideal_rainfall": "1000-2000mm", "ideal_temp": "20-35°C", "season": "Kharif"},
        "Wheat": {"ideal_rainfall": "300-500mm", "ideal_temp": "15-25°C", "season": "Rabi"},
        "Maize": {"ideal_rainfall": "500-800mm", "ideal_temp": "18-32°C", "season": "Kharif"},
        "Cotton": {"ideal_rainfall": "500-1000mm", "ideal_temp": "25-35°C", "season": "Kharif"},
        "Sugarcane": {"ideal_rainfall": "1000-1500mm", "ideal_temp": "20-35°C", "season": "Zaid"},
        "Soybean": {"ideal_rainfall": "600-800mm", "ideal_temp": "20-30°C", "season": "Kharif"},
        "Groundnut": {"ideal_rainfall": "500-600mm", "ideal_temp": "25-30°C", "season": "Kharif"},
        "Mustard": {"ideal_rainfall": "250-400mm", "ideal_temp": "10-25°C", "season": "Rabi"},
        "Barley": {"ideal_rainfall": "300-500mm", "ideal_temp": "12-25°C", "season": "Rabi"},
        "Jowar": {"ideal_rainfall": "400-600mm", "ideal_temp": "25-35°C", "season": "Kharif"}
    }
    return crop_info.get(crop, {})