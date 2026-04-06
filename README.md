
# 🌾 Fasal Upaj Predictor

### AI-Powered Hyperlocal Crop Yield Predictor for Indian Farmers

**Developer:** Ankita Choudhary | AI & Data Science — IIT Guwahati

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fasal-upaj-predictor.streamlit.app)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[![LGD Data](https://img.shields.io/badge/Data-LGD%20Govt%20of%20India-orange.svg)](https://lgdirectory.gov.in)

---

## 🎯 Problem Statement

Indian farmers lack access to **hyperlocal, multilingual crop yield prediction tools**. Existing solutions are:

- Generic (not India-specific)

- Only in English

- Show results in hectares (farmers use Killa, Katha, Cent!)

- No village-level granularity

## 💡 Solution

**Fasal Upaj Predictor** — A free AI-powered web app that predicts crop yield for Indian farmers in their **local language** and **local land units**!

---

## ✨ Features

| Feature | Details |

|---------|---------|

| 📍 Location | Village → Tehsil → District → State |

| 🗺️ Coverage | 37 States+UTs, 783 Districts, 7076 Tehsils |

| 📏 Land Units | 60+ local units — Killa, Katha, Cent, Guntha, Bigha... |

| 🗣️ Languages | 22 Indian scheduled languages |

| 🤖 AI Chat | KrishiBot — Groq LLaMA 3.1 powered |

| 🌦️ Weather | Auto-fetch via Open-Meteo API (free) |

| 🌾 Crops | 196 crops across 10 categories |

| 📊 Accuracy | 89% (R² = 0.89) ML model |

| 💰 Cost | 100% Free |

---

## 🗺️ Location Hierarchy

**Source:** Government of India — [Local Government Directory](https://lgdirectory.gov.in)

---

## 📏 State-wise Land Units

| State | Local Units |

|-------|------------|

| Punjab / Haryana | Killa, Kanal, Marla |

| Uttar Pradesh | Bigha, Biswa, Katha |

| Bihar | Bigha, Katha, Dhur |

| West Bengal | Bigha, Katha, Chhatak |

| Tamil Nadu | Cent, Ground, Kuzhi |

| Kerala | Cent, Are, Ankanam |

| Karnataka | Guntha, Are |

| Maharashtra | Guntha, Are |

| Rajasthan | Bigha (Pucca), Biswa |

| Gujarat | Bigha, Vigha |

---

## 🌾 Crops Supported (196 Total)

- 🌾 **Grains** — Rice, Wheat, Maize, Bajra, Ragi...

- 🫘 **Pulses** — Arhar, Moong, Urad, Chickpea...

- 🌻 **Oilseeds** — Mustard, Groundnut, Soybean...

- 🎋 **Cash Crops** — Sugarcane, Cotton, Jute...

- 🥬 **Vegetables** — Tomato, Onion, Potato, 30+ more

- 🍎 **Fruits** — Mango, Banana, Apple, 30+ more

- 🌺 **Flowers** — Rose, Marigold, Jasmine, 15+ more

- 🌿 **Spices** — Turmeric, Cardamom, Saffron...

- 🍵 **Plantation** — Tea, Coffee, Coconut, Rubber...

- 🌱 **Medicinal** — Aloe Vera, Tulsi, Ashwagandha...

---

## 🛠️ Tech Stack

| Tool | Purpose | Cost |

|------|---------|------|

| Streamlit | Web UI | Free |

| Groq (LLaMA 3.1) | KrishiBot AI | Free |

| scikit-learn | ML Prediction | Free |

| Open-Meteo | Weather API | Free |

| LGD (Govt of India) | Location Data | Free |

| Plotly | Charts | Free |

| deep-translator | 22 Languages | Free |

| Streamlit Cloud | Hosting | Free |

**Total Cost: ₹0** 🎉

---

## 🚀 Local Setup

```bash

# Clone

git clone https://github.com/ankitarchoudhary/Crop-Yield-Predictor

cd Crop-Yield-Predictor

# Install

pip install -r requirements.txt

# Add API keys

echo "GROQ_API_KEY=your_key_here" > .env

# Run

streamlit run app.py

```

---

## 📊 Data Sources

| Data | Source |

|------|--------|

| Location (State/District/Tehsil) | LGD, Govt of India |

| Villages | LGD Live API |

| Crop Yield Guidelines | ICAR |

| Weather | Open-Meteo (IMD based) |

| MSP Prices | CACP, Govt of India |

---

## 👩‍💻 Developer

**Ankita Choudhary**

AI & Data Science | IIT Guwahati

[![GitHub](https://img.shields.io/badge/GitHub-ankitarchoudhary-black.svg)](https://github.com/ankitarchoudhary)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankita_Choudhary-blue.svg)](https://linkedin.com/in/ankitachoudhary)

---

*Built with ❤️ for Indian Farmers | IIT Guwahati*

