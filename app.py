import streamlit as st
import requests
import re
import os

# =========================
# ENV (CI / PROD SWITCH)
# =========================
ENV = os.getenv("ENV", "prod")

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="Weather Agent",
    page_icon="⛅",
    layout="centered"
)

# =========================
# SECRETS
# =========================
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
DATABRICKS_ENDPOINT = st.secrets["DATABRICKS_ENDPOINT"]

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# STYLES
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: white;
}
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 10px;
}
.stButton > button {
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("⛅ Weather Agent")

# =========================
# UTIL: CITY EXTRACTION
# =========================
def extract_city(text: str):
    match = re.search(r"\bin\s+([A-Za-z\s]+)", text, re.I)
    if match:
        return match.group(1).strip()
    return text.split()[-1] if text else "Hyderabad"

# =========================
# WEATHER API
# =========================
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            return None, "City not found"

        data = r.json()

        return {
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
            "clouds": data.get("clouds", {}).get("all", 0),
            "icon": data["weather"][0]["icon"]
        }, None

    except Exception as e:
        return None, str(e)

# =========================
# LLM (CI + PROD SAFE)
# =========================
def call_llm(query, temp, desc, clouds):

    # CI MODE → NO EXTERNAL CALL
    if ENV == "ci":
        return "☔ Mock response: carry umbrella if needed.", None

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [{
            "role": "user",
            "content": f"{query} | Temp:{temp}°C | {desc} | Clouds:{clouds}%"
        }],
        "max_tokens": 60,
        "temperature": 0.2
    }

    try:
        r = requests.post(DATABRICKS_ENDPOINT, headers=headers, json=payload, timeout=30)

        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], None

        return None, r.text

    except Exception as e:
        return None, str(e)

# =========================
# QUICK ACTIONS
# =========================
st.write("### Quick Prompts")

col1, col2, col3 = st.columns(3)

if col1.button("🏃 Gym Singapore", key="gym"):
    st.session_state.quick = "Gym in Singapore"

if col2.button("☕ Coffee Hyderabad", key="coffee"):
    st.session_state.quick = "Coffee in Hyderabad"

if col3.button("🏖️ Beach Mumbai", key="beach"):
    st.session_state.quick = "Beach in Mumbai"

# =========================
# CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =========================
# INPUT
# =========================
query = st.chat_input(
    st.session_state.get("quick", "Weather in Singapore?")
)

# =========================
# MAIN FLOW
# =========================
if query:

    st.session_state.messages.append({"role": "user", "content": query})

    city = extract_city(query)
    weather, err = get_weather(city)

    with st.chat_message("assistant"):

        if err:
            st.error(err)
        else:
            result, llm_err = call_llm(
                query,
                weather["temp"],
                weather["desc"],
                weather["clouds"]
            )

            if llm_err:
                st.error(llm_err)
            else:
                st.image(f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png")
                st.success(result)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result
                })