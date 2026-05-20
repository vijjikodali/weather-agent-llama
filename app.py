import streamlit as st
import requests
import re
import os
from databricks import sql

# =========================
# STREAMLIT PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Weather Agent",
    page_icon="⛅",
    layout="centered"
)

# =========================
# SECRETS
# =========================
DATABRICKS_HOST = st.secrets["DATABRICKS_HOST"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
DATABRICKS_HTTP_PATH = st.secrets["DATABRICKS_HTTP_PATH"]
DATABRICKS_ENDPOINT = st.secrets["DATABRICKS_ENDPOINT"]
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# =========================
# CHAT MEMORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    color: white;
}

[data-testid="stChatMessage"] {
    background-color: rgba(255,255,255,0.06);
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

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists("photo.jpg"):
        try:
            st.image("photo.jpg", width=90)
        except Exception:
            st.image("https://github.com/vijjikodali.png", width=90)
    else:
        st.image("https://github.com/vijjikodali.png", width=90)

with col2:
    st.title("⛅ Weather Agent")
    st.caption(
        "Built by Vijayalaxmi Kodali | "
        "[LinkedIn](https://www.linkedin.com/in/kodali-vijayalaxmi-40860222) | "
        "[GitHub](https://github.com/vijjikodali/weather-agent-llama)"
    )

st.divider()

# =========================
# FUNCTIONS
# =========================

def extract_city(text):
    match = re.search(r'\bin\s+([A-Za-z\s]+)', text, re.IGNORECASE)

    if match:
        city = match.group(1).strip()

        city = re.sub(
            r'\b(tomorrow|today|now|weekend|morning|evening|tonight)\b.*',
            '',
            city,
            flags=re.IGNORECASE
        ).strip()

        city = city.strip('?.,!')
        return city

    words = text.replace('?', '').split()

    return words[-1] if words else "Hyderabad"


def get_weather(city):

    city_map = {
        "singapore": "Singapore,SG",
        "hyderabad": "Hyderabad,IN",
        "mumbai": "Mumbai,IN",
        "delhi": "Delhi,IN"
    }

    city_query = city_map.get(city.lower(), city)

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city_query}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:

            data = response.json()

            return {
                'temp': data['main']['temp'],
                'desc': data['weather'][0]['description'],
                'rain': data.get('clouds', {}).get('all', 0),
                'icon': data['weather'][0]['icon']
            }, None

        else:
            return None, f"City not found: {city}"

    except Exception as e:
        return None, f"Weather API error: {e}"


def call_databricks_llm(query, temp, desc, rain):

    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""
User asks: {query}

Weather:
- Temperature: {temp}°C
- Condition: {desc}
- Cloud cover: {rain}%

Give a short, friendly suggestion.
Mention umbrella/jacket if needed.
Keep under 40 words.
"""

    # FINAL FIXED PAYLOAD
    payload = {
        "model": "databricks-meta-llama-3-1-70b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 60,
        "temperature": 0.2
    }

    try:

        response = requests.post(
            DATABRICKS_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:

            result = response.json()

            return result['choices'][0]['message']['content'].strip(), None

        else:

            return None, (
                f"Databricks LLM error "
                f"{response.status_code}: {response.text}"
            )

    except Exception as e:

        return None, f"Databricks LLM error: {e}"
    try:

        response = requests.post(
            DATABRICKS_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:

            result = response.json()

            return result['choices'][0]['message']['content'].strip(), None

        else:
            return None, (
                f"Databricks LLM error "
                f"{response.status_code}: {response.text}"
            )

    except Exception as e:
        return None, f"Databricks LLM error: {e}"


# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.subheader("🔧 Dev Tools")

    if st.button("Test Databricks SQL"):

        try:

            with sql.connect(
                server_hostname=DATABRICKS_HOST,
                http_path=DATABRICKS_HTTP_PATH,
                access_token=DATABRICKS_TOKEN,
                _socket_timeout=60
            ) as connection:

                with connection.cursor() as cursor:

                    cursor.execute(
                        "SELECT current_date() as today, 1+1 as test_calc"
                    )

                    result = cursor.fetchall()

                    st.success(
                        f"SQL Connected ✅ {result[0][0]}, "
                        f"Calc: {result[0][1]}"
                    )

        except Exception as e:
            st.error(f"Databricks SQL Failed ❌ {e}")

# =========================
# QUICK PROMPTS
# =========================
st.write("### Quick Prompts")

c1, c2, c3 = st.columns(3)

if c1.button("🏃 Gym Singapore", use_container_width=True):
    st.session_state.quick_prompt = "Gym in Singapore"

if c2.button("☕ Coffee Hyderabad", use_container_width=True):
    st.session_state.quick_prompt = "Coffee in Hyderabad"

if c3.button("🏖️ Beach Mumbai", use_container_width=True):
    st.session_state.quick_prompt = "Beach in Mumbai"

# =========================
# DISPLAY CHAT HISTORY
# =========================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# =========================
# CHAT INPUT
# =========================
query = st.chat_input(
    st.session_state.get(
        "quick_prompt",
        "Tomorrow gym in Hyderabad?"
    )
)

# =========================
# MAIN CHAT FLOW
# =========================
if query:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Show user message
    with st.chat_message("user"):
        st.write(query)

    city = extract_city(query)

    weather, err = get_weather(city)

    if err:

        with st.chat_message("assistant"):
            st.error(err)

    else:

        with st.chat_message("assistant"):

            with st.spinner("🌦️ AI Weather Agent thinking..."):

                suggestion, llm_err = call_databricks_llm(
                    query,
                    weather['temp'],
                    weather['desc'],
                    weather['rain']
                )

            if llm_err:

                st.error(llm_err)

            else:

                st.image(
                    f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png",
                    width=80
                )

                st.success(suggestion)

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "🌡️ Temp",
                    f"{weather['temp']}°C"
                )

                c2.metric(
                    "☁️ Weather",
                    weather['desc']
                )

                c3.metric(
                    "💧 Clouds",
                    f"{weather['rain']}%"
                )

                assistant_reply = f"""
{suggestion}

🌡️ Temp: {weather['temp']}°C  
☁️ Condition: {weather['desc']}  
💧 Clouds: {weather['rain']}%
"""

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_reply
                    }
                )

                # Share block
                share_text = f"""
Weather tip for {city}: {suggestion}

Built by Vijayalaxmi Kodali
Try it:
https://weather-agent-llama.streamlit.app
"""

                st.text_area(
                    "📱 Copy to share:",
                    share_text,
                    height=120
                )

st.divider()

st.caption(
    "Made with Streamlit + Databricks + OpenWeather | "
    "Built by Vijayalaxmi Kodali"
)
