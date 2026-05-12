import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from difflib import get_close_matches

# ============================
# FamilyHub AI - Winner Version + Login System
# ============================

st.set_page_config(page_title="FamilyHub AI", layout="wide")

# ----------------------------
# SIMPLE FAMILY LOGIN SYSTEM
# ----------------------------

USERS = {
    "parent": "1234",
    "child1": "1111",
    "child2": "2222",
    "admin": "admin"
}

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = None


def login_page():
    st.title("🔐 FamilyHub AI Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.auth = True
            st.session_state.user = username
            st.success(f"Welcome {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ----------------------------
# BLOCK APP IF NOT LOGGED IN
# ----------------------------

if not st.session_state.auth:
    login_page()
    st.stop()

# ----------------------------
# SESSION STATE INIT
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
# SMART AI ENGINE
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
# DASHBOARD CALCULATIONS
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
        return int(data[-1])

    coeff = np.polyfit(x, data, 1)
    return int(coeff[0] * (len(data) + 1) + coeff[1])

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------

menu = st.sidebar.radio(
    f"Logged in as: {st.session_state.user}",
    ["🏠 Dashboard", "🧠 AI Assistant", "🚨 Safety", "🛒 Grocery", "⚡ Energy", "😊 Mood", "📄 Weekly Report"]
)

# ----------------------------
# DASHBOARD
# ----------------------------

if menu == "🏠 Dashboard":
    st.title("🏠 Family Intelligence Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Mood Score", f"{mood_score()} / 100")

    with col2:
        st.metric("Energy Forecast", energy_forecast())

    with col3:
        st.metric("Grocery Items", len(st.session_state.grocery_list))

    st.line_chart(st.session_state.energy_usage)

# ----------------------------
# AI ASSISTANT
# ----------------------------

elif menu == "🧠 AI Assistant":
    st.title("🧠 AI Assistant")

    user_input = st.text_input("Ask something")

    if user_input:
        response = smart_ai_response(user_input)
        st.session_state.chat.append((user_input, response))

    for q, r in reversed(st.session_state.chat[-10:]):
        st.write(f"You: {q}")
        st.write(f"AI: {r}")
        st.write("---")

# ----------------------------
# SAFETY
# ----------------------------

elif menu == "🚨 Safety":
    st.title("🚨 Safety System")

    if mood_score() < 40:
        st.error("Emotional risk detected")

    if energy_forecast() > np.mean(st.session_state.energy_usage) + 2:
        st.warning("High energy usage predicted")

    if st.button("Emergency Alert"):
        st.error("Alert sent to family members")

# ----------------------------
# GROCERY
# ----------------------------

elif menu == "🛒 Grocery":
    st.title("🛒 Grocery Planner")

    item = st.text_input("Add item")

    if st.button("Add") and item:
        st.session_state.grocery_list.append(item)

    for i, g in enumerate(st.session_state.grocery_list, 1):
        st.write(f"{i}. {g}")

# ----------------------------
# ENERGY
# ----------------------------

elif menu == "⚡ Energy":
    st.title("⚡ Energy Monitor")

    st.line_chart(st.session_state.energy_usage)
    st.write("Forecast:", energy_forecast())

# ----------------------------
# MOOD
# ----------------------------

elif menu == "😊 Mood":
    st.title("😊 Mood Tracker")

    mood = st.selectbox("Mood", ["Happy", "Neutral", "Stressed", "Sad"])

    if st.button("Log"):
        st.session_state.mood_log.append((datetime.now().strftime("%Y-%m-%d %H:%M"), mood))

    st.dataframe(pd.DataFrame(st.session_state.mood_log, columns=["Time", "Mood"]))

# ----------------------------
# WEEKLY REPORT
# ----------------------------

elif menu == "📄 Weekly Report":
    st.title("📄 Weekly AI Report")

    if st.button("Generate"):
        report = f"""
Family Report
----------------
Mood Score: {mood_score()}
Energy Forecast: {energy_forecast()}
Grocery Items: {len(st.session_state.grocery_list)}

Insights:
- Mood status: {'Good' if mood_score()>60 else 'Needs attention'}
- Energy trend: {'Rising' if energy_forecast()>6 else 'Stable'}

Suggestions:
- Improve family interaction
- Optimize energy usage
- Plan groceries efficiently
"""
        st.text_area("Report", report, height=300)
