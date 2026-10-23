import streamlit as st
from services.analytics_service import run_query

st.title("⭐ Top Players")

df, err = run_query(3)  # Top ODI run scorers
if err:
    st.warning("Seed sample data to see stats.")
else:
    st.subheader("Top ODI Run Scorers")
    st.dataframe(df)