# predictor.py
# ML-based Crop Yield Predictor
# Author: Ankita Choudhary | IIT Guwahati
# Based on ICAR agronomic knowledge

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import streamlit as st
from data_handler import CROPS, ALL_CROPS, STATES, SEASONS, convert_to_hectare

# ─────────────────────────────────────────
# CROP YIELD RANGES (ton/ha)
# Source: ICAR guidelines + Agricultural science
# ─────────────────────────────────────────
CROP_YIELD_RANGES = {
    # Grains
    "Rice":                   (2.0, 6.0),
    "Wheat":                  (2.5, 5.5),
    "Maize (Corn)":           (3.0, 7.0),
    "Barley":                 (2.0, 4.5),
    "Jowar (Sorghum)":        (1.5, 4.0),
    "Bajra (Pearl Millet)":   (1.5, 3.5),
    "Ragi (Finger Millet)":   (1.0, 3.0),
    "Oats":                   (1.5, 3.5),
    "Small Millet (Kutki)":   (0.5, 1.5),
    "Kodo Millet":            (0.5, 1.5),
    "Foxtail Millet":         (0.8, 2.0),
    "Proso Millet":           (0.8, 2.0),
    "Barnyard Millet":        (0.8, 2.0),
    "Amaranth (Rajgira)":     (1.0, 2.5),

    # Pulses
    "Arhar (Tur/Pigeon Pea)": (0.8, 2.0),
    "Moong (Green Gram)":     (0.6, 1.5),
    "Urad (Black Gram)":      (0.6, 1.5),
    "Chickpea (Chana)":       (0.8, 2.0),
    "Lentil (Masur)":         (0.8, 1.8),
    "Rajma (Kidney Bean)":    (1.0, 2.5),
    "Lobiya (Cowpea)":        (0.8, 1.8),
    "Moth Bean":              (0.5, 1.2),
    "Horse Gram (Kulthi)":    (0.5, 1.2),
    "Field Pea (Matar)":      (1.0, 2.5),
    "Flat Bean (Sem)":        (3.0, 8.0),
    "Cluster Bean (Guar)":    (0.8, 2.0),
    "Faba Bean (Bakla)":      (1.5, 3.0),
    "Lakh (Grass Pea)":       (0.5, 1.2),

    # Oilseeds
    "Mustard (Sarson)":       (1.0, 2.5),
    "Groundnut (Moongfali)":  (1.5, 3.5),
    "Soybean":                (1.5, 3.0),
    "Sunflower":              (1.2, 2.5),
    "Sesame (Til)":           (0.4, 1.0),
    "Linseed (Alsi)":         (0.5, 1.2),
    "Castor (Arandi)":        (1.0, 2.5),
    "Safflower (Kusum)":      (0.8, 1.8),
    "Niger Seed":             (0.3, 0.8),
    "Rapeseed":               (1.0, 2.5),
    "Toria (Yellow Sarson)":  (0.8, 1.8),

    # Cash Crops
    "Sugarcane":              (60.0, 100.0),
    "Cotton (Kapas)":         (1.5, 3.5),
    "Jute":                   (2.0, 3.5),
    "Tobacco":                (1.5, 2.5),
    "Indigo":                 (1.0, 2.0),
    "Hemp (Bhang)":           (1.0, 3.0),
    "Flax (Patsan)":          (0.8, 1.5),

    # Vegetables
    "Tomato":                 (20.0, 50.0),
    "Onion":                  (15.0, 30.0),
    "Potato":                 (20.0, 40.0),
    "Brinjal (Baingan)":      (15.0, 35.0),
    "Cauliflower":            (15.0, 30.0),
    "Cabbage":                (20.0, 40.0),
    "Spinach (Palak)":        (10.0, 20.0),
    "Peas (Matar)":           (5.0, 12.0),
    "Bhindi (Okra)":          (8.0, 15.0),
    "Bitter Gourd (Karela)":  (8.0, 15.0),
    "Bottle Gourd (Lauki)":   (15.0, 30.0),
    "Capsicum (Shimla Mirch)":(10.0, 20.0),
    "Carrot (Gajar)":         (15.0, 30.0),
    "Radish (Mooli)":         (15.0, 25.0),
    "Beetroot":               (15.0, 30.0),
    "Garlic (Lahsun)":        (5.0, 12.0),
    "Pumpkin (Kaddu)":        (15.0, 30.0),
    "Ridge Gourd (Tori)":     (8.0, 15.0),
    "Snake Gourd":            (10.0, 20.0),
    "Sponge Gourd":           (8.0, 15.0),
    "Tinda (Indian Round Gourd)":(8.0, 15.0),
    "Parwal (Pointed Gourd)": (8.0, 15.0),
    "Colocasia (Arbi)":       (10.0, 20.0),
    "Sweet Potato (Shakarkand)":(10.0, 20.0),
    "Yam (Suran)":            (10.0, 25.0),
    "Turnip (Shalgam)":       (15.0, 25.0),
    "Drumstick (Sahjan)":     (5.0, 15.0),
    "Cucumber (Kheera)":      (10.0, 20.0),
    "Ash Gourd (Petha)":      (15.0, 30.0),
    "Lettuce":                (10.0, 20.0),
    "Celery":                 (8.0, 15.0),
    "Broccoli":               (8.0, 15.0),
    "Spring Onion":           (8.0, 15.0),
    "Fenugreek Leaves (Methi)":(8.0, 15.0),
    "Coriander Leaves (Hara Dhaniya)":(8.0, 12.0),
    "Curry Leaves":           (3.0, 8.0),
    "Mint (Pudina)":          (8.0, 15.0),
    "Bathua":                 (5.0, 10.0),
    "Amaranth Leaves (Chaulai)":(8.0, 15.0),

    # Fruits
    "Mango (Aam)":            (8.0, 20.0),
    "Banana (Kela)":          (20.0, 50.0),
    "Apple (Seb)":            (8.0, 25.0),
    "Grapes (Angoor)":        (10.0, 25.0),
    "Guava (Amrood)":         (10.0, 20.0),
    "Papaya (Papita)":        (30.0, 60.0),
    "Pomegranate (Anar)":     (8.0, 15.0),
    "Orange (Santra)":        (10.0, 20.0),
    "Lemon (Nimbu)":          (10.0, 20.0),
    "Litchi":                 (5.0, 12.0),
    "Pineapple (Ananas)":     (15.0, 30.0),
    "Watermelon (Tarbuj)":    (20.0, 40.0),
    "Muskmelon (Kharbooja)":  (10.0, 20.0),
    "Strawberry":             (8.0, 20.0),
    "Kiwi":                   (8.0, 15.0),
    "Pear (Nashpati)":        (8.0, 20.0),
    "Plum (Aloo Bukhara)":    (5.0, 15.0),
    "Peach (Aadoo)":          (5.0, 15.0),
    "Apricot (Khurmani)":     (3.0, 10.0),
    "Cherry (Cheri)":         (3.0, 10.0),
    "Fig (Anjeer)":           (5.0, 12.0),
    "Dates (Khajoor)":        (5.0, 15.0),
    "Avocado":                (5.0, 12.0),
    "Custard Apple (Sharifa)": (5.0, 12.0),
    "Wood Apple (Bel)":       (5.0, 10.0),
    "Indian Gooseberry (Amla)":(5.0, 12.0),
    "Jackfruit (Kathal)":     (10.0, 25.0),
    "Mulberry (Shahtoot)":    (5.0, 15.0),
    "Jamun (Java Plum)":      (5.0, 12.0),
    "Karonda":                (3.0, 8.0),
    "Phalsa":                 (3.0, 8.0),
    "Star Fruit (Kamrakh)":   (5.0, 12.0),
    "Dragon Fruit":           (5.0, 15.0),
    "Passion Fruit":          (5.0, 12.0),
    "Tamarind (Imli)":        (3.0, 8.0),
    "Sapota (Chikoo)":        (8.0, 15.0),
    "Loquat (Lukaat)":        (5.0, 12.0),

    # Flowers (ton/ha fresh weight)
    "Rose (Gulab)":           (8.0, 20.0),
    "Marigold (Genda)":       (10.0, 20.0),
    "Jasmine (Chameli)":      (3.0, 8.0),
    "Chrysanthemum (Guldaudi)":(10.0, 20.0),
    "Gladiolus":              (5.0, 12.0),
    "Tuberose (Rajnigandha)": (5.0, 12.0),
    "Lotus (Kamal)":          (3.0, 8.0),
    "Sunflower (Surajmukhi)": (8.0, 15.0),
    "Dahlia":                 (8.0, 15.0),
    "Orchid":                 (2.0, 5.0),
    "Carnation":              (8.0, 15.0),
    "Lily":                   (5.0, 12.0),
    "Gerbera":                (5.0, 12.0),
    "Anthurium":              (3.0, 8.0),
    "Bird of Paradise":       (3.0, 8.0),
    "Crossandra":             (5.0, 10.0),
    "Aster":                  (5.0, 10.0),
    "Larkspur":               (3.0, 8.0),
    "Pansy":                  (3.0, 8.0),
    "Zinnia":                 (5.0, 10.0),

    # Spices
    "Turmeric (Haldi)":       (3.0, 8.0),
    "Dry Ginger (Sonth)":     (1.5, 4.0),
    "Red Chilli (Lal Mirch)": (1.5, 3.5),
    "Green Chilli (Hari Mirch)":(5.0, 12.0),
    "Coriander (Dhaniya)":    (0.8, 2.0),
    "Cumin (Jeera)":          (0.5, 1.2),
    "Fenugreek (Methi Dana)": (1.0, 2.0),
    "Cardamom (Elaichi)":     (0.1, 0.3),
    "Black Pepper (Kali Mirch)":(0.5, 2.0),
    "Clove (Laung)":          (0.5, 1.5),
    "Nutmeg (Jaiphal)":       (0.5, 1.5),
    "Cinnamon (Dalchini)":    (1.0, 3.0),
    "Star Anise (Chakri Phool)":(0.5, 1.5),
    "Bay Leaf (Tej Patta)":   (1.0, 3.0),
    "Ajwain (Carom Seeds)":   (0.5, 1.2),
    "Fennel (Saunf)":         (1.0, 2.0),
    "Asafoetida (Hing)":      (0.1, 0.5),
    "Mustard Seeds (Sarson Dana)":(1.0, 2.5),
    "Poppy Seeds (Khus Khus)":(0.5, 1.2),
    "Saffron (Kesar)":        (0.002, 0.006),
    "Vanilla":                (0.5, 2.0),
    "Kokum":                  (2.0, 5.0),
    "Lemongrass":             (5.0, 15.0),
    "Brahmi":                 (3.0, 8.0),
    "Stevia":                 (3.0, 8.0),
    "Isabgol (Psyllium)":     (1.0, 2.0),

    # Plantation
    "Tea (Chai)":             (1.5, 3.5),
    "Coffee (Kaphi)":         (0.5, 2.0),
    "Coconut (Nariyal)":      (8.0, 15.0),
    "Areca Nut (Supari)":     (1.5, 3.0),
    "Rubber":                 (1.0, 2.5),
    "Cashew (Kaju)":          (0.8, 2.0),
    "Cocoa":                  (0.5, 1.5),
    "Oil Palm":               (15.0, 25.0),
    "Eucalyptus":             (15.0, 30.0),
    "Bamboo (Baans)":         (20.0, 40.0),
    "Teak (Sagwan)":          (5.0, 15.0),

    # Medicinal
    "Aloe Vera":              (8.0, 20.0),
    "Neem":                   (3.0, 8.0),
    "Tulsi (Holy Basil)":     (3.0, 8.0),
    "Lavender":               (1.0, 3.0),
    "Peppermint":             (3.0, 8.0),
    "Spearmint":              (3.0, 8.0),
    "Chamomile":              (1.0, 3.0),
    "Calendula":              (1.0, 3.0),
    "Giloy (Guduchi)":        (3.0, 8.0),
    "Shatavari":              (3.0, 8.0),
    "Mulethi (Liquorice)":    (2.0, 5.0),
    "Kalmegh":                (2.0, 5.0),
    "Safed Musli":            (1.5, 4.0),
    "Bhumi Amla":             (2.0, 5.0),
    "Jatamansi":              (1.0, 3.0),
    "Valerian":               (1.5, 4.0),
    "Ashwagandha (Withania)": (0.5, 1.5),
}

