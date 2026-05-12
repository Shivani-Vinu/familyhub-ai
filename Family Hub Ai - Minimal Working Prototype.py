import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from difflib import get_close_matches

# ============================
# FamilyHub AI - Winner Version (Hackathon Upgrade)
# ============================

st.set_page_config(page_title="FamilyHub AI", layout="wide")

# ----------------------------
# Session State Init
# ----------------------------

if "chat" not in st.session_state:
    st.session_state.chat = []

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

if "energy_usage" not in st.session_state:
    st.session_state.energy_usage = [5, 6, 4, 7, 8, 6, 9]

# ----------------------------
# Smart AI Engine (Light NLP)
# ----------------------------

knowledge_base = {
    "homework": "Break tasks into small steps and study in focused 25-minute sessions.",
    "stress": "Take a short break, talk with family, or do a relaxing activity together.",
    "energy": "Turn off unused appliances and use natural light during daytime.",
    "grocery": "Use the grocery planner to track and optimize family needs.",
    "family": "Strong communication improves family wellbeing and happiness."
}

def smart_ai_response(query):
    query = query.lower()
    keys = list(knowledge_base.keys())

    match = get_close_matches(query, keys, n=1, cutoff=0.3)

    if match:
        return knowledge_base[match[0]]

    for k in keys:
        if k in query:
            return knowledge_base[k]

    return "I analyzed your input. Try asking about stress, homework, energy, or groceries."

# ----------------------------
# Dashboard Calculations
# ----------------------------

def mood_score():
    if not st.session_state.mood_log:
        return 50

    mapping = {"Happy": 80, "Neutral": 50, "Stressed": 30, "Sad": 20}
    scores = [mapping[m[1]] for m in st.session_state.mood_log]
    return int(np.mean(scores))

def energy_forecast():
    data = np.array(st.session_state.energy_usage)
    x = np.arange(len(data))

    if len(data) < 2:
        return data[-1]

    coeff = np.polyfit(x, data, 1)
    return int(coeff[0] * (len(data) + 1) + coeff[1])

# ----------------------------
# Sidebar Navigation
# ----------------------------

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🧠 AI Assistant", "🚨 Safety", "🛒 Grocery", "⚡ Energy", "😊 Mood", "📄 Weekly Report"]
)

# ----------------------------
# DASHBOARD (NEW)
# ----------------------------

if menu == "🏠 Dashboard":
    st.title("🏠 FamilyHub AI - Intelligence Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Family Mood Score", f"{mood_score()} / 100")

    with col2:
        st.metric("Next Energy Forecast", energy_forecast())

    with col3:
        st.metric("Grocery Items", len(st.session_state.grocery_list))

    st.subheader("⚡ Energy Trend")
    st.line_chart(st.session_state.energy_usage)

# ----------------------------
# AI ASSISTANT (UPGRADED)
# ----------------------------

elif menu == "🧠 AI Assistant":
    st.title("🧠 Intelligent Family AI Assistant")

    user_input = st.text_input("Ask something:")

    if user_input:
        response = smart_ai_response(user_input)
        st.session_state.chat.append((user_input, response))

    for q, r in reversed(st.session_state.chat[-10:]):
        st.write(f"🧑 You: {q}")
        st.write(f"🤖 AI: {r}")
        st.write("---")

# ----------------------------
# SAFETY MODULE (UPGRADED)
# ----------------------------

elif menu == "🚨 Safety":
    st.title("🚨 Smart Safety Monitoring")

    if mood_score() < 40:
        st.error("⚠ Emotional risk detected in family mood pattern")

    if energy_forecast() > np.mean(st.session_state.energy_usage) + 2:
        st.warning("⚡ High energy usage predicted")

    if st.button("Trigger Emergency Alert"):
        st.error("🚨 Emergency Alert Sent to Family Members")

# ----------------------------
# GROCERY (SMART)
# ----------------------------

elif menu == "🛒 Grocery":
    st.title("🛒 Smart Grocery Intelligence")

    item = st.text_input("Add item")

    if st.button("Add") and item:
        st.session_state.grocery_list.append(item)

    st.subheader("Current List")
    for i, g in enumerate(st.session_state.grocery_list, 1):
        st.write(f"{i}. {g}")

    if len(st.session_state.grocery_list) > 5:
        st.info("📦 Suggestion: Consider bulk buying for savings")

# ----------------------------
# ENERGY
# ----------------------------

elif menu == "⚡ Energy":
    st.title("⚡ Energy Intelligence System")

    st.line_chart(st.session_state.energy_usage)

    st.write("Forecasted next value:", energy_forecast())

    if energy_forecast() > 7:
        st.warning("High usage predicted")

# ----------------------------
# MOOD TRACKER
# ----------------------------

elif menu == "😊 Mood":
    st.title("😊 Family Mood Intelligence")

    mood = st.selectbox("Mood", ["Happy", "Neutral", "Stressed", "Sad"])

    if st.button("Log"):
        st.session_state.mood_log.append((datetime.now().strftime("%Y-%m-%d %H:%M"), mood))

    df = pd.DataFrame(st.session_state.mood_log, columns=["Time", "Mood"])
    st.dataframe(df)

# ----------------------------
# WEEKLY REPORT (NEW BIG FEATURE)
# ----------------------------

elif menu == "📄 Weekly Report":
    st.title("📄 AI Family Weekly Report")

    if st.button("Generate Report"):
        report = f"""
        🏠 FAMILY REPORT
        ----------------------
        Mood Score: {mood_score()}/100
        Energy Forecast: {energy_forecast()}
        Grocery Items: {len(st.session_state.grocery_list)}

        Insights:
        - Mood is {'healthy' if mood_score()>60 else 'needs attention'}
        - Energy usage trend is {'rising' if energy_forecast()>6 else 'stable'}

        Suggestions:
        - Spend more family time together
        - Optimize energy usage
        - Plan grocery shopping efficiently
        """

        st.text_area("Report", report, height=300)
