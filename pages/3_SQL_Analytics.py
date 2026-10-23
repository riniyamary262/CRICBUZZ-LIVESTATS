import streamlit as st
from services.analytics_service import run_query, get_query_meta
from sql.queries import QUERIES

st.title("📊 SQL Analytics")

qid = st.selectbox("Select Query", list(QUERIES.keys()),
                   format_func=lambda x: f"Q{x}: {QUERIES[x]['title']} ({QUERIES[x]['level']})")

meta = get_query_meta(qid)
st.caption(f"**Level**: {meta['level']}")
st.code(meta["sql"], language="sql")

if st.button("Run Query"):
    df, err = run_query(qid)
    if err:
        st.error(err)
    else:
        st.dataframe(df, use_container_width=True)