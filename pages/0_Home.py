import streamlit as st

st.title("🏏 Cricbuzz LiveStats")
st.markdown("""
A comprehensive cricket analytics dashboard integrating **Cricbuzz API** with **SQL**.

### Modules
- **Live Matches**: Real-time scores from Cricbuzz API
- **Top Players**: Batting & bowling statistics
- **SQL Analytics**: 25 practice queries (Beginner → Advanced)
- **CRUD**: Manage player records

### Setup
1. Add your RapidAPI key to `.streamlit/secrets.toml`
2. Run: `streamlit run main.py`
""")