# ─────────────────────────────────────────
# STATE-CROP SUITABILITY
# Based on ICAR regional recommendations
# ─────────────────────────────────────────
STATE_CROP_SUITABILITY = {
    "Punjab":          ["Wheat", "Rice", "Maize (Corn)", "Cotton (Kapas)", "Sugarcane", "Mustard (Sarson)", "Sunflower"],
    "Haryana":         ["Wheat", "Rice", "Sugarcane", "Cotton (Kapas)", "Mustard (Sarson)", "Barley"],
    "Uttar Pradesh":   ["Wheat", "Rice", "Sugarcane", "Potato", "Mustard (Sarson)", "Arhar (Tur/Pigeon Pea)"],
    "Bihar":           ["Rice", "Wheat", "Maize (Corn)", "Lentil (Masur)", "Mustard (Sarson)", "Sugarcane"],
    "Rajasthan":       ["Bajra (Pearl Millet)", "Wheat", "Mustard (Sarson)", "Jowar (Sorghum)", "Groundnut (Moongfali)"],
    "Madhya Pradesh":  ["Soybean", "Wheat", "Chickpea (Chana)", "Maize (Corn)", "Cotton (Kapas)"],
    "Maharashtra":     ["Sugarcane", "Cotton (Kapas)", "Soybean", "Jowar (Sorghum)", "Onion", "Grapes (Angoor)"],
    "Gujarat":         ["Cotton (Kapas)", "Groundnut (Moongfali)", "Wheat", "Rice", "Sugarcane", "Castor (Arandi)"],
    "Tamil Nadu":      ["Rice", "Sugarcane", "Banana (Kela)", "Coconut (Nariyal)", "Turmeric (Haldi)"],
    "Kerala":          ["Coconut (Nariyal)", "Rubber", "Tea (Chai)", "Coffee (Kaphi)", "Black Pepper (Kali Mirch)", "Cardamom (Elaichi)"],
    "Karnataka":       ["Rice", "Sugarcane", "Coffee (Kaphi)", "Maize (Corn)", "Groundnut (Moongfali)"],
    "Andhra Pradesh":  ["Rice", "Cotton (Kapas)", "Maize (Corn)", "Groundnut (Moongfali)", "Chilli"],
    "Telangana":       ["Rice", "Cotton (Kapas)", "Maize (Corn)", "Soybean", "Red Chilli (Lal Mirch)"],
    "West Bengal":     ["Rice", "Jute", "Tea (Chai)", "Potato", "Mustard (Sarson)"],
    "Odisha":          ["Rice", "Maize (Corn)", "Groundnut (Moongfali)", "Jute", "Turmeric (Haldi)"],
    "Assam":           ["Tea (Chai)", "Rice", "Jute", "Mustard (Sarson)", "Coconut (Nariyal)"],
    "Himachal Pradesh":["Apple (Seb)", "Wheat", "Maize (Corn)", "Ginger (Adrak)", "Saffron (Kesar)"],
    "Jammu & Kashmir": ["Saffron (Kesar)", "Apple (Seb)", "Wheat", "Rice", "Cherry (Cheri)"],
    "Uttarakhand":     ["Wheat", "Rice", "Apple (Seb)", "Mandua", "Soybean"],
    "Jharkhand":       ["Rice", "Maize (Corn)", "Arhar (Tur/Pigeon Pea)", "Mustard (Sarson)"],
    "Chhattisgarh":    ["Rice", "Maize (Corn)", "Soybean", "Arhar (Tur/Pigeon Pea)"],
}

