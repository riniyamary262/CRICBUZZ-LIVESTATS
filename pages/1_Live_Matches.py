import streamlit as st
from api.cricbuzz_client import fetch_live_matches

st.title("📡 Live Matches")

if st.button("Refresh Live Scores"):
    with st.spinner("Fetching..."):
        data = fetch_live_matches()
    if "error" in data:
        st.error(data["error"])
    else:
        st.success("Live data fetched")
        st.json(data)

st.info(
    "Live data requires a RapidAPI key with an active subscription to the "
    "Cricbuzz Cricket API. Configure it in `.streamlit/secrets.toml`."
)
