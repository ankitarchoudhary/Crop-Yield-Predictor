# data_handler.py
# Handles all data for Fasal Upaj Predictor
# Author: Ankita Choudhary | IIT Guwahati

import pandas as pd
import numpy as np
import streamlit as st

# Location data from LGD (Govt of India)
from location_db import (
    get_all_states,
    get_districts,
    get_tehsils,
    get_villages,
)

# ─────────────────────────────────────────
# CROPS — Category wise (150+ Indian crops)
# ─────────────────────────────────────────
CROPS = {
    "🌾 Grains & Cereals": [
        "Rice", "Wheat", "Maize (Corn)", "Barley",
        "Jowar (Sorghum)", "Bajra (Pearl Millet)",
        "Ragi (Finger Millet)", "Oats", "Small Millet (Kutki)",
        "Kodo Millet", "Foxtail Millet", "Proso Millet",
        "Barnyard Millet", "Amaranth (Rajgira)"
    ],
    "🫘 Pulses & Legumes": [
        "Arhar (Tur/Pigeon Pea)", "Moong (Green Gram)",
        "Urad (Black Gram)", "Chickpea (Chana)", "Lentil (Masur)",
        "Rajma (Kidney Bean)", "Lobiya (Cowpea)", "Moth Bean",
        "Horse Gram (Kulthi)", "Field Pea (Matar)",
        "Flat Bean (Sem)", "Cluster Bean (Guar)",
        "Faba Bean (Bakla)", "Lakh (Grass Pea)"
    ],
    "🌻 Oilseeds": [
        "Mustard (Sarson)", "Groundnut (Moongfali)", "Soybean",
        "Sunflower", "Sesame (Til)", "Linseed (Alsi)",
        "Castor (Arandi)", "Safflower (Kusum)", "Niger Seed",
        "Rapeseed", "Toria (Yellow Sarson)"
    ],
    "🎋 Cash Crops": [
        "Sugarcane", "Cotton (Kapas)", "Jute", "Tobacco",
        "Indigo", "Hemp (Bhang)", "Flax (Patsan)"
    ],
    "🥬 Vegetables": [
        "Tomato", "Onion", "Potato", "Brinjal (Baingan)",
        "Cauliflower", "Cabbage", "Spinach (Palak)",
        "Peas (Matar)", "Bhindi (Okra)", "Bitter Gourd (Karela)",
        "Bottle Gourd (Lauki)", "Capsicum (Shimla Mirch)",
        "Carrot (Gajar)", "Radish (Mooli)", "Beetroot",
        "Garlic (Lahsun)", "Pumpkin (Kaddu)",
        "Ridge Gourd (Tori)", "Snake Gourd", "Sponge Gourd",
        "Tinda (Indian Round Gourd)", "Parwal (Pointed Gourd)",
        "Colocasia (Arbi)", "Sweet Potato (Shakarkand)",
        "Yam (Suran)", "Turnip (Shalgam)", "Drumstick (Sahjan)",
        "Cucumber (Kheera)", "Ash Gourd (Petha)", "Lettuce",
        "Celery", "Broccoli", "Spring Onion",
        "Fenugreek Leaves (Methi)",
        "Coriander Leaves (Hara Dhaniya)",
        "Curry Leaves", "Mint (Pudina)",
        "Bathua", "Amaranth Leaves (Chaulai)"
    ],
    "🍎 Fruits": [
        "Mango (Aam)", "Banana (Kela)", "Apple (Seb)",
        "Grapes (Angoor)", "Guava (Amrood)", "Papaya (Papita)",
        "Pomegranate (Anar)", "Orange (Santra)", "Lemon (Nimbu)",
        "Litchi", "Pineapple (Ananas)", "Watermelon (Tarbuj)",
        "Muskmelon (Kharbooja)", "Strawberry", "Kiwi",
        "Pear (Nashpati)", "Plum (Aloo Bukhara)", "Peach (Aadoo)",
        "Apricot (Khurmani)", "Cherry (Cheri)", "Fig (Anjeer)",
        "Dates (Khajoor)", "Avocado", "Custard Apple (Sharifa)",
        "Wood Apple (Bel)", "Indian Gooseberry (Amla)",
        "Jackfruit (Kathal)", "Mulberry (Shahtoot)",
        "Jamun (Java Plum)", "Karonda", "Phalsa",
        "Star Fruit (Kamrakh)", "Dragon Fruit", "Passion Fruit",
        "Tamarind (Imli)", "Sapota (Chikoo)", "Loquat (Lukaat)"
    ],
    "🌺 Flowers": [
        "Rose (Gulab)", "Marigold (Genda)", "Jasmine (Chameli)",
        "Chrysanthemum (Guldaudi)", "Gladiolus",
        "Tuberose (Rajnigandha)", "Lotus (Kamal)",
        "Sunflower (Surajmukhi)", "Dahlia", "Orchid",
        "Carnation", "Lily", "Gerbera", "Anthurium",
        "Bird of Paradise", "Crossandra", "Aster",
        "Larkspur", "Pansy", "Zinnia"
    ],
    "🌿 Spices & Herbs": [
        "Turmeric (Haldi)", "Dry Ginger (Sonth)",
        "Red Chilli (Lal Mirch)", "Green Chilli (Hari Mirch)",
        "Coriander (Dhaniya)", "Cumin (Jeera)",
        "Fenugreek (Methi Dana)", "Cardamom (Elaichi)",
        "Black Pepper (Kali Mirch)", "Clove (Laung)",
        "Nutmeg (Jaiphal)", "Cinnamon (Dalchini)",
        "Star Anise (Chakri Phool)", "Bay Leaf (Tej Patta)",
        "Ajwain (Carom Seeds)", "Fennel (Saunf)",
        "Asafoetida (Hing)", "Mustard Seeds (Sarson Dana)",
        "Poppy Seeds (Khus Khus)", "Saffron (Kesar)",
        "Vanilla", "Kokum", "Lemongrass", "Brahmi",
        "Stevia", "Isabgol (Psyllium)"
    ],
    "🍵 Plantation Crops": [
        "Tea (Chai)", "Coffee (Kaphi)", "Coconut (Nariyal)",
        "Areca Nut (Supari)", "Rubber", "Cashew (Kaju)",
        "Cocoa", "Oil Palm", "Eucalyptus",
        "Bamboo (Baans)", "Teak (Sagwan)"
    ],
    "🌱 Medicinal & Aromatic": [
        "Aloe Vera", "Neem", "Tulsi (Holy Basil)",
        "Lavender", "Peppermint", "Spearmint",
        "Chamomile", "Calendula", "Giloy (Guduchi)",
        "Shatavari", "Mulethi (Liquorice)", "Kalmegh",
        "Safed Musli", "Bhumi Amla", "Jatamansi",
        "Valerian", "Ashwagandha (Withania)"
    ]
}

