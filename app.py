import os
import re
import requests
import streamlit as st
from databricks import sql

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

# ---------------- VALIDATION ----------------
def validate():
    missing = [
        k for k, v in {
            "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
            "DATABRICKS_TOKEN": DATABRICKS_TOKEN,
            "DATABRICKS_HOST": DATABRICKS_HOST,
            "DATABRICKS_HTTP_PATH": DATABRICKS_HTTP_PATH,
        }.items()
        if not v
    ]

    if missing:
        st.error(f"Missing secrets: {', '.join(missing)}")
        st.stop()

validate()

# ---------------- DATABRICKS CONNECTION ----------------
def get_db_connection():
    return sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- UI ----------------
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("https://github.com/vijjikodali.png", width=120)
    st.markdown("### Weather AI Agent")
    st.success("OpenWeather API")
    st.success("Databricks SQL + AI")
    st.markdown("[Repo](https://github.com/vijjikodali/weather-agent-llama)")

# ---------------- CITY EXTRACTION ----------------
def city_extract(text):
    text = re.sub(r"[?.!,]", "", text or "")
    m = re.search(r"\bin\s+([A-Za-z\s]+)", text, re.I)

    if m:
        return m.group(1).strip()

    words = text.split()
    return words[-1] if words else "Singapore"

# ---------------- WEATHER ----------------
def weather(city):
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        if r.status_code != 200:
            return None, f"Weather error: {r.text}"

        d = r.json()

        return {
            "temp": d["main"]["temp"],
            "desc": d["weather"][0]["description"],
            "icon": d["weather"][0]["icon"],
        }, None

    except Exception as e:
        return None, str(e)

# ---------------- DATABRICKS LOG ----------------
def log_weather(user_query, city, weather_data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        temp = float(weather_data["temp"])
        desc = weather_data["desc"]

        rain = 80.0 if "rain" in desc.lower() else 0.0
        ai = "Carry umbrella" if rain > 50 else "Good weather"

        cur.execute(f"""
        INSERT INTO weather_logs
        (
            ts,
            user_query,
            city,
            temp,
            description,
            rain_percent,
            ai_suggestion
        )
        VALUES
        (
            current_timestamp(),
            '{user_query.replace("'", "''")}',
            '{city.replace("'", "''")}',
            {temp},
            '{desc.replace("'", "''")}',
            {rain},
            '{ai}'
        )
        """)

        cur.close()
        conn.close()

        st.success("✅ Logged to Databricks")

    except Exception as e:
        st.error(f"❌ Databricks insert failed: {e}")
        print(e)

# ---------------- SYSTEM CHECK ----------------
def system_check():
    st.info("Checking systems...")

    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": "Singapore",
                "appid": OPENWEATHER_API_KEY,
            },
            timeout=5,
        )
        weather_ok = r.status_code == 200
    except Exception:
        weather_ok = False

   try:
    st.write("HOST loaded:", bool(DATABRICKS_HOST))
    st.write("HTTP PATH loaded:", bool(DATABRICKS_HTTP_PATH))
    st.write("TOKEN loaded:", bool(DATABRICKS_TOKEN))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1")
    result = cur.fetchone()

    st.success(f"Databricks OK: {result}")

    cur.close()
    conn.close()

    db_ok = True

except Exception as e:
    st.error(f"DATABRICKS ERROR: {type(e).__name__}: {e}")
    db_ok = False
# ---------------- SIDEBAR BUTTON ----------------
with st.sidebar:
    if st.button("🔍 System Check"):
        system_check()

# ---------------- CHAT UI ----------------
st.title("⛅ Weather Agent (Live AI)")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

q = st.chat_input("Ask weather...")

if q:
    st.session_state.messages.append(
        {"role": "user", "content": q}
    )

    with st.chat_message("user"):
        st.write(q)

    city = city_extract(q)
    w, err = weather(city)

    with st.chat_message("assistant"):

        if err or not w:
            st.error(err or "Weather failed")

        else:
            st.image(
                f"https://openweathermap.org/img/wn/{w['icon']}@2x.png"
            )

            msg = f"{city}: {w['temp']}°C, {w['desc']}"

            st.success(msg)

            log_weather(q, city, w)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": msg,
                }
            )

# ---------------- VIEW LATEST LOGS ----------------
st.markdown("---")
st.subheader("Latest Databricks Records")

try:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ts, city, temp, description
        FROM weather_logs
        ORDER BY ts DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    if rows:
        st.dataframe(rows)

    cur.close()
    conn.close()

except Exception as e:
    st.warning(f"Unable to load logs: {e}")

st.markdown("---")
st.markdown("Built by vijjikodali 🚀")
