import os
import re
import requests
import streamlit as st

ENV = os.getenv("ENV", "prod")

st.set_page_config(page_title="Weather Agent", page_icon="⛅", layout="centered")


def get_secret(name, default=""):
    if ENV == "ci":
        return default
    return st.secrets.get(name, os.getenv(name, default))


OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")
DATABRICKS_TOKEN = get_secret("DATABRICKS_TOKEN")
DATABRICKS_ENDPOINT = get_secret("DATABRICKS_ENDPOINT")


def validate():
    if ENV == "ci":
        return
    missing = [
        k for k, v in {
            "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
            "DATABRICKS_TOKEN": DATABRICKS_TOKEN,
            "DATABRICKS_ENDPOINT": DATABRICKS_ENDPOINT
        }.items() if not v
    ]
    if missing:
        st.error(f"Missing: {', '.join(missing)}")
        st.stop()


validate()

if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("""
<style>
.stApp {background: linear-gradient(to bottom right, #0f172a, #1e293b); color: white;}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image("https://github.com/vijjikodali.png", width=120)
    st.markdown("### vijjikodali")
    st.success("Databricks AI")
    st.success("OpenWeather")
    st.markdown("[Repo](https://github.com/vijjikodali/weather-agent-llama)")


st.title("⛅ Weather Agent")


def city_extract(text):
    text = re.sub(r"[?.!,]", "", text or "")
    m = re.search(r"\bin\s+([A-Za-z\s]+)", text, re.I)
    return m.group(1).strip() if m else (text.split()[-1] if text else "Singapore")


def weather(city):
    if ENV == "ci":
        return {"temp": 28, "desc": "mock", "icon": "02d"}, None

    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=10
        )
        if r.status_code != 200:
            return None, "Weather error"

        d = r.json()
        return {
            "temp": d["main"]["temp"],
            "desc": d["weather"][0]["description"],
            "icon": d["weather"][0]["icon"]
        }, None

    except Exception as e:
        return None, str(e)


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])


q = st.chat_input("Ask weather...")

if q:
    st.session_state.messages.append({"role": "user", "content": q})

    with st.chat_message("user"):
        st.write(q)

    with st.chat_message("assistant"):
        city = city_extract(q)
        w, err = weather(city)

        if err:
            st.error(err)
        else:
            st.image(f"https://openweathermap.org/img/wn/{w['icon']}@2x.png")
            msg = f"{city}: {w['temp']}°C, {w['desc']}"
            st.success(msg)

            st.session_state.messages.append({"role": "assistant", "content": msg})


st.markdown("---")
st.markdown("Built by vijjikodali 🚀")