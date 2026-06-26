import os
import re
import requests
import streamlit as st
from databricks import sql
from groq import Groq


# ---------------- CONFIG ----------------
ENV = os.getenv("ENV", "prod")

st.set_page_config(
    page_title="Weather Agent",
    page_icon="⛅",
    layout="centered"
)

# ---------------- SECRETS ----------------
def get_secret(name, default=""):
    if ENV == "ci":
        return default
    return st.secrets.get(name, os.getenv(name, default))

OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")
DATABRICKS_TOKEN = get_secret("DATABRICKS_TOKEN")
DATABRICKS_HOST = get_secret("DATABRICKS_HOST")
DATABRICKS_HTTP_PATH = get_secret("DATABRICKS_HTTP_PATH")
GROQ_API_KEY = get_secret("GROQ_API_KEY")

# ---------------- CLIENTS ----------------
client = Groq(api_key=GROQ_API_KEY)

# ---------------- VALIDATION ----------------
def validate():
    missing = [k for k, v in {
        "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
        "DATABRICKS_TOKEN": DATABRICKS_TOKEN,
        "DATABRICKS_HOST": DATABRICKS_HOST,
        "DATABRICKS_HTTP_PATH": DATABRICKS_HTTP_PATH,
        "GROQ_API_KEY": GROQ_API_KEY
    }.items() if not v]

    if missing:
        st.error(f"Missing secrets: {', '.join(missing)}")
        st.stop()

validate()

# ---------------- DB ----------------
def get_db_connection():
    return sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )

# ---------------- AI ROUTER ----------------
def route_intent(user_query):
    prompt = f"""
Classify user message into WEATHER, ADVICE, CHAT.

Message: {user_query}

Return only one word.
"""

    res = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

    return res.choices[0].message.content.strip().upper()

# ---------------- WEATHER ----------------
def weather(city):
    r = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
    )
    d = r.json()

    if r.status_code != 200 or "main" not in d:
        return None, d.get("message", "error")

    return {
        "temp": d["main"]["temp"],
        "desc": d["weather"][0]["description"],
        "icon": d["weather"][0]["icon"],
    }, None

# ---------------- AI RESPONSE ----------------
def get_ai_advice(city, temp, desc, user_query):
    prompt = f"""
User: {user_query}
City: {city}
Temp: {temp}
Condition: {desc}

Give short helpful answer.
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content

# ---------------- DB LOG ----------------
def log_weather(user_query, city, weather_data, ai_text):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"""
    INSERT INTO weather_logs
    (ts, user_query, city, temp, description, ai_suggestion)
    VALUES
    (
        current_timestamp(),
        '{user_query.replace("'", "''")}',
        '{city.replace("'", "''")}',
        {weather_data["temp"]},
        '{weather_data["desc"].replace("'", "''")}',
        '{ai_text.replace("'", "''")}'
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp{
    background-color:#0f172a;
    color:white;
}

section[data-testid="stSidebar"]{
    background-color:#111827;
}

a{
    color:#38bdf8 !important;
    text-decoration:none;
}

a:hover{
    text-decoration:underline;
}
</style>
""", unsafe_allow_html=True)

st.title("⛅ Weather Agent (AI Router)")

with st.sidebar:

    st.image(
        "https://github.com/vijjikodali.png",
        width=120
    )

    st.markdown("## 🌦️ Weather AI Agent")
    st.markdown("---")

    st.markdown(
        "[🐙 GitHub Repository](https://github.com/vijjikodali/weather-agent-llama)"
    )

    st.markdown(
        "[📂 GitHub Profile](https://github.com/vijjikodali?tab=repositories)"
    )

    st.markdown(
        "[💼 LinkedIn](https://www.linkedin.com/in/kodali-vijayalaxmi-40860222)"
    )

    st.markdown("---")

    st.caption("Developed by")
    st.markdown(
        "**Kodali Vijayalaxmi**"
    )
# ---------------- SYSTEM CHECK ----------------
def system_check():
    st.info("Checking systems...")

    # OpenWeather check
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": "Singapore",
                "appid": OPENWEATHER_API_KEY,
            },
            timeout=5,
        )

        st.write("Weather Status Code:", r.status_code)

        if r.status_code == 200:
            st.success("✅ OpenWeather API OK")
        else:
            st.error(f"❌ OpenWeather Error: {r.text}")

    except Exception as e:
        st.error(f"❌ OpenWeather Exception: {e}")

    # Databricks check
          # Databricks check
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                current_timestamp(),
                current_catalog(),
                current_schema()
        """)

        result = cur.fetchone()

        st.success("✅ Databricks Connected")
        st.write(f"🕒 Time: {result[0]}")
        st.write(f"📦 Catalog: {result[1]}")
        st.write(f"🗂️ Schema: {result[2]}")

        cur.close()
        conn.close()

    except Exception as e:
        st.error(f"❌ Databricks Error: {e}")

# ---------------- SIDEBAR BUTTON ----------------
with st.sidebar:
    if st.button("🔍 System Check"):
        system_check()
# ---------------- CHAT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

q = st.chat_input("Ask something...")

if q:
    st.session_state.messages.append(
        {"role": "user", "content": q}
    )

    intent = route_intent(q)

    with st.chat_message("assistant"):

        if intent == "WEATHER":

            city = q.split()[-1]
            w, err = weather(city)

            if err:
                ai = get_ai_advice("unknown", 0, err, q)
                st.info(ai)

            else:
                st.image(
                    f"https://openweathermap.org/img/wn/{w['icon']}@2x.png"
                )

                st.success(
                    f"{city}: {w['temp']}°C, {w['desc']}"
                )

                ai = get_ai_advice(
                    city,
                    w["temp"],
                    w["desc"],
                    q
                )

                st.info(ai)

                try:
                    log_weather(q, city, w, ai)
                except Exception as e:
                    st.warning(
                        f"Databricks Log Failed: {e}"
                    )

        else:

            ai = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": q
                    }
                ]
            ).choices[0].message.content

            st.write(ai)
            st.markdown("---")
st.caption(
    "🚀 Developed by Kodali Vijayalaxmi | Weather AI Agent using Streamlit + OpenWeather + Groq + Databricks"
)