# ─────────────────────────────────────────
# GENERATE TRAINING DATA
# Based on agronomic science
# ─────────────────────────────────────────
def generate_training_data(n_samples: int = 5000) -> pd.DataFrame:
    """
    Agronomic science pe based realistic
    training data generate karta hai
    """
    np.random.seed(42)
    records = []

    for _ in range(n_samples):
        crop = np.random.choice(ALL_CROPS)
        state = np.random.choice(STATES)
        season = np.random.choice(SEASONS)

        # Crop ki yield range lo
        y_min, y_max = CROP_YIELD_RANGES.get(crop, (1.0, 5.0))

        # State suitability check
        suitable_crops = STATE_CROP_SUITABILITY.get(state, [])
        if crop in suitable_crops:
            # Suitable state mein yield better hogi
            base_yield = np.random.uniform(
                y_min + (y_max - y_min) * 0.4,
                y_max
            )
        else:
            # Non-suitable state mein yield kam hogi
            base_yield = np.random.uniform(
                y_min,
                y_min + (y_max - y_min) * 0.6
            )

        # Weather conditions
        rainfall = np.random.uniform(200, 2500)
        temperature = np.random.uniform(10, 45)
        humidity = np.random.uniform(30, 95)
        soil_ph = np.random.uniform(5.0, 8.5)
        fertilizer = np.random.uniform(0, 400)
        irrigation = np.random.uniform(0, 100)

        # Weather ka yield pe impact
        if 500 <= rainfall <= 1500:
            base_yield *= np.random.uniform(1.0, 1.2)
        elif rainfall < 300:
            base_yield *= np.random.uniform(0.5, 0.8)

        if 15 <= temperature <= 35:
            base_yield *= np.random.uniform(1.0, 1.1)
        elif temperature > 40:
            base_yield *= np.random.uniform(0.6, 0.8)

        if 6.0 <= soil_ph <= 7.5:
            base_yield *= np.random.uniform(1.0, 1.1)

        # Final yield — range ke andar rakho
        final_yield = np.clip(base_yield, y_min * 0.5, y_max * 1.2)

        records.append({
            "Crop": crop,
            "State": state,
            "Season": season,
            "Rainfall_mm": rainfall,
            "Temperature_C": temperature,
            "Humidity_%": humidity,
            "Soil_pH": soil_ph,
            "Fertilizer_kg_per_ha": fertilizer,
            "Irrigation_%": irrigation,
            "Yield_ton_per_ha": round(final_yield, 3),
        })

    return pd.DataFrame(records)


