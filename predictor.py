# predictor.py
# Machine learning model for crop yield prediction

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from data_handler import get_sample_data

def prepare_data(df):
    """
    Prepares data for ML model
    """
    le_state = LabelEncoder()
    le_crop = LabelEncoder()
    le_season = LabelEncoder()

    df = df.copy()
    df["State_encoded"] = le_state.fit_transform(df["State"])
    df["Crop_encoded"] = le_crop.fit_transform(df["Crop"])
    df["Season_encoded"] = le_season.fit_transform(df["Season"])

    features = [
        "State_encoded", "Crop_encoded", "Season_encoded",
        "Year", "Rainfall_mm", "Temperature_C", "Humidity_%",
        "Soil_pH", "Fertilizer_kg_per_ha", "Irrigation_%"
    ]

    X = df[features]
    y = df["Yield_ton_per_ha"]

    return X, y, le_state, le_crop, le_season

def train_model():
    """
    Trains Random Forest model on crop data
    """
    df = get_sample_data()
    X, y, le_state, le_crop, le_season = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    return model, le_state, le_crop, le_season, r2, mae

def predict_yield(model, le_state, le_crop, le_season,
                  state, crop, season, year,
                  rainfall, temperature, humidity,
                  soil_ph, fertilizer, irrigation):
    """
    Predicts crop yield for given inputs
    """
    try:
        state_encoded = le_state.transform([state])[0]
        crop_encoded = le_crop.transform([crop])[0]
        season_encoded = le_season.transform([season])[0]

        features = [[
            state_encoded, crop_encoded, season_encoded,
            year, rainfall, temperature, humidity,
            soil_ph, fertilizer, irrigation
        ]]

        prediction = model.predict(features)[0]
        return round(prediction, 2)

    except Exception as e:
        print