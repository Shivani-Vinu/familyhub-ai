import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from difflib import get_close_matches
from sklearn.linear_model import LinearRegression, LogisticRegression

# ============================
# FamilyHub AI - ML Enhanced Version
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
# ML MODELS (TRAINED ON SESSION DATA)
# ----------------------------

def train_energy_model():
    data = np.array(st.session_state.energy_usage)
    X = np.arange(len(data)).reshape(-1, 1)
    y = data

    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_energy(model):
    next_x = np.array([[len(st.session_state.energy_usage)]])
    return float(model.predict(next_x)[0])


def train_mood_model():
    if not st.session_state.mood_log:
        return None

    mapping = {"Happy": 3, "Neutral": 2, "Stressed": 1, "Sad": 0}

    X = np.array([[i] for i in range(len(st.session_state.mood_log))])
    y = np.array([mapping[m[1]] for m in st.session_state.mood_log])

    model = LogisticRegression()
    model.fit(X, y)
    return model

# ----------------------------
# AI ENGINE
# ----------------------------

knowledge_base = {
    "homework": "Break tasks into small steps and study in focused sessions.",
    "stress": "Take breaks and talk with family.",
    "energy": "Turn off unused appliances.",
    "grocery": "Use planner to optimize shopping.",
    "family": "Communication improves wellbeing."
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

    return "AI is learning. Try asking about stress, energy, or homework."

# ----------------------------
# DASHBOARD METRICS
# ----------------------------

def mood_score():
    if not st.session_state.mood_log:
        return 50

    mapping = {"Happy": 80, "Neutral": 50, "Stressed": 30, "Sad": 20}
    scores = [mapping[m[1]] for m in st.session_state.mood_log]
    return int(np.mean(scores))

energy_model = train_energy_model()
energy_prediction = predict_energy(energy_model)

mood_model = train_mood_model()

# ----------------------------
# NAVIGATION
# ----------------------------

menu = st.sidebar.radio(
    f"Logged in as: {st.session_state.user}",
    ["🏠 Dashboard", "🧠 AI Assistant", "🚨 Safety", "🛒 Grocery", "⚡ Energy", "😊 Mood", "📄 Weekly Report"]
)

# ----------------------------
# DASHBOARD
# ----------------------------

if menu == "🏠 Dashboard":
    st.title("🏠 AI Family Intelligence Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Mood Score", f"{mood_score()} / 100")

    with col2:
        st.metric("ML Energy Forecast", round(energy_prediction, 2))

    with col3:
        st.metric("Grocery Items", len(st.session_state.grocery_list))

    st.line_chart(st.session_state.energy_usage)

# ----------------------------
# AI ASSISTANT
# ----------------------------

elif menu == "🧠 AI Assistant":
    st.title("🧠 ML-Powered AI Assistant")

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
    st.title("🚨 Smart Safety System")

    if mood_score() < 40:
        st.error("Emotional risk detected")

    if energy_prediction > np.mean(st.session_state.energy_usage) + 2:
        st.warning("High energy usage predicted (ML model)")

    if st.button("Emergency Alert"):
        st.error("Alert sent to family members")

# ----------------------------
# GROCERY
# ----------------------------

elif menu == "🛒 Grocery":
    st.title("🛒 Smart Grocery Planner")

    item = st.text_input("Add item")

    if st.button("Add") and item:
        st.session_state.grocery_list.append(item)

    for i, g in enumerate(st.session_state.grocery_list, 1):
        st.write(f"{i}. {g}")

# ----------------------------
# ENERGY
# ----------------------------

elif menu == "⚡ Energy":
    st.title("⚡ ML Energy Forecast System")

    st.line_chart(st.session_state.energy_usage)
    st.success(f"Predicted next usage (ML): {round(energy_prediction,2)}")

# ----------------------------
# MOOD
# ----------------------------

elif menu == "😊 Mood":
    st.title("😊 Family Mood Tracker")

    mood = st.selectbox("Mood", ["Happy", "Neutral", "Stressed", "Sad"])

    if st.button("Log"):
        st.session_state.mood_log.append((datetime.now().strftime("%Y-%m-%d %H:%M"), mood))

    st.dataframe(pd.DataFrame(st.session_state.mood_log, columns=["Time", "Mood"]))

# ----------------------------
# WEEKLY REPORT
# ----------------------------

elif menu == "📄 Weekly Report":
    st.title("📄 AI Weekly Intelligence Report")

    if st.button("Generate"):
        report = f"""
FAMILY AI REPORT
-------------------
Mood Score: {mood_score()}
ML Energy Forecast: {round(energy_prediction,2)}
Grocery Items: {len(st.session_state.grocery_list)}

Insights:
- Mood: {'Healthy' if mood_score()>60 else 'Needs attention'}
- Energy: {'Rising trend' if energy_prediction>6 else 'Stable'}

AI Suggestions:
- Improve family bonding time
- Optimize electricity usage
- Maintain balanced routine
"""
        st.text_area("Report", report, height=300)