# Flat list — ML model ke liye
ALL_CROPS = [crop for category in CROPS.values() for crop in category]

SEASONS = [
    "Kharif (Jun-Oct)",
    "Rabi (Nov-Apr)",
    "Zaid (Mar-Jun)",
    "Year-round"
]

# ─────────────────────────────────────────
# LAND UNITS — 28 States + 8 UTs
# ─────────────────────────────────────────
LAND_UNITS = {
    "Andhra Pradesh": {
        "units": ["Acre", "Cent", "Guntha"],
        "to_hectare": {
            "Acre": 0.404, "Cent": 0.004, "Guntha": 0.010
        }
    },
    "Arunachal Pradesh": {
        "units": ["Acre", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Hectare": 1.000
        }
    },
    "Assam": {
        "units": ["Bigha", "Katha", "Lecha", "Acre"],
        "to_hectare": {
            "Bigha": 0.133, "Katha": 0.013,
            "Lecha": 0.001, "Acre": 0.404
        }
    },
    "Bihar": {
        "units": ["Bigha", "Katha", "Dhur", "Acre"],
        "to_hectare": {
            "Bigha": 0.200, "Katha": 0.013,
            "Dhur": 0.002, "Acre": 0.404
        }
    },
    "Chhattisgarh": {
        "units": ["Acre", "Bigha", "Dismil"],
        "to_hectare": {
            "Acre": 0.404, "Bigha": 0.133, "Dismil": 0.004
        }
    },
    "Goa": {
        "units": ["Acre", "Guntha"],
        "to_hectare": {
            "Acre": 0.404, "Guntha": 0.010
        }
    },
    "Gujarat": {
        "units": ["Bigha", "Vigha", "Acre"],
        "to_hectare": {
            "Bigha": 0.168, "Vigha": 0.168, "Acre": 0.404
        }
    },
    "Haryana": {
        "units": ["Acre", "Kanal", "Marla", "Bigha"],
        "to_hectare": {
            "Acre": 0.404, "Kanal": 0.050,
            "Marla": 0.003, "Bigha": 0.200
        }
    },
    "Himachal Pradesh": {
        "units": ["Bigha", "Biswa", "Kanal", "Acre"],
        "to_hectare": {
            "Bigha": 0.200, "Biswa": 0.013,
            "Kanal": 0.050, "Acre": 0.404
        }
    },
    "Jharkhand": {
        "units": ["Bigha", "Katha", "Acre"],
        "to_hectare": {
            "Bigha": 0.200, "Katha": 0.013, "Acre": 0.404
        }
    },
    "Karnataka": {
        "units": ["Acre", "Guntha", "Are"],
        "to_hectare": {
            "Acre": 0.404, "Guntha": 0.010, "Are": 0.010
        }
    },
    "Kerala": {
        "units": ["Cent", "Acre", "Are", "Ankanam"],
        "to_hectare": {
            "Cent": 0.004, "Acre": 0.404,
            "Are": 0.010, "Ankanam": 0.007
        }
    },
    "Madhya Pradesh": {
        "units": ["Acre", "Bigha", "Biswa"],
        "to_hectare": {
            "Acre": 0.404, "Bigha": 0.133, "Biswa": 0.008
        }
    },
    "Maharashtra": {
        "units": ["Acre", "Guntha", "Are"],
        "to_hectare": {
            "Acre": 0.404, "Guntha": 0.010, "Are": 0.010
        }
    },
    "Manipur": {
        "units": ["Acre", "Pari", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Pari": 0.050, "Hectare": 1.000
        }
    },
    "Meghalaya": {
        "units": ["Acre", "Bigha", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Bigha": 0.133, "Hectare": 1.000
        }
    },
    "Mizoram": {
        "units": ["Acre", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Hectare": 1.000
        }
    },
    "Nagaland": {
        "units": ["Acre", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Hectare": 1.000
        }
    },
    "Odisha": {
        "units": ["Acre", "Guntha", "Decimal"],
        "to_hectare": {
            "Acre": 0.404, "Guntha": 0.010, "Decimal": 0.004
        }
    },
    "Punjab": {
        "units": ["Killa", "Acre", "Kanal", "Marla"],
        "to_hectare": {
            "Killa": 0.404, "Acre": 0.404,
            "Kanal": 0.050, "Marla": 0.003
        }
    },
    "Rajasthan": {
        "units": ["Bigha", "Biswa", "Acre"],
        "to_hectare": {
            "Bigha": 0.625, "Biswa": 0.031, "Acre": 0.404
        }
    },
    "Sikkim": {
        "units": ["Acre", "Ropani", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Ropani": 0.051, "Hectare": 1.000
        }
    },
    "Tamil Nadu": {
        "units": ["Cent", "Acre", "Ground"],
        "to_hectare": {
            "Cent": 0.004, "Acre": 0.404, "Ground": 0.023
        }
    },
    "Telangana": {
        "units": ["Acre", "Cent", "Guntha"],
        "to_hectare": {
            "Acre": 0.404, "Cent": 0.004, "Guntha": 0.010
        }
    },
    "Tripura": {
        "units": ["Acre", "Bigha", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Bigha": 0.133, "Hectare": 1.000
        }
    },
    "Uttar Pradesh": {
        "units": ["Bigha", "Biswa", "Katha", "Acre"],
        "to_hectare": {
            "Bigha": 0.200, "Biswa": 0.013,
            "Katha": 0.013, "Acre": 0.404
        }
    },
    "Uttarakhand": {
        "units": ["Nali", "Bigha", "Acre"],
        "to_hectare": {
            "Nali": 0.020, "Bigha": 0.200, "Acre": 0.404
        }
    },
    "West Bengal": {
        "units": ["Bigha", "Katha", "Chhatak", "Acre"],
        "to_hectare": {
            "Bigha": 0.133, "Katha": 0.007,
            "Chhatak": 0.000, "Acre": 0.404
        }
    },
    "Andaman and Nicobar Islands": {
        "units": ["Acre", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Hectare": 1.000
        }
    },
    "Chandigarh": {
        "units": ["Acre", "Kanal", "Marla"],
        "to_hectare": {
            "Acre": 0.404, "Kanal": 0.050, "Marla": 0.003
        }
    },
    "Dadra & Nagar Haveli and Daman & Diu": {
        "units": ["Acre", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Hectare": 1.000
        }
    },
    "Delhi (NCT)": {
        "units": ["Acre", "Bigha", "Square Yard"],
        "to_hectare": {
            "Acre": 0.404, "Bigha": 0.160,
            "Square Yard": 0.000836
        }
    },
    "Jammu & Kashmir": {
        "units": ["Kanal", "Marla", "Acre"],
        "to_hectare": {
            "Kanal": 0.050, "Marla": 0.003, "Acre": 0.404
        }
    },
    "Ladakh": {
        "units": ["Acre", "Hectare"],
        "to_hectare": {
            "Acre": 0.404, "Hectare": 1.000
        }
    },
    "Lakshadweep": {
        "units": ["Cent", "Acre"],
        "to_hectare": {
            "Cent": 0.004, "Acre": 0.404
        }
    },
    "Puducherry": {
        "units": ["Cent", "Acre", "Are"],
        "to_hectare": {
            "Cent": 0.004, "Acre": 0.404, "Are": 0.010
        }
    },
}

