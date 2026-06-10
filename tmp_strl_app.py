import streamlit as st

dashboard = st.Page(
    "tmp_strl_app.py",
    title="Demo",
    default=True
)

settings = st.Page(
    "eval_strl_app.py",
    title="Đánh giá"
)

pg = st.navigation([
    dashboard,
    settings
])

pg.run()
