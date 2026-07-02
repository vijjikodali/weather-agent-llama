
import streamlit as st

from config import (
    OPENWEATHER_API_KEY,
    DATABRICKS_TOKEN,
    DATABRICKS_HOST,
    DATABRICKS_HTTP_PATH,
    GROQ_API_KEY,
)

def validate_config():
    missing = [
        k for k, v in {
            "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
            "DATABRICKS_TOKEN": DATABRICKS_TOKEN,
            "DATABRICKS_HOST": DATABRICKS_HOST,
            "DATABRICKS_HTTP_PATH": DATABRICKS_HTTP_PATH,
            "GROQ_API_KEY": GROQ_API_KEY,
        }.items()
        if not v
    ]

    if missing:
        st.error(f"Missing secrets: {', '.join(missing)}")
        st.stop()