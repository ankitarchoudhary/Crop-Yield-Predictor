# app.py
# Fasal Upaj Predictor — Main Application
# Author: Ankita Choudhary | IIT Guwahati
from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data_handler import (
    CROPS, ALL_CROPS, STATES, SEASONS,
    get_districts, get_tehsils, get_villages,
    get_land_units, convert_to_hectare, get_crop_info
)
from predictor import train_model, predict_yield, generate_training_data
from utils import get_weather_data, FAQS, CONTACT_INFO
from chat_handler import (
    chat_with_krishibot, get_categories,
    get_questions_by_category, ALL_QUICK_QUESTIONS
)

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Fasal Upaj Predictor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS THEME — Earthy Green (Readable)
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    background-color: #1a2e0a !important;
    color: #e8f5b0 !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #1a2e0a !important;
}
[data-testid="stMain"] {
    background-color: #1a2e0a !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a0a 0%, #243d0d 100%) !important;
    border-right: 1px solid #4a7020 !important;
}
[data-testid="stSidebar"] * { color: #c8e88a !important; }
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #d4e88a !important;
}
.crop-card {
    background: linear-gradient(135deg, #243d0d, #2d4f10);
    border: 1px solid #4a7020;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.result-card {
    background: linear-gradient(135deg, #2d4f10, #3a6215);
    border: 2px solid #5a8a20;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    text-align: center;
}
.warning-box {
    background: #3a2a05;
    border: 1px solid #aa7020;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #f0c060 !important;
}
.chat-user {
    background: #2d4f10;
    border-left: 3px solid #7ab040;
    border-radius: 0 10px 10px 10px;
    padding: 10px 14px;
    margin: 6px 0;
    color: #e8f5b0 !important;
}
.chat-bot {
    background: #243d0d;
    border-left: 3px solid #c8a040;
    border-radius: 0 10px 10px 10px;
    padding: 10px 14px;
    margin: 6px 0;
    color: #e8f5b0 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #3a7a10, #4d9a20) !important;
    color: #e8f5b0 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.25s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4a8a20, #5daa30) !important;
    transform: translateY(-1px) !important;
}
.stSelectbox > div > div {
    background: #243d0d !important;
    border-color: #4a7020 !important;
    color: #e8f5b0 !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #243d0d !important;
}
[data-baseweb="option"] {
    background: #243d0d !important;
    color: #e8f5b0 !important;
}
.stSlider > div { color: #c8e88a !important; }
.stSlider label { color: #c8e88a !important; }
[data-testid="stMetricValue"] {
    color: #7ab040 !important;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] { color: #c8e88a !important; }
.stTabs [data-baseweb="tab-list"] {
    background: #1e3a0a !important;
    border-bottom: 1px solid #4a7020 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #8aaa5a !important;
    font-size: 15px !important;
}
.stTabs [aria-selected="true"] {
    color: #7ab040 !important;
    border-bottom-color: #7ab040 !important;
}
hr { border-color: #4a7020 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1a2e0a; }
::-webkit-scrollbar-thumb { background: #4a7020; border-radius: 3px; }
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #243d0d !important;
    border-color: #4a7020 !important;
    color: #e8f5b0 !important;
}
.stNumberInput > div > div > input {
    background: #243d0d !important;
    border-color: #4a7020 !important;
    color: #e8f5b0 !important;
}
.streamlit-expanderHeader {
    background: #243d0d !important;
    color: #c8e88a !important;
    border-radius: 8px !important;
}
.stCaption { color: #8aaa5a !important; }
.stMarkdown p { color: #e8f5b0 !important; }
label { color: #c8e88a !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prediction_context" not in st.session_state:
    st.session_state.prediction_context = None
if "language" not in st.session_state:
    st.session_state.language = "English"
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None
if "last_state" not in st.session_state:
    st.session_state.last_state = None

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 Fasal Upaj Predictor")
    st.markdown(
        "<div style='color:#8aaa5a;font-size:12px;'>"
        "AI-Powered Crop Yield Intelligence"
        "</div>",
        unsafe_allow_html=True
    )
    st.divider()

    # Language
    st.markdown("### 🗣️ Language / भाषा")
    languages = [
        "English", "Hindi", "Bengali", "Telugu",
        "Marathi", "Tamil", "Urdu", "Gujarati",
        "Kannada", "Odia", "Malayalam", "Punjabi",
        "Assamese", "Maithili", "Santali", "Kashmiri",
        "Nepali", "Sindhi", "Konkani", "Dogri",
        "Manipuri", "Bodo",
    ]
    selected_lang = st.selectbox(
        "Select Language", languages,
        index=languages.index(st.session_state.language),
        label_visibility="collapsed",
    )
    st.session_state.language = selected_lang
    st.divider()

   # Groq API Key — loaded from secrets
    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key:
        st.success("✅ KrishiBot Ready!")
    else:
        st.warning("⚠️ KrishiBot unavailable")
    st.divider()

    # About
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Version:** 1.0.0
        **Developer:** Ankita Choudhary
        **Institute:** IIT Guwahati
        **Stack:** Streamlit, Groq AI,
        scikit-learn, Open-Meteo
        """)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center;font-size:2.5rem;margin-bottom:0;'>
🌾 Fasal Upaj Predictor
</h1>
<p style='text-align:center;color:#8aaa5a;
font-size:14px;letter-spacing:0.1em;'>
AI-POWERED CROP YIELD INTELLIGENCE FOR INDIAN FARMERS
</p>
""", unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────
with st.spinner("🤖 Loading AI Model..."):
    model, le_crop, le_state, le_season, r2, mae = train_model()

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔮 Predict Yield",
    "📊 Data Analysis",
    "💬 KrishiBot",
    "❓ FAQs",
    "📞 Contact Us",
])

# ════════════════════════════════════════
# TAB 1 — PREDICT YIELD
# ════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # LOCATION
        st.markdown(
            "<div class='crop-card'>"
            "<h3 style='color:#7ab040;margin-top:0;"
            "font-size:1rem;letter-spacing:0.08em;'>"
            "📍 LOCATION</h3>",
            unsafe_allow_html=True
        )
        state = st.selectbox("State", STATES)

        # Auto weather fetch
        if st.session_state.last_state != state:
            with st.spinner("🌦️ Fetching weather..."):
                st.session_state.weather_data = get_weather_data(state)
                st.session_state.last_state = state

        districts = get_districts(state)
        district  = st.selectbox("District", districts)
        tehsils   = get_tehsils(state, district)
        tehsil    = st.selectbox("Tehsil", tehsils)
        villages = get_villages(state, district, tehsil)
        village_option = st.selectbox(
            "Village",
            ["Other (Manual Entry)"] + villages,
        )
        if village_option == "Other (Manual Entry)":
            village = st.text_input(
                "Enter Village Name",
                placeholder="e.g. Ajnala Kalan",
            )
        else:
            village = village_option
        st.markdown("</div>", unsafe_allow_html=True)

        # CROP
        st.markdown(
            "<div class='crop-card'>"
            "<h3 style='color:#7ab040;margin-top:0;"
            "font-size:1rem;letter-spacing:0.08em;'>"
            "🌾 CROP DETAILS</h3>",
            unsafe_allow_html=True
        )
        category = st.selectbox("Crop Category", list(CROPS.keys()))
        crop     = st.selectbox("Crop", CROPS[category])
        season   = st.selectbox("Season", SEASONS)

        # Land area
        st.markdown(
            "<p style='color:#c8e88a;font-weight:700;"
            "margin-bottom:8px;'>📏 Land Area</p>",
            unsafe_allow_html=True
        )
        land_units = get_land_units(state)
        ac1, ac2  = st.columns([2, 1])
        with ac1:
            area_value = st.number_input(
                "Area", min_value=0.1,
                max_value=10000.0,
                value=1.0, step=0.5,
            )
        with ac2:
            area_unit = st.selectbox("Unit", land_units)

        area_ha = convert_to_hectare(area_value, area_unit, state)
        st.caption(f"= {area_ha} hectares")
        st.markdown("</div>", unsafe_allow_html=True)

        # Crop Info
        crop_info = get_crop_info(crop)
        if crop_info:
            with st.expander(f"ℹ️ Ideal conditions for {crop}"):
                ci1, ci2, ci3 = st.columns(3)
                with ci1:
                    st.info(f"💧 {crop_info['ideal_rainfall']}")
                with ci2:
                    st.info(f"🌡️ {crop_info['ideal_temp']}")
                with ci3:
                    st.info(f"📅 {crop_info['season']}")

    with col2:
        # WEATHER
        st.markdown(
            "<div class='crop-card'>"
            "<h3 style='color:#7ab040;margin-top:0;"
            "font-size:1rem;letter-spacing:0.08em;'>"
            "🌦️ WEATHER CONDITIONS</h3>",
            unsafe_allow_html=True
        )
        w      = st.session_state.weather_data or {}
        source = w.get("source", "Default values")
        st.caption(f"📡 Source: {source}")

        temperature = st.slider(
            "🌡️ Temperature (°C)",
            min_value=5.0, max_value=50.0,
            value=float(w.get("temperature", 25.0)),
            step=0.5,
        )
        rainfall = st.slider(
            "💧 Rainfall (mm)",
            min_value=0, max_value=3000,
            value=int(w.get("rainfall", 800)),
            step=25,
        )
        humidity = st.slider(
            "💨 Humidity (%)",
            min_value=0, max_value=100,
            value=int(w.get("humidity", 60)),
        )
        soil_ph = st.slider(
            "🧪 Soil pH",
            min_value=3.5, max_value=9.5,
            value=6.5, step=0.1,
        )
        fertilizer = st.slider(
            "🌱 Fertilizer (kg/ha)",
            min_value=0, max_value=400,
            value=150, step=10,
        )
        irrigation = st.slider(
            "💦 Irrigation (%)",
            min_value=0, max_value=100,
            value=50,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # PREDICT BUTTON
        predict_btn = st.button(
            "🔮 Predict Yield",
            use_container_width=True,
        )

        if predict_btn:
            with st.spinner("🤖 Analyzing..."):
                result = predict_yield(
                    model, le_crop, le_state, le_season,
                    crop, state, season,
                    rainfall, temperature, humidity,
                    soil_ph, fertilizer, irrigation,
                    area_value, area_unit,
                )

            if result:
                if result["warning"]:
                    st.markdown(
                        f"<div class='warning-box'>"
                        f"{result['warning']}</div>",
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"<div class='result-card'>"
                    f"<div style='color:#c8e88a;font-size:13px;"
                    f"letter-spacing:0.1em;'>PREDICTED YIELD</div>"
                    f"<div style='font-size:3rem;color:#7ab040;"
                    f"font-family:Playfair Display,serif;"
                    f"font-weight:700;'>"
                    f"{result['yield_per_ha']} ton/ha</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(
                        f"Per {area_unit}",
                        f"{result['yield_per_unit']} ton"
                    )
                with m2:
                    st.metric(
                        f"Total Yield",
                        f"{result['total_yield']} ton"
                    )
                with m3:
                    st.metric("Area", f"{result['area_ha']} ha")

                st.session_state.prediction_context = {
                    "state":      state,
                    "district":   district,
                    "tehsil":     tehsil,
                    "village":    village,
                    "crop":       crop,
                    "season":     season,
                    "area_value": area_value,
                    "area_unit":  area_unit,
                    "yield":      result["yield_per_ha"],
                }
                st.success(
                    "✅ Ask KrishiBot about your crop "
                    "in the 💬 KrishiBot tab!"
                )
            else:
                st.error("Prediction failed. Please try again.")

# ════════════════════════════════════════
# TAB 2 — DATA ANALYSIS
# ════════════════════════════════════════
with tab2:
    st.markdown("### 📊 Crop Yield Analysis — India")
    df = generate_training_data(1000)

    subtab1, subtab2, subtab3 = st.tabs([
        "State-wise", "Crop-wise", "Season-wise"
    ])

    plot_config = dict(
        paper_bgcolor="#243d0d",
        plot_bgcolor="#1e3a0a",
        font=dict(color="#c8e88a"),
        coloraxis_showscale=False,
        height=450,
    )

    with subtab1:
        state_data = df.groupby("State")[
            "Yield_ton_per_ha"
        ].mean().reset_index().sort_values(
            "Yield_ton_per_ha", ascending=False
        )
        fig1 = px.bar(
            state_data,
            x="State", y="Yield_ton_per_ha",
            title="Average Crop Yield by State (ton/ha)",
            color="Yield_ton_per_ha",
            color_continuous_scale=[
                [0, "#2a4a10"], [0.5, "#7ab040"], [1, "#c8e060"]
            ],
        )
        fig1.update_layout(**plot_config, xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)

    with subtab2:
        top_crops = df.groupby("Crop")[
            "Yield_ton_per_ha"
        ].mean().reset_index().sort_values(
            "Yield_ton_per_ha", ascending=False
        ).head(15)
        fig2 = px.bar(
            top_crops,
            x="Yield_ton_per_ha", y="Crop",
            orientation="h",
            title="Top 15 Crops by Average Yield (ton/ha)",
            color="Yield_ton_per_ha",
            color_continuous_scale=[
                [0, "#2a4a10"], [0.5, "#7ab040"], [1, "#c8e060"]
            ],
        )
        fig2.update_layout(**{**plot_config, "height": 500})
        st.plotly_chart(fig2, use_container_width=True)

    with subtab3:
        season_data = df.groupby("Season")[
            "Yield_ton_per_ha"
        ].mean().reset_index()
        fig3 = px.pie(
            season_data,
            values="Yield_ton_per_ha",
            names="Season",
            title="Yield Distribution by Season",
            color_discrete_sequence=[
                "#7ab040", "#4a8a20", "#c8e060", "#2a5010"
            ],
        )
        fig3.update_layout(
            paper_bgcolor="#243d0d",
            font=dict(color="#c8e88a"),
            height=400,
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.markdown("### 🤖 Model Performance")
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric("R² Accuracy", f"{r2:.2%}")
    with mc2:
        st.metric("Mean Error", f"{mae:.2f} ton/ha")
    with mc3:
        st.metric("Total Crops", len(ALL_CROPS))

# ════════════════════════════════════════
# TAB 3 — KRISHIBOT
# ════════════════════════════════════════
with tab3:
    st.markdown("### 💬 KrishiBot — AI Farming Assistant")
    st.markdown(
        "<div style='color:#8aaa5a;font-size:13px;'>"
        "Ask anything about farming in any Indian language!"
        "</div>",
        unsafe_allow_html=True
    )

    if not groq_key:
        st.warning(
            "⚠️ Please add your Groq API key in the sidebar "
            "to use KrishiBot. Get free key at console.groq.com"
        )
    else:
        # Quick questions
        st.markdown(
            "<p style='color:#c8e88a;font-weight:700;'>"
            "⚡ Quick Questions:</p>",
            unsafe_allow_html=True
        )
        categories  = get_categories()
        sel_cat     = st.selectbox(
            "Category", categories,
            label_visibility="collapsed"
        )
        questions = get_questions_by_category(sel_cat)

        for i in range(0, min(6, len(questions)), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(questions):
                    q = questions[i + j]
                    with col:
                        if st.button(
                            q[:45] + "..." if len(q) > 45 else q,
                            key=f"qq_{i}_{j}",
                            use_container_width=True,
                        ):
                            st.session_state.chat_history.append(
                                {"role": "user", "content": q}
                            )
                            with st.spinner("KrishiBot thinking..."):
                                resp = chat_with_krishibot(
                                    q,
                                    st.session_state.chat_history[:-1],
                                    groq_key,
                                    st.session_state.language,
                                    st.session_state.prediction_context,
                                )
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": resp}
                            )
                            st.rerun()

        st.divider()

        # Chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"<div class='chat-user'>"
                    f"🧑‍🌾 <b>You:</b> {msg['content']}"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='chat-bot'>"
                    f"🤖 <b>KrishiBot:</b> {msg['content']}"
                    f"</div>",
                    unsafe_allow_html=True
                )

        # Input form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Message",
                placeholder="e.g. Wheat ke liye kitna paani chahiye?",
                height=80,
                label_visibility="collapsed",
            )
            sc, cc = st.columns([4, 1])
            with sc:
                send = st.form_submit_button(
                    "📤 Send", use_container_width=True
                )
            with cc:
                clear = st.form_submit_button(
                    "🗑️ Clear", use_container_width=True
                )

        if send and user_input.strip():
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input.strip()}
            )
            with st.spinner("🤖 KrishiBot thinking..."):
                resp = chat_with_krishibot(
                    user_input.strip(),
                    st.session_state.chat_history[:-1],
                    groq_key,
                    st.session_state.language,
                    st.session_state.prediction_context,
                )
            st.session_state.chat_history.append(
                {"role": "assistant", "content": resp}
            )
            st.rerun()

        if clear:
            st.session_state.chat_history = []
            st.rerun()

# ════════════════════════════════════════
# TAB 4 — FAQs
# ════════════════════════════════════════
with tab4:
    st.markdown("### ❓ Frequently Asked Questions")
    st.markdown(
        "<div style='color:#8aaa5a;'>28 questions about "
        "the app, farming, and predictions</div>",
        unsafe_allow_html=True
    )
    st.divider()

    search = st.text_input(
        "🔍 Search FAQs...",
        placeholder="Type keyword to search...",
    )

    filtered = [
        faq for faq in FAQS
        if not search or (
            search.lower() in faq["q"].lower() or
            search.lower() in faq["a"].lower()
        )
    ]

    st.caption(
        f"Showing {len(filtered)} of {len(FAQS)} questions"
    )
    st.divider()

    if filtered:
        for i, faq in enumerate(filtered):
            with st.expander(f"Q{i+1}. {faq['q']}"):
                st.markdown(
                    f"<div style='color:#e8f5b0;line-height:1.7;font-size:15px;'>"
                    f"{faq['a']}</div>",
                    unsafe_allow_html=True
                )
    else:
        st.info(
            "No FAQs found. Try different keywords."
        )

# ════════════════════════════════════════
# TAB 5 — CONTACT US
# ════════════════════════════════════════
with tab5:
    st.markdown("### 📞 Contact Us")
    st.divider()

    cont1, cont2 = st.columns([1, 1], gap="large")

    with cont1:
        st.markdown(f"""
        <div class='crop-card'>
        <h3 style='color:#7ab040;margin-top:0;'>
        👩‍💻 Developer</h3>
        <p style='font-size:1.3rem;color:#e8f5b0;
        font-weight:700;'>{CONTACT_INFO['name']}</p>
        <p style='color:#c8e88a;line-height:2;'>
        🎓 {CONTACT_INFO['role']}<br>
        🏛️ {CONTACT_INFO['college']}<br>
        📍 {CONTACT_INFO['location']}
        </p>
        <br>
        <a href='mailto:{CONTACT_INFO["email"]}'
        style='color:#7ab040;text-decoration:none;'>
        📧 {CONTACT_INFO['email']}</a><br><br>
        <a href='{CONTACT_INFO["github"]}'
        target='_blank'
        style='color:#7ab040;text-decoration:none;'>
        🐙 GitHub Profile</a><br><br>
        <a href='{CONTACT_INFO["linkedin"]}'
        target='_blank'
        style='color:#7ab040;text-decoration:none;'>
        💼 LinkedIn Profile</a><br><br>
        <a href='{CONTACT_INFO["project_github"]}'
        target='_blank'
        style='color:#7ab040;text-decoration:none;'>
        ⭐ Project GitHub</a>
        </div>
        """, unsafe_allow_html=True)

    with cont2:
        st.markdown(
            "<div class='crop-card'>"
            "<h3 style='color:#7ab040;margin-top:0;'>"
            "📝 Send Feedback</h3>",
            unsafe_allow_html=True
        )
        fb_name  = st.text_input("Your Name")
        fb_email = st.text_input("Your Email")
        fb_msg   = st.text_area(
            "Your Message",
            placeholder="Share feedback, suggestions, or bugs...",
            height=120,
        )
        if st.button("📤 Send Feedback", use_container_width=True):
            if fb_name and fb_msg:
                st.success(
                    "✅ Thank you for your feedback! "
                    "We will get back to you soon."
                )
            else:
                st.error("Please fill in your name and message.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style='text-align:center;color:#6a8a4a;font-size:12px;'>
    🌾 Fasal Upaj Predictor &nbsp;|&nbsp;
    Built with ❤️ for Indian Farmers &nbsp;|&nbsp;
    IIT Guwahati &nbsp;|&nbsp;
    Data: ICAR, Open-Meteo, LGD
    </div>
    """, unsafe_allow_html=True)