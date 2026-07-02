
import os
import streamlit as st

# ---------------- SECRETS ----------------
def get_secret(name, default=""):
    # 1. GitHub Actions / local environment variables
    value = os.getenv(name)
    if value:
        return value

    # 2. Streamlit secrets.toml
    return st.secrets.get(name, default)

OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")
DATABRICKS_TOKEN = get_secret("DATABRICKS_TOKEN")
DATABRICKS_HOST = get_secret("DATABRICKS_HOST")
DATABRICKS_HTTP_PATH = get_secret("DATABRICKS_HTTP_PATH")
GROQ_API_KEY = get_secret("GROQ_API_KEY")