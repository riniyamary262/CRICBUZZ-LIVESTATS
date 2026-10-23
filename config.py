import os
import streamlit as st

# Load from secrets.toml when deployed; fallback to env var locally
def get_api_key():
    try:
        return st.secrets["RAPIDAPI_KEY"]
    except Exception:
        return os.environ.get("RAPIDAPI_KEY", "")

API_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"
DB_PATH = "cricket.db"