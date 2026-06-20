import os
import re
import requests
import streamlit as st


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
# CONFIG / SECRETS
# =========================
def get_secret(name: str, default: str = "") -> str:
    if ENV == "ci":
        return default
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)


OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")
DATABRICKS_TOKEN = get_secret("DATABRICKS_TOKEN")
DATABRICKS_ENDPOINT = get_secret("DATABRICKS_ENDPOINT")


# =========================
# VALIDATION
# =========================
def validate_config():
    if ENV == "ci":
        return

    missing = []

    if not OPENWEATHER_API_KEY:
        missing.append("OPENWEATHER_API_KEY")

    if not DATABRICKS_TOKEN:
        missing.append("DATABRICKS_TOKEN")

    if not DATABRICKS_ENDPOINT:
        missing.append("DATABRICKS_ENDPOINT")

    if missing:
        st.error(f"Missing required secrets: {', '.join(missing)}")
        st.stop()


validate_config()


# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick" not in st.session_state:
    st.session_state.quick = "Weather in Singapore?"


# =========================
# STYLES
# =========================
st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.image("https://github.com/vijjikodali.png", width=140)

    st.markdown("### Ravi Kumar")
    st.markdown("Solution Architect")

    st.markdown("---")
    st.success("✅ Databricks Serverless - Live Tested")
    st.success("✅ OpenWeather API")
    st.success("✅ Streamlit Cloud")

    st.markdown("---")
    st.markdown("[🐙 GitHub Profile](https://github.com/vijjikodali)")
    st.markdown("[📂 GitHub Repository](https://github.com/vijjikodali/weather-agent-llama)")


# =========================
# HEADER
# =========================
st.title("⛅ Weather Agent")
st.caption("Built by Ravi Kumar | Databricks Serverless AI + OpenWeather API")


# =========================
# BASIC CITY EXTRACTION FALLBACK
# =========================
def extract_city_fallback(text: str) -> str:
    if not text:
        return "Singapore"

    cleaned = re.sub(r"[?.!,]", "", text).strip()

    match = re.search(r"\bin\s+([A-Za-z\s]+)", cleaned, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        city = re.sub(
            r"\b(today|tomorrow|now|weather|gym|coffee|beach)\b",
            "",
            city,
            flags=re.IGNORECASE
        ).strip()
        return city or "Singapore"

    words = cleaned.split()
    return words[-1] if words else "Singapore"


# =========================
# DATABRICKS CITY EXTRACTION
# =========================
def extract_city_with_llm(user_query: str) -> str:
    if ENV == "ci":
        return extract_city_fallback(user_query)

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "Extract the city name from the user query. "
                    "Return only the city name. "
                    "Do not return explanation, punctuation, JSON, or extra text. "
                    "If no city is found, return Singapore."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        "max_tokens": 20,
        "temperature": 0
    }

    try:
        response = requests.post(
            DATABRICKS_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.status_code != 200:
            return extract_city_fallback(user_query)

        city = response.json()["choices"][0]["message"]["content"].strip()
        city = re.sub(r"[^A-Za-z\s]", "", city).strip()

        return city or extract_city_fallback(user_query)

    except Exception:
        return extract_city_fallback(user_query)


# =========================
# OPENWEATHER API
# =========================
def get_weather(city: str):
    if ENV == "ci":
        return {
            "temp": 28,
            "desc": "mock weather",
            "clouds": 40,
            "icon": "02d"
        }, None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 401:
            return None, "Invalid OpenWeather API key."

        if response.status_code == 404:
            return None, f"City not found: {city}"

        if response.status_code != 200:
            return None, f"OpenWeather API error: {response.status_code}"

        data = response.json()

        return {
            "temp": data["main"]["temp"],
            "feels_like": data["main"].get("feels_like"),
            "humidity": data["main"].get("humidity"),
            "desc": data["weather"][0]["description"],
            "clouds": data.get("clouds", {}).get("all", 0),
            "wind": data.get("wind", {}).get("speed"),
            "icon": data["weather"][0]["icon"]
        }, None

    except requests.exceptions.Timeout:
        return None, "OpenWeather request timed out."

    except requests.exceptions.RequestException as e:
        return None, f"OpenWeather request failed: {e}"

    except Exception as e:
        return None, f"Unexpected weather error: {e}"


# =========================
# DATABRICKS FINAL RESPONSE
# =========================
def call_weather_agent(query: str, city: str, weather: dict):
    if ENV == "ci":
        return "☔ Mock response: carry umbrella if needed.", None

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a practical weather assistant. "
                    "Give short, useful advice based on the weather. "
                    "Mention whether the user can proceed with the activity. "
                    "Keep the answer under 4 sentences."
                )
            },
            {
                "role": "user",
                "content": (
                    f"User query: {query}\n"
                    f"City: {city}\n"
                    f"Temperature: {weather['temp']}°C\n"
                    f"Feels like: {weather.get('feels_like')}°C\n"
                    f"Weather: {weather['desc']}\n"
                    f"Clouds: {weather['clouds']}%\n"
                    f"Humidity: {weather.get('humidity')}%\n"
                    f"Wind speed: {weather.get('wind')} m/s"
                )
            }
        ],
        "max_tokens": 120,
        "temperature": 0.2
    }

    try:
        response = requests.post(
            DATABRICKS_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return None, f"Databricks API error: {response.status_code} - {response.text}"

        return response.json()["choices"][0]["message"]["content"], None

    except requests.exceptions.Timeout:
        return None, "Databricks request timed out."

    except requests.exceptions.RequestException as e:
        return None, f"Databricks request failed: {e}"

    except Exception as e:
        return None, f"Unexpected Databricks error: {e}"


# =========================
# QUICK ACTIONS
# =========================
st.write("### Quick Prompts")

col1, col2, col3 = st.columns(3)

if col1.button("🏃 Gym Singapore"):
    st.session_state.quick = "Can I go gym today in Singapore?"

if col2.button("☕ Coffee Hyderabad"):
    st.session_state.quick = "Is it good weather for coffee in Hyderabad?"

if col3.button("🏖️ Beach Mumbai"):
    st.session_state.quick = "Can I go to beach today in Mumbai?"


# =========================
# CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# =========================
# USER INPUT
# =========================
query = st.chat_input(st.session_state.quick)


# =========================
# MAIN FLOW
# =========================
if query:
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Checking live weather and generating advice..."):
            city = extract_city_with_llm(query)
            weather, weather_error = get_weather(city)

            if weather_error:
                st.error(weather_error)

            else:
                result, llm_error = call_weather_agent(query, city, weather)

                if llm_error:
                    st.error(llm_error)

                else:
                    st.image(
                        f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png",
                        width=90
                    )

                    st.success(result)

                    st.caption(
                        f"Detected city: {city} | "
                        f"Temp: {weather['temp']}°C | "
                        f"Condition: {weather['desc']}"
                    )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result
                    })


# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    """
    <div style='text-align:center'>
        Built by <b>Ravi Kumar</b><br>
        Powered by Databricks Serverless AI + OpenWeather API<br><br>
        <a href='https://github.com/vijjikodali/weather-agent-llama'>
            GitHub Repository
        </a>
    </div>
    """,
    unsafe_allow_html=True
)