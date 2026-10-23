import streamlit as st
from services.player_service import create_player, get_all_players, update_player, delete_player

st.title("✏️ CRUD Operations")

tab1, tab2, tab3 = st.tabs(["Create", "Read", "Update/Delete"])

with tab1:
    with st.form("create"):
        name = st.text_input("Name")
        country = st.text_input("Country")
        role = st.selectbox("Role", ["Batsman","Bowler","All-rounder","Wicket-keeper"])
        bat = st.text_input("Batting style")
        bowl = st.text_input("Bowling style")
        if st.form_submit_button("Add Player"):
            create_player(name, country, role, bat, bowl)
            st.success("Player added")

with tab2:
    players = get_all_players()
    if players:
        st.dataframe(players)

with tab3:
    players = get_all_players()
    if players:
        p = st.selectbox("Select player", players, format_func=lambda x: x["name"])
        new_name = st.text_input("New name", value=p["name"])
        if st.button("Update"):
            update_player(p["player_id"], new_name, p["country"], p["role"])
            st.success("Updated")
        if st.button("Delete", type="secondary"):
            delete_player(p["player_id"])
            st.warning("Deleted")