import streamlit as st
import requests
import re
import pandas as pd
from databricks import sql

# All keys from Streamlit Secrets
DATABRICKS_HOST = st.secrets["dbc-efb575fe-3817.cloud.databricks.com"]
DATABRICKS_TOKEN = st.secrets["OPENWEATHER_API_KEY = st.secrets["27d2aad3e92bac30a9929b2f570db79e"]
DATABRICKS_HOST = st.secrets["DATABRICKS_HOST"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
DATABRICKS_HTTP_PATH = st.secrets["/sql/1.0/warehouses/4945f74d9ad52cfb"]
DATABRICKS_ENDPOINT = st.secrets["DATABRICKS_ENDPOINT"] # e.g. "databricks-llama-4-maverick"


# Build the URL properly
DATABRICKS_MODEL_URL = f"https://{DATABRICKS_HOST}/serving-endpoints/{DATABRICKS_ENDPOINT}/invocations"

def extract_city(text):
    match = re.search(r'\bin\s+([A-Za-z\s]+)', text, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        city = re.sub(r'\b(tomorrow|today|now|weekend|morning|evening|tonight)\b.*', '', city, flags=re.IGNORECASE).strip()
        city = city.strip('?.,!')
        return city
    words = text.replace('?', '').split()
    return words[-1] if words else "Hyderabad"

def get_weather(city):
    # Try with country code for common cities
    city_map = {
        "Singapore": "Singapore, SG",
        "Hyderabad": "Hyderabad, IN",
        "Mumbai": "Mumbai, IN",
        "Delhi": "Delhi, IN"
    }

    city_query = city_map.get(city.lower(), city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'temp': data['main']['temp'],
                'desc': data['weather'][0]['description'],
                'rain': data.get('clouds', {}).get('all', 0) # using cloud % as rain proxy
            }, None
        else:
            return None, f"City not found: {city}. API said: {response.json().get('message')}"
    except Exception as e:
        return None, f"Weather API error: {e}"

def call_databricks_llm(query, temp, desc, rain):
    """Call Databricks Model Serving endpoint"""
    url = f"{DATABRICKS_HOST}/serving-endpoints/{DATABRICKS_ENDPOINT}/invocations"
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""User asks: {query}
Weather: {temp}°C, {desc}, {rain}% rain chance.
Give a short, friendly suggestion for their activity. Mention if they need umbrella/jacket. Keep under 40 words."""

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 60,
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip(), None
        else:
            return None, f"Databricks LLM error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Databricks LLM error: {e}"

st.set_page_config(page_title="Weather Agent", page_icon="⛅")
st.title("⛅ Weather Agent - Databricks Llama")

# ----- DATABRICKS SQL CONNECTION TEST -----
if st.sidebar.button("Test Databricks SQL"):
    try:
        with sql.connect(
            server_hostname=DATABRICKS_HOST,
            http_path=DATABRICKS_HTTP_PATH,
            access_token=DATABRICKS_TOKEN
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_date() as today, 1+1 as test_calc")
                result = cursor.fetchall()
                st.sidebar.success(f"SQL Connected ✅ {result[0][0]}, Calc: {result[0][1]}")
    except Exception as e:
        st.sidebar.error(f"Databricks SQL Failed ❌ {e}")
# ----- END TEST -----

query = st.text_input("Ask about your plans:", placeholder="Tomorrow gym in Hyderabad?")

if st.button("Check"):
    if not query.strip():
        st.warning("Please enter your plan with a city")
    else:
        city = extract_city(query)
        st.write(f"Checking weather for: {city}")

        weather, err = get_weather(city)
        if err:
            st.error(err)
        else:
            with st.spinner("Asking Databricks Llama..."):
                suggestion, llm_err = call_databricks_llm(query, weather['temp'], weather['desc'], weather['rain'])

            if llm_err:
                st.error(llm_err)
            else:
                st.subheader("AI Suggestion:")
                st.success(suggestion)
                st.caption(f"Temp: {weather['temp']}°C | Condition: {weather['desc']} | Rain: {weather['rain']}%")