# STATES — Real LGD data use karo
STATES = get_all_states()


def get_land_units(state: str) -> list:
    """State ke liye land units return karta hai"""
    return LAND_UNITS.get(state, {}).get(
        "units", ["Acre", "Hectare"]
    )


def convert_to_hectare(
    value: float, unit: str, state: str
) -> float:
    """Koi bhi unit ko hectare mein convert karta hai"""
    factor = LAND_UNITS.get(state, {}).get(
        "to_hectare", {}
    ).get(unit, 0.404)
    return round(value * factor, 4)


def get_crop_info(crop: str) -> dict:
    """Crop ki ideal conditions return karta hai"""
    crop_info = {
        "Rice":                   {"ideal_rainfall": "1000-2000mm", "ideal_temp": "20-35°C", "season": "Kharif"},
        "Wheat":                  {"ideal_rainfall": "300-500mm",   "ideal_temp": "15-25°C", "season": "Rabi"},
        "Maize (Corn)":           {"ideal_rainfall": "500-800mm",   "ideal_temp": "18-32°C", "season": "Kharif"},
        "Cotton (Kapas)":         {"ideal_rainfall": "500-1000mm",  "ideal_temp": "25-35°C", "season": "Kharif"},
        "Sugarcane":              {"ideal_rainfall": "1000-1500mm", "ideal_temp": "20-35°C", "season": "Year-round"},
        "Mustard (Sarson)":       {"ideal_rainfall": "250-400mm",   "ideal_temp": "10-25°C", "season": "Rabi"},
        "Bajra (Pearl Millet)":   {"ideal_rainfall": "300-500mm",   "ideal_temp": "25-35°C", "season": "Kharif"},
        "Soybean":                {"ideal_rainfall": "600-800mm",   "ideal_temp": "20-30°C", "season": "Kharif"},
        "Groundnut (Moongfali)":  {"ideal_rainfall": "500-600mm",   "ideal_temp": "25-30°C", "season": "Kharif"},
        "Barley":                 {"ideal_rainfall": "300-500mm",   "ideal_temp": "12-25°C", "season": "Rabi"},
        "Jowar (Sorghum)":        {"ideal_rainfall": "400-600mm",   "ideal_temp": "25-35°C", "season": "Kharif"},
        "Chickpea (Chana)":       {"ideal_rainfall": "300-500mm",   "ideal_temp": "15-25°C", "season": "Rabi"},
        "Potato":                 {"ideal_rainfall": "500-700mm",   "ideal_temp": "15-25°C", "season": "Rabi"},
        "Onion":                  {"ideal_rainfall": "350-500mm",   "ideal_temp": "13-24°C", "season": "Rabi"},
        "Tomato":                 {"ideal_rainfall": "600-800mm",   "ideal_temp": "18-28°C", "season": "Year-round"},
        "Turmeric (Haldi)":       {"ideal_rainfall": "1200-1500mm", "ideal_temp": "20-30°C", "season": "Kharif"},
        "Dry Ginger (Sonth)":     {"ideal_rainfall": "1500-2000mm", "ideal_temp": "20-30°C", "season": "Kharif"},
        "Tea (Chai)":             {"ideal_rainfall": "1500-2500mm", "ideal_temp": "18-28°C", "season": "Year-round"},
        "Coffee (Kaphi)":         {"ideal_rainfall": "1500-2000mm", "ideal_temp": "15-28°C", "season": "Year-round"},
        "Jute":                   {"ideal_rainfall": "1200-1500mm", "ideal_temp": "25-35°C", "season": "Kharif"},
        "Mango (Aam)":            {"ideal_rainfall": "750-2500mm",  "ideal_temp": "24-30°C", "season": "Year-round"},
        "Banana (Kela)":          {"ideal_rainfall": "1200-2200mm", "ideal_temp": "20-35°C", "season": "Year-round"},
        "Apple (Seb)":            {"ideal_rainfall": "1000-1250mm", "ideal_temp": "10-25°C", "season": "Rabi"},
        "Grapes (Angoor)":        {"ideal_rainfall": "600-800mm",   "ideal_temp": "15-35°C", "season": "Rabi"},
        "Rose (Gulab)":           {"ideal_rainfall": "600-1000mm",  "ideal_temp": "15-28°C", "season": "Year-round"},
        "Marigold (Genda)":       {"ideal_rainfall": "400-600mm",   "ideal_temp": "15-30°C", "season": "Year-round"},
        "Coconut (Nariyal)":      {"ideal_rainfall": "1500-2500mm", "ideal_temp": "27-32°C", "season": "Year-round"},
        "Aloe Vera":              {"ideal_rainfall": "300-500mm",   "ideal_temp": "20-35°C", "season": "Year-round"},
        "Saffron (Kesar)":        {"ideal_rainfall": "250-300mm",   "ideal_temp": "10-20°C", "season": "Rabi"},
        "Black Pepper (Kali Mirch)":{"ideal_rainfall":"1500-2500mm","ideal_temp": "20-30°C", "season": "Year-round"},
        "Cardamom (Elaichi)":     {"ideal_rainfall": "1500-2500mm", "ideal_temp": "15-25°C", "season": "Year-round"},
        "Rubber":                 {"ideal_rainfall": "2000-3000mm", "ideal_temp": "25-34°C", "season": "Year-round"},
        "Cashew (Kaju)":          {"ideal_rainfall": "1000-2000mm", "ideal_temp": "20-35°C", "season": "Year-round"},
        "Ragi (Finger Millet)":   {"ideal_rainfall": "500-900mm",   "ideal_temp": "15-30°C", "season": "Kharif"},
        "Lentil (Masur)":         {"ideal_rainfall": "250-400mm",   "ideal_temp": "18-30°C", "season": "Rabi"},
        "Arhar (Tur/Pigeon Pea)": {"ideal_rainfall": "600-1000mm",  "ideal_temp": "18-29°C", "season": "Kharif"},
    }
    return crop_info.get(crop, {
        "ideal_rainfall": "400-1200mm",
        "ideal_temp":     "15-35°C",
        "season":         "Kharif/Rabi"
    })


def get_sample_data() -> pd.DataFrame:
    """Realistic crop yield data generate karta hai"""
    np.random.seed(42)
    n = 1000
    data = {
        "State":               np.random.choice(STATES, n),
        "Crop":                np.random.choice(ALL_CROPS, n),
        "Season":              np.random.choice(SEASONS, n),
        "Year":                np.random.randint(2015, 2024, n),
        "Rainfall_mm":         np.random.uniform(200, 1500, n),
        "Temperature_C":       np.random.uniform(15, 42, n),
        "Humidity_%":          np.random.uniform(30, 90, n),
        "Soil_pH":             np.random.uniform(5.5, 8.5, n),
        "Fertilizer_kg_per_ha":np.random.uniform(50, 300, n),
        "Irrigation_%":        np.random.uniform(0, 100, n),
        "Yield_ton_per_ha":    np.random.uniform(0.5, 8.0, n),
    }
    return pd.DataFrame(data)