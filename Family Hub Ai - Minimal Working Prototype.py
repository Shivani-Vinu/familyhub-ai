import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from difflib import get_close_matches
from sklearn.linear_model import LinearRegression, LogisticRegression

# ============================
# FamilyHub AI - Figma Style UI + ML Version
# ============================

st.set_page_config(page_title="Kindred", layout="wide")

# ----------------------------
# MODERN UI (FIGMA-STYLE CSS)
# ----------------------------

st.markdown("""
<style>

/* Background */
.main {
    background-color: #0f172a;
    color: white;
}

/* Card style */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
    margin-bottom: 15px;
}

/* Metric box */
.metric-box {
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    padding: 20px;
    border-radius: 16px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

/* Title */
h1, h2, h3 {
    color: white;
    font-family: 'Arial';
}

/* Sidebar */
.css-1d391kg {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOGIN SYSTEM
# ----------------------------

USERS = {"Shivani Mohan":"1234","child1":"1111","child2":"2222","admin":"admin"}

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = None


def login_page():
    st.title("🔐 FamilyHub AI")
    st.subheader("Secure Family Login")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Username")
    with col2:
        password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.auth = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.auth:
    login_page()
    st.stop()

# ----------------------------
# SESSION STATE
# ----------------------------

if "chat" not in st.session_state:
    st.session_state.chat = []

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

if "energy_usage" not in st.session_state:
    st.session_state.energy_usage = [5,6,4,7,8,6,9]

# ----------------------------
# ML MODELS
# ----------------------------

def energy_model():
    X = np.arange(len(st.session_state.energy_usage)).reshape(-1,1)
    y = np.array(st.session_state.energy_usage)
    model = LinearRegression()
    model.fit(X,y)
    return model

def energy_predict():
    model = energy_model()
    pred = model.predict([[len(st.session_state.energy_usage)]])
    return float(pred[0])

# ----------------------------
# AI ENGINE
# ----------------------------

kb = {
    "homework":"Break tasks into small steps.",
    "stress":"Take breaks and relax.",
    "energy":"Turn off unused devices.",
    "family":"Communication improves bonding.",
}

def ai(q):
    q=q.lower()
    match=get_close_matches(q,list(kb.keys()),n=1,cutoff=0.3)
    if match:
        return kb[match[0]]
    for k in kb:
        if k in q:
            return kb[k]
    return "AI is learning..."

# ----------------------------
# METRICS
# ----------------------------

def mood_score():
    if not st.session_state.mood_log:
        return 50
    mapv={"Happy":80,"Neutral":50,"Stressed":30,"Sad":20}
    return int(np.mean([mapv[m[1]] for m in st.session_state.mood_log]))

# ----------------------------
# SIDEBAR
# ----------------------------

menu=st.sidebar.radio("Navigation",
["🏠 Dashboard","🧠 AI","🚨 Safety","🛒 Grocery","⚡ Energy","😊 Mood","📄 Report"])

# ----------------------------
# DASHBOARD (FIGMA STYLE)
# ----------------------------

if menu=="🏠 Dashboard":
    st.title("🏠 Family Intelligence Dashboard")

    col1,col2,col3=st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='metric-box'>
        <h3>Mood Score</h3>
        <h1>{mood_score()}</h1>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-box'>
        <h3>Energy Forecast</h3>
        <h1>{round(energy_predict(),2)}</h1>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-box'>
        <h3>Grocery Items</h3>
        <h1>{len(st.session_state.grocery_list)}</h1>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.subheader("Energy Trend")
    st.line_chart(st.session_state.energy_usage)
    st.markdown("</div>",unsafe_allow_html=True)

# ----------------------------
# AI
# ----------------------------

elif menu=="🧠 AI":
    st.title("🧠 Smart AI Assistant")

    q=st.text_input("Ask")

    if q:
        st.session_state.chat.append((q,ai(q)))

    for a,b in reversed(st.session_state.chat[-8:]):
        st.markdown(f"<div class='card'><b>You:</b> {a}<br><b>AI:</b> {b}</div>",unsafe_allow_html=True)

# ----------------------------
# SAFETY
# ----------------------------

elif menu=="🚨 Safety":
    st.title("🚨 Safety Center")

    if mood_score()<40:
        st.error("Emotional risk detected")

    if energy_predict()>np.mean(st.session_state.energy_usage)+2:
        st.warning("High energy usage predicted")

    if st.button("Emergency Alert"):
        st.error("Alert sent")

# ----------------------------
# GROCERY
# ----------------------------

elif menu=="🛒 Grocery":
    st.title("🛒 Smart Grocery")

    item=st.text_input("Item")

    if st.button("Add") and item:
        st.session_state.grocery_list.append(item)

    for i,g in enumerate(st.session_state.grocery_list,1):
        st.write(i,g)

# ----------------------------
# ENERGY
# ----------------------------

elif menu=="⚡ Energy":
    st.title("⚡ Energy AI")

    st.line_chart(st.session_state.energy_usage)
    st.success(f"Prediction: {round(energy_predict(),2)}")

# ----------------------------
# MOOD
# ----------------------------

elif menu=="😊 Mood":
    st.title("😊 Mood Tracker")

    m=st.selectbox("Mood",["Happy","Neutral","Stressed","Sad"])

    if st.button("Log"):
        st.session_state.mood_log.append((datetime.now().strftime("%H:%M"),m))

    st.dataframe(pd.DataFrame(st.session_state.mood_log,columns=["Time","Mood"]))

# ----------------------------
# REPORT
# ----------------------------

elif menu=="📄 Report":
    st.title("📄 Weekly AI Report")

    if st.button("Generate"):
        st.text_area("Report",
        f"Mood:{mood_score()}\nEnergy:{round(energy_predict(),2)}\nItems:{len(st.session_state.grocery_list)}",
        height=250)
