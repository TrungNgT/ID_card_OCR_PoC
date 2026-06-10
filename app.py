import streamlit as st

dashboard = st.Page(
    "pages/tmp_strl_app.py",
    title="Demo",
    default=True
)

settings = st.Page(
    "pages/eval_strl_app.py",
    title="Đánh giá"
)

pg = st.navigation([
    dashboard,
    settings
])

pg.run()
