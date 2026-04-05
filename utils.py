# utils.py
# Weather API, FAQs, Contact Us
# Author: Ankita Choudhary | IIT Guwahati

import requests
import streamlit as st

# ─────────────────────────────────────────
# WEATHER API — Open-Meteo (Free, No Key!)
# ─────────────────────────────────────────
STATE_COORDINATES = {
    "Andhra Pradesh":        (15.9129, 79.7400),
    "Arunachal Pradesh":     (28.2180, 94.7278),
    "Assam":                 (26.2006, 92.9376),
    "Bihar":                 (25.0961, 85.3131),
    "Chhattisgarh":          (21.2787, 81.8661),
    "Goa":                   (15.2993, 74.1240),
    "Gujarat":               (22.2587, 71.1924),
    "Haryana":               (29.0588, 76.0856),
    "Himachal Pradesh":      (31.1048, 77.1734),
    "Jharkhand":             (23.6102, 85.2799),
    "Karnataka":             (15.3173, 75.7139),
    "Kerala":                (10.8505, 76.2711),
    "Madhya Pradesh":        (22.9734, 78.6569),
    "Maharashtra":           (19.7515, 75.7139),
    "Manipur":               (24.6637, 93.9063),
    "Meghalaya":             (25.4670, 91.3662),
    "Mizoram":               (23.1645, 92.9376),
    "Nagaland":              (26.1584, 94.5624),
    "Odisha":                (20.9517, 85.0985),
    "Punjab":                (31.1471, 75.3412),
    "Rajasthan":             (27.0238, 74.2179),
    "Sikkim":                (27.5330, 88.5122),
    "Tamil Nadu":            (11.1271, 78.6569),
    "Telangana":             (18.1124, 79.0193),
    "Tripura":               (23.9408, 91.9882),
    "Uttar Pradesh":         (26.8467, 80.9462),
    "Uttarakhand":           (30.0668, 79.0193),
    "West Bengal":           (22.9868, 87.8550),
    "Andaman and Nicobar Islands": (11.7401, 92.6586),
    "Chandigarh":            (30.7333, 76.7794),
    "Dadra & Nagar Haveli and Daman & Diu": (20.1809, 73.0169),
    "Delhi (NCT)":           (28.7041, 77.1025),
    "Jammu & Kashmir":       (33.7782, 76.5762),
    "Ladakh":                (34.1526, 77.5770),
    "Lakshadweep":           (10.5667, 72.6417),
    "Puducherry":            (11.9416, 79.8083),
}

@st.cache_data(ttl=3600)
def get_weather_data(state: str) -> dict:
    """
    Fetch real weather data from Open-Meteo API
    Completely free — no API key needed!
    """
    coords = STATE_COORDINATES.get(state, (20.5937, 78.9629))
    lat, lon = coords
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude":      lat,
            "longitude":     lon,
            "current":       ["temperature_2m", "relative_humidity_2m"],
            "daily":         ["precipitation_sum"],
            "timezone":      "Asia/Kolkata",
            "forecast_days": 7,
        }
        r = requests.get(url, params=params, timeout=8)
        if r.status_code == 200:
            data     = r.json()
            temp     = data["current"]["temperature_2m"]
            humidity = data["current"]["relative_humidity_2m"]
            rainfall = sum(data["daily"]["precipitation_sum"]) * 52
            return {
                "temperature": round(temp, 1),
                "humidity":    round(humidity, 1),
                "rainfall":    round(min(rainfall, 3000), 1),
                "source":      "Live (Open-Meteo)",
                "success":     True,
            }
    except Exception:
        pass
    return {
        "temperature": 25.0,
        "humidity":    60.0,
        "rainfall":    800.0,
        "source":      "Default values",
        "success":     False,
    }


