import streamlit as st
from utils.db_connection import init_db

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")

if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

pg = st.navigation([
    st.Page("pages/0_Home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/1_Live_Matches.py", title="Live Matches", icon="📡"),
    st.Page("pages/2_Top_Players.py", title="Top Players", icon="⭐"),
    st.Page("pages/3_SQL_Analytics.py", title="SQL Analytics", icon="📊"),
    st.Page("pages/4_CRUD.py", title="CRUD Operations", icon="✏️"),
])
pg.run()