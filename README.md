# weather-agent-llama
AI weather advisor using Groq Llama 3.3 + OpenWeather API. Logs user queries to Databricks for analytics. Built with Streamlit + Python.
# Weather Agent - Llama 4 + Databricks

AI weather advisor that answers natural language queries like "Should I run tomorrow?" using real-time weather data + LLM reasoning.

**Live Demo:** [Your Streamlit Link]

### Features
- **Groq Llama 3.3 70B** for fast, accurate weather advice
- **OpenWeather API** integration for real-time data
- **Databricks SQL** logging of every query for analytics
- **Global city support** - Tested: Hyderabad, Singapore, New York, Mumbai
- **Streamlit UI** with chat interface

### Tech Stack
**Backend:** Python, Databricks SQL Connector, Groq API  
**Frontend:** Streamlit  
**Data:** OpenWeather API, Databricks Lakehouse  
**Deployment:** Streamlit Community Cloud

### How It Works
1. User asks: "Tomorrow run in Singapore?"
2. App fetches weather data for Singapore
3. Llama 3.3 generates contextual advice
4. Query + response logged to Databricks table

### Local Setup
1. `git clone https://github.com/vijjikodali/weather-agent-llama`
2. `pip install -r requirements.txt`
3. Create `.env` with your API keys
4. `streamlit run app.py`