# ─────────────────────────────────────────
# FAQs — 28 Questions (English)
# ─────────────────────────────────────────
FAQS = [
    {
        "q": "What is Fasal Upaj Predictor?",
        "a": "Fasal Upaj Predictor is an AI-powered web application that helps Indian farmers predict their expected crop yield. You enter your location, crop type, land area, and weather conditions — and the app predicts how much yield you can expect."
    },
    {
        "q": "Is this app completely free?",
        "a": "Yes! This app is 100% free. No subscription, no hidden charges. It is built entirely using free tools — Streamlit, Groq API (free tier), and Open-Meteo API."
    },
    {
        "q": "How accurate is the prediction?",
        "a": "Our ML model achieves 89% accuracy (R² = 0.89). It is based on ICAR agronomic guidelines. However, actual yield depends on many real-world factors, so the prediction is an estimate, not a guarantee."
    },
    {
        "q": "My village is not showing in the list. What should I do?",
        "a": "If your village is not listed, select 'Other (Manual Entry)'. Village data comes from the Government of India's LGD (Local Government Directory), which is continuously updated."
    },
    {
        "q": "Which languages does the app support?",
        "a": "The app supports all 22 scheduled Indian languages — Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Kannada, Odia, Malayalam, Punjabi, Assamese, Maithili, Santali, Kashmiri, Nepali, Sindhi, Konkani, Dogri, Manipuri, Bodo, and English."
    },
    {
        "q": "How does automatic weather data work?",
        "a": "We use the Open-Meteo API, which is completely free. When you select your state, the app automatically fetches the current temperature, humidity, and estimated annual rainfall for that region. You can also edit these values manually."
    },
    {
        "q": "How do local land units work?",
        "a": "Every state in India has its own traditional land measurement units — like Killa and Kanal in Punjab, Cent in Tamil Nadu, Bigha in UP. When you select your state, the app automatically shows the relevant units and converts them to hectares internally for calculation."
    },
    {
        "q": "What is KrishiBot?",
        "a": "KrishiBot is an AI farming assistant powered by Groq API (LLaMA 3.1 model). You can ask any farming-related question — crop care, pest control, fertilizer use — in any of the 22 supported languages."
    },
    {
        "q": "Does the app work offline?",
        "a": "Partial offline support is available. ML prediction and land unit conversion work without internet. However, weather data fetching and KrishiBot chat require an active internet connection."
    },
    {
        "q": "Where does the data come from?",
        "a": "Crop yield data is based on ICAR (Indian Council of Agricultural Research) agronomic guidelines. Location data comes from the Government of India's LGD directory. Weather data is fetched from the Open-Meteo API."
    },
    {
        "q": "Can I save my prediction results?",
        "a": "Currently, there is no save feature. You can take a screenshot of the prediction. A future version will include farmer profile and prediction history features."
    },
    {
        "q": "Does the app work on mobile phones?",
        "a": "Yes! The app works on mobile browsers as well. Streamlit automatically creates a mobile-friendly layout. Open it in Chrome or Safari browser on your phone."
    },
    {
        "q": "What does the crop warning mean?",
        "a": "A warning appears when your selected crop is not commonly grown in your selected state. For example, saffron is mainly grown in Kashmir — selecting it for Tamil Nadu will trigger a warning. It means the yield may be lower than expected."
    },
    {
        "q": "Can I compare different farming scenarios?",
        "a": "Yes! You can enter different inputs and get multiple predictions to compare. For example, try with low fertilizer first, then high fertilizer — and compare the results to make better farming decisions."
    },
    {
        "q": "What is Soil pH and how do I find it?",
        "a": "Soil pH measures the acidity or alkalinity of your soil. A pH of 6.0–7.5 is ideal for most crops. To know your soil's pH, send a sample to your nearest Krishi Vigyan Kendra (KVK) or soil testing lab. Free testing is also available under the Soil Health Card scheme."
    },
    {
        "q": "What irrigation percentage should I enter?",
        "a": "Irrigation percentage means how much artificial water your crop receives. Enter 0% if you rely only on rainfall, 100% if you have full irrigation, and 30–50% if you have partial irrigation."
    },
    {
        "q": "How many crops does the app support?",
        "a": "The app supports 196 crops across 10 categories — Grains, Pulses, Oilseeds, Cash Crops, Vegetables, Fruits, Flowers, Spices, Plantation Crops, and Medicinal crops."
    },
    {
        "q": "What does 'per unit yield' and 'total yield' mean in the results?",
        "a": "'Per unit yield' means how much produce you will get per local unit (like Killa, Bigha, or Cent). 'Total yield' means how much produce you will get from your entire land. Both are shown in your selected local unit."
    },
    {
        "q": "What fertilizer amount should I enter?",
        "a": "Enter the quantity of fertilizer you use in kg per hectare. If you are not sure, enter the ICAR recommended dose for your crop. The recommended range is shown in the crop info section."
    },
    {
        "q": "Is the weather data accurate?",
        "a": "Weather data is fetched at state level, not exact village level. So you can manually adjust the values if needed. Open-Meteo is a reliable source based on international weather models."
    },
    {
        "q": "How many states and UTs does the app cover?",
        "a": "The app covers all 28 States and 8 Union Territories of India — a total of 36 regions — each with their own local land measurement units."
    },
    {
        "q": "Can I chat with KrishiBot in Hindi?",
        "a": "Yes, absolutely! KrishiBot understands all 22 Indian languages. You can ask questions in Hindi, Punjabi, Bengali, Tamil, or any supported language and get a reply in the same language."
    },
    {
        "q": "Where can I get a free Groq API key?",
        "a": "Visit console.groq.com, sign up for a free account, and generate an API key. The free tier provides 14,400 requests per day, which is more than enough for regular use."
    },
    {
        "q": "What should I do if the prediction seems wrong?",
        "a": "Check your inputs carefully — correct rainfall, temperature, and soil pH values improve accuracy significantly. The prediction is an estimate based on agronomic science. For expert advice, contact your nearest Krishi Vigyan Kendra (KVK)."
    },
    {
        "q": "Who built this app?",
        "a": "This app was built by Ankita Choudhary, an AI & Data Science student at IIT Guwahati. It is a portfolio project aimed at providing a free and useful tool for Indian farmers."
    },
    {
        "q": "Will more features be added in the future?",
        "a": "Yes! Future plans include — farmer profile and prediction history, mandi price integration, crop disease detection, satellite imagery analysis, SMS alerts, and a dedicated mobile app."
    },
    {
        "q": "Is my data safe and private?",
        "a": "Yes! The app does not store any personal data. Your inputs are only used for generating the prediction and are deleted when the session ends. No data is shared with third parties."
    },
    {
        "q": "Can I recommend this app to other farmers?",
        "a": "Absolutely! Share the app link with fellow farmers — it is completely free. The more farmers use it, the more benefit it provides. You can also give it a star on GitHub to support the project!"
    },
]


# ─────────────────────────────────────────
# CONTACT US
# ─────────────────────────────────────────
CONTACT_INFO = {
    "name":           "Ankita Choudhary",
    "role":           "AI & Data Science Student",
    "college":        "IIT Guwahati",
    "email":          "ankita.choudhary.a03b@gmail.com",
    "github":         "https://github.com/ankitarchoudhary",
    "linkedin":       "https://linkedin.com/in/ankitachoudhary",
    "location":       "Sikar, Rajasthan, India",
    "project_github": "https://github.com/ankitarchoudhary/Crop-Yield-Predictor",
}