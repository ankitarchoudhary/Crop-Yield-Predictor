# chat_handler.py
# KrishiBot — AI Farming Assistant
# Author: Ankita Choudhary | IIT Guwahati
# Powered by Groq API (Free)

from groq import Groq
import streamlit as st

# ─────────────────────────────────────────
# KRISHIBOT SYSTEM PROMPT
# ─────────────────────────────────────────
SYSTEM_PROMPT = """You are KrishiBot — an expert AI farming assistant 
for Indian farmers. You have deep knowledge of:
- Indian agriculture, crops, and farming practices
- ICAR guidelines and recommendations
- Government schemes for farmers (PM-KISAN, PMFBY, etc.)
- Soil health, irrigation, and fertilizer management
- Pest and disease control
- Organic farming techniques
- Market prices and mandi rates
- Weather-based farming decisions

IMPORTANT RULES:
1. Always give practical, actionable advice
2. Keep answers simple — farmers may not be highly educated
3. Always respond in the SAME language the user writes in
4. If asked in Hindi, respond in Hindi
5. If asked in Tamil, respond in Tamil
6. Mention government schemes wherever relevant
7. Always be respectful and encouraging
8. Keep responses concise — 3 to 5 points maximum
9. Use simple examples from daily farming life
10. Never give wrong or misleading information
"""

# ─────────────────────────────────────────
# 100 QUICK QUESTIONS — Category wise
# ─────────────────────────────────────────
QUICK_QUESTIONS = {
    "🌾 Crop Care": [
        "What is the best time to sow wheat in Punjab?",
        "How many days does rice take to mature?",
        "What is the ideal plant spacing for maize?",
        "How to increase sugarcane yield?",
        "What are the best varieties of wheat in India?",
        "How to grow tomatoes in summer?",
        "What is the best season to grow onions?",
        "How to improve mango flowering?",
        "What is the ideal time to harvest potato?",
        "How to grow saffron in Kashmir?",
        "What are HYV seeds and where to get them?",
        "How to grow cotton successfully in Maharashtra?",
        "What is intercropping and how does it help?",
        "How to do crop rotation properly?",
        "How to grow turmeric successfully?",
        "What is the best variety of rice for West Bengal?",
        "How to grow apple in Himachal Pradesh?",
        "What is mixed farming?",
        "How to increase banana yield?",
        "How to grow brinjal in a small farm?",
    ],

    "💧 Water & Irrigation": [
        "How much water does wheat need per week?",
        "What is drip irrigation and is it useful for small farmers?",
        "How to conserve water in dry regions like Rajasthan?",
        "What is sprinkler irrigation?",
        "How to check if my crop needs water?",
        "What is the best time to irrigate crops?",
        "How to get subsidy on drip irrigation?",
        "How does waterlogging harm crops?",
        "What is rainwater harvesting for farms?",
        "How to irrigate sugarcane efficiently?",
    ],

    "🧪 Soil & Fertilizer": [
        "How to improve soil fertility naturally?",
        "What is NPK fertilizer and how to use it?",
        "What is the ideal soil pH for wheat?",
        "How to do soil testing for free?",
        "What is vermicompost and how to make it at home?",
        "How to fix acidic soil?",
        "How to fix alkaline soil?",
        "What is green manuring?",
        "How much urea should I use for rice?",
        "What is DAP fertilizer and when to use it?",
        "How to make organic fertilizer at home?",
        "What is micronutrient deficiency in crops?",
        "How to improve sandy soil for farming?",
        "What is soil organic matter and why is it important?",
        "How to use neem cake as fertilizer?",
    ],

    "🐛 Pest & Disease": [
        "How to control aphids on mustard crop?",
        "What is stem borer in rice and how to control it?",
        "How to prevent fungal disease in wheat?",
        "What is powdery mildew and how to treat it?",
        "How to control weeds without chemicals?",
        "What is integrated pest management (IPM)?",
        "How to make organic pesticide at home?",
        "What is leaf curl disease in cotton?",
        "How to protect crops from locusts?",
        "What is blight disease in potato?",
        "How to control mealybugs on fruits?",
        "What is yellow mosaic virus in soybean?",
        "How to protect stored grains from pests?",
        "How to control fruit fly in mango?",
        "What is brown planthopper in rice?",
    ],

    "🌦️ Weather & Season": [
        "What crops should I grow in Kharif season?",
        "What crops should I grow in Rabi season?",
        "How does climate change affect farming?",
        "What to do if there is less rainfall this year?",
        "How to protect crops from frost?",
        "How to protect crops from hailstorm?",
        "What crops grow best in dry weather?",
        "How to manage crops during heavy rainfall?",
        "What is the effect of high temperature on wheat?",
        "How to get weather forecast for my village?",
    ],

    "💰 Government Schemes": [
        "What is PM-KISAN scheme and how to apply?",
        "What is PMFBY crop insurance scheme?",
        "How to get Kisan Credit Card?",
        "What is e-NAM and how does it help farmers?",
        "How to get subsidy on farm equipment?",
        "What is Pradhan Mantri Krishi Sinchayee Yojana?",
        "How to apply for soil health card?",
        "What is the Minimum Support Price (MSP)?",
        "How to get free seeds from government?",
        "What is Paramparagat Krishi Vikas Yojana?",
        "How to get loan for farming from government bank?",
        "What is National Food Security Mission?",
        "How to register on PM-KISAN portal?",
        "What benefits do women farmers get?",
        "What is Kisan Suvidha app?",
    ],

    "📈 Market & Prices": [
        "How to get best price for my crop?",
        "What is mandi and how does it work?",
        "How to sell crops directly without middlemen?",
        "What is the MSP for wheat in 2024?",
        "How to check current mandi rates on phone?",
        "What is FPO (Farmer Producer Organisation)?",
        "How to do contract farming?",
        "What is the best time to sell onions?",
        "How to store grains to get better price later?",
        "How to export Indian crops abroad?",
    ],

    "🌱 Organic Farming": [
        "How to start organic farming?",
        "What is the difference between organic and chemical farming?",
        "How to get organic certification in India?",
        "What is natural farming (Zero Budget)?",
        "How to make jeevamrit at home?",
        "How to make beejamrit for seed treatment?",
        "What crops are best for organic farming?",
        "How to control pests in organic farming?",
        "Where to sell organic produce at better price?",
        "What government support is available for organic farming?",
    ],
}

# Flat list of all questions
ALL_QUICK_QUESTIONS = [
    q for questions in QUICK_QUESTIONS.values()
    for q in questions
]


# ─────────────────────────────────────────
# GROQ CLIENT
# ─────────────────────────────────────────
def get_groq_client(api_key: str):
    """Initialize Groq client"""
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


# ─────────────────────────────────────────
# CHAT FUNCTION
# ─────────────────────────────────────────
def chat_with_krishibot(
    user_message: str,
    chat_history: list,
    api_key: str,
    language: str = "English",
    prediction_context: dict = None,
) -> str:
    """
    Send message to KrishiBot via Groq API
    Returns AI response as string
    """
    client = get_groq_client(api_key)
    if not client:
        return "❌ Invalid API key. Please check your Groq API key."

    # Build system prompt with context
    system = SYSTEM_PROMPT
    if prediction_context:
        system += f"""
\nCurrent farmer context:
- Location: {prediction_context.get('village', '')}, 
  {prediction_context.get('tehsil', '')},
  {prediction_context.get('district', '')},
  {prediction_context.get('state', '')}
- Crop: {prediction_context.get('crop', '')}
- Season: {prediction_context.get('season', '')}
- Land: {prediction_context.get('area_value', '')} 
  {prediction_context.get('area_unit', '')}
- Predicted Yield: {prediction_context.get('yield', '')} ton/ha
Use this context to give personalized advice.
"""

    if language != "English":
        system += f"\nIMPORTANT: The farmer has selected '{language}' language. Always respond in {language}."

    # Build messages
    messages = [{"role": "system", "content": system}]

    # Add chat history (last 10 messages)
    for msg in chat_history[-10:]:
        messages.append({
            "role":    msg["role"],
            "content": msg["content"]
        })

    # Add current message
    messages.append({
        "role":    "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model       = "llama-3.1-70b-versatile",
            messages    = messages,
            temperature = 0.7,
            max_tokens  = 500,
        )
        return response.choices[0].message.content

    except Exception as e:
        err = str(e)
        if "401" in err:
            return "❌ Invalid Groq API key. Please check and re-enter."
        if "429" in err:
            return "⏳ Too many requests. Please wait a moment and try again."
        if "model" in err.lower():
            return "❌ Model not available. Please try again."
        return f"❌ Error: {err[:100]}"


# ─────────────────────────────────────────
# GET QUESTIONS BY CATEGORY
# ─────────────────────────────────────────
def get_categories() -> list:
    """Return list of question categories"""
    return list(QUICK_QUESTIONS.keys())


def get_questions_by_category(category: str) -> list:
    """Return questions for a given category"""
    return QUICK_QUESTIONS.get(category, [])