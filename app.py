# app.py
import streamlit as st
from streamlit import session_state as state

st.set_page_config(
    page_title="ارزیابی عملکرد کشتی",
    page_icon="🎯",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={}
)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles/custom.css")

form = st.Page(
    "pages/form/power.py", title="تست قدرت", icon=":material/notification_important:"
)

onerm = st.Page(
    "pages/form/orm.py", title="orm", icon=":material/notification_important:"
)

dashboard = st.Page(
    "pages/dashboard.py", title="قدرت", icon=":material/notification_important:"
)
pg = st.navigation(
        {
            "فرم": [form],
            "آنالیز": [dashboard],
            "onerm": [onerm],

        }
    )


pg.run()
