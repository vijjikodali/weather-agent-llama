import os
import streamlit as st
import requests
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# API Keys from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Databricks secrets (using environment for consistency, or st.secrets if preferred)
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")

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
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'temp': data['main']['temp'],
                'desc': data['weather'][0]['description'],
                'rain': data.get('pop', 0) * 100 if 'pop' in data else data.get('rain', {}).get('1h', 0)
            }, None
        else:
            return None, f"City not found: {city}"
    except Exception as e:
        return None, f"Weather API error: {e}"

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2, api_key=GROQ_API_KEY)

prompt = PromptTemplate.from_template(
    "User asks: {query}\nWeather: {temp}°C, {desc}, {rain}% rain chance.\nGive a short, friendly suggestion for their activity. Mention if they need umbrella/jacket. Keep under 40 words."
)
chain = prompt | llm | StrOutputParser()

st.set_page_config(page_title="Weather Agent", page_icon="⛅")
st.title("⛅ Weather Agent - Llama 3.3 + Databricks")
# ----- DATABRICKS CONNECTION TEST -----
import pandas as pd
from databricks import sql

if st.sidebar.button("Test Databricks Connection"):
    try:
        with sql.connect(
            server_hostname=DATABRICKS_HOST,
            http_path=DATABRICKS_HTTP_PATH,
            access_token=DATABRICKS_TOKEN
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_date() as today, 1+1 as test_calc")
                result = cursor.fetchall()
                st.sidebar.success(f"Connected ✅ Databricks says: {result[0][0]}, Calc: {result[0][1]}")
    except Exception as e:
        st.sidebar.error(f"Databricks Failed ❌ {e}")
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
            response = chain.invoke({
                "query": query,
                "temp": weather['temp'],
                "desc": weather['desc'],
                "rain": weather['rain']
            })
            st.subheader("AI Suggestion:")
            st.success(response)
            st.caption(f"Temp: {weather['temp']}°C | Condition: {weather['desc']} | Rain: {weather['rain']:.0f}% | City: {city}")