# ─────────────────────────────────────────
# TRAIN MODEL
# ─────────────────────────────────────────
@st.cache_resource
def train_model():
    """
    RandomForest model train karta hai
    Returns: model, encoders, r2, mae
    """
    df = generate_training_data(5000)

    le_crop  = LabelEncoder()
    le_state = LabelEncoder()
    le_season = LabelEncoder()

    df["Crop_enc"]   = le_crop.fit_transform(df["Crop"])
    df["State_enc"]  = le_state.fit_transform(df["State"])
    df["Season_enc"] = le_season.fit_transform(df["Season"])

    features = [
        "Crop_enc", "State_enc", "Season_enc",
        "Rainfall_mm", "Temperature_C", "Humidity_%",
        "Soil_pH", "Fertilizer_kg_per_ha", "Irrigation_%"
    ]

    X = df[features]
    y = df["Yield_ton_per_ha"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2  = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    return model, le_crop, le_state, le_season, r2, mae


# ─────────────────────────────────────────
# PREDICT YIELD
# ─────────────────────────────────────────
def predict_yield(
    model, le_crop, le_state, le_season,
    crop, state, season,
    rainfall, temperature, humidity,
    soil_ph, fertilizer, irrigation,
    area_value, area_unit
):
    """
    User ke inputs se yield predict karta hai
    Area user ki local unit mein deta hai
    """
    try:
        # Encode inputs
        crop_enc   = le_crop.transform([crop])[0]
        state_enc  = le_state.transform([state])[0]
        season_enc = le_season.transform([season])[0]

        features = [[
            crop_enc, state_enc, season_enc,
            rainfall, temperature, humidity,
            soil_ph, fertilizer, irrigation
        ]]

        # Predict per hectare
        yield_per_ha = model.predict(features)[0]

        # Area convert karo hectare mein
        area_ha = convert_to_hectare(area_value, area_unit, state)

        # Total yield
        total_yield = yield_per_ha * area_ha

        # Per unit yield
        yield_per_unit = yield_per_ha * convert_to_hectare(
            1, area_unit, state
        )

        # Suitability warning
        suitable = STATE_CROP_SUITABILITY.get(state, [])
        warning = None
        if suitable and crop not in suitable:
            warning = f"⚠️ {crop} is not commonly grown in {state}. Yield may be lower than expected."

        return {
            "yield_per_ha":   round(yield_per_ha, 2),
            "yield_per_unit": round(yield_per_unit, 2),
            "total_yield":    round(total_yield, 2),
            "area_ha":        round(area_ha, 3),
            "area_value":     area_value,
            "area_unit":      area_unit,
            "warning":        warning,
        }

    except Exception as e:
        return None


# ─────────────────────────────────────────
# GET SAMPLE DATA (for charts)
# ─────────────────────────────────────────
def get_sample_data():
    return generate_training_data(1000)