import streamlit as st
from datetime import datetime

# ----------------------------
# FamilyHub AI - Minimal Prototype
# ----------------------------

st.set_page_config(page_title="FamilyHub AI", layout="wide")

# Session state initialization
if "chat" not in st.session_state:
    st.session_state.chat = []

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

if "energy_usage" not in st.session_state:
    st.session_state.energy_usage = [5, 6, 4, 7, 8]

# ----------------------------
# AI Assistant (Simple Rule-Based)
# ----------------------------

def ai_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello! I am FamilyHub AI. How can I help your family today?"

    elif "homework" in user_input:
        return "Tip: Break homework into small tasks and take short breaks every 25 minutes."

    elif "stress" in user_input:
        return "It seems like stress is high. Suggestion: Take a family walk or short break together."

    elif "energy" in user_input:
        return "Energy usage can be optimized by turning off unused appliances and using daylight."

    elif "grocery" in user_input:
        return "You can add items in the Grocery Planner section. I can help you organize them."

    else:
        return "I am still learning. Try asking about homework, stress, energy, or groceries."

# ----------------------------
# Sidebar Navigation
# ----------------------------

menu = st.sidebar.selectbox(
    "Select Module",
    ["AI Assistant", "Safety", "Grocery Planner", "Energy Monitor", "Mood Tracker"]
)

# ----------------------------
# AI Assistant Module
# ----------------------------

if menu == "AI Assistant":
    st.title("🧠 FamilyHub AI Assistant")

    user_input = st.text_input("Ask me something for your family:")

    if user_input:
        response = ai_response(user_input)
        st.session_state.chat.append((user_input, response))

    for q, r in reversed(st.session_state.chat):
        st.write(f"You: {q}")
        st.write(f"AI: {r}")
        st.write("---")

# ----------------------------
# Safety Module
# ----------------------------

elif menu == "Safety":
    st.title("🚨 Family Safety Center")

    if st.button("Trigger Emergency Alert"):
        st.error("Emergency Alert Sent to Family Members!")

    st.info("This module simulates emergency alert system.")

# ----------------------------
# Grocery Planner
# ----------------------------

elif menu == "Grocery Planner":
    st.title("🛒 Smart Grocery Planner")

    item = st.text_input("Add grocery item:")

    if st.button("Add Item") and item:
        st.session_state.grocery_list.append(item)

    st.subheader("Your Grocery List")
    for i, g in enumerate(st.session_state.grocery_list, 1):
        st.write(f"{i}. {g}")

# ----------------------------
# Energy Monitor
# ----------------------------

elif menu == "Energy Monitor":
    st.title("⚡ Energy Usage Monitor")

    st.line_chart(st.session_state.energy_usage)

    st.write("Tip: Reduce usage during peak hours for savings.")

# ----------------------------
# Mood Tracker
# ----------------------------

elif menu == "Mood Tracker":
    st.title("😊 Family Mood Tracker")

    mood = st.selectbox("Select today’s mood", ["Happy", "Neutral", "Stressed", "Sad"])

    if st.button("Log Mood"):
        st.session_state.mood_log.append((datetime.now().strftime("%Y-%m-%d %H:%M"), mood))

    st.subheader("Mood History")
    for time, m in reversed(st.session_state.mood_log):
        st.write(f"{time} - {m}")