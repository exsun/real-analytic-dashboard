# app.py
import streamlit as st
from streamlit import session_state as state
from utils import local_css
st.set_page_config(
    page_title="ارزیابی عملکرد کشتی",
    page_icon="🎯",
    layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={}
)
# def main():

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

local_css("styles/custom.css")

pg.run()
