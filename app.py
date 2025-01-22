# app.py
import streamlit as st
from streamlit import session_state as state
from streamlit_nej_datepicker import datepicker_component, Config
from persiantools.jdatetime import JalaliDate
from datetime import datetime
import pytz
import pandas as pd
from utils.database import list_athlete, list_athlete_history
from st_supabase_connection import SupabaseConnection, execute_query


st.set_page_config(
    page_title="ارزیابی عملکرد کشتی",
    page_icon="🎯",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={}
)

try:
    st.session_state["client"] = st.connection(
        name="supabase",
        type=SupabaseConnection,
        ttl=None,
    )
    st.session_state["initialized"] = True
except Exception as e:
    st.error(
        f"""Client initialization failed
        {e}""",
        icon="❌",
    )
    st.session_state["initialized"] = False


if "record_data" not in st.session_state:
    st.session_state.record_data = {}


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/styles/custom.css")




# Widgets shared by all the pages
strength = st.Page(
    "pages/form/strength.py", title="قدرت", icon=":material/notification_important:"
)
stamina = st.Page(
    "pages/form/stamina.py", title="استقامت", icon=":material/notification_important:"
)
anaerobic = st.Page(
    "pages/form/anaerobic.py", title="بی هوازی", icon=":material/notification_important:"
)
agility = st.Page(
    "pages/form/agility.py", title="چابکی", icon=":material/notification_important:"
)
reaction = st.Page(
    "pages/form/reaction.py", title="عکس العمل", icon=":material/notification_important:"
)
felexibility = st.Page(
    "pages/form/felexibility.py", title="انعطاف پذیری", icon=":material/notification_important:"
)
power = st.Page(
    "pages/form/power.py", title="توان", icon=":material/notification_important:"
)
muscle_stamina = st.Page(
    "pages/form/muscle_stamina.py", title="استقامت عضلانی", icon=":material/power:"
)
sleep = st.Page(
    "pages/form/sleep.py", title="خواب", icon=":material/sleep:"
)
stress_anxiety = st.Page(
    "pages/form/stress_anxiety.py", title="استرس - اضطراب", icon=":material/sleep:"
)
blood_urine = st.Page(
    "pages/form/blood_urine.py", title="خون - ادرار", icon=":material/sleep:"
)
anaerobic_report = st.Page(
    "pages/report/anaerobic_report.py", title="بی هوازی", icon=":material/sleep:"
)
orm = st.Page(
    "pages/form/orm.py", title="orm", icon=":material/notification_important:"
)
athlethes = st.Page(
    "pages/athlethe/list.py", title="ورزشکاران", icon=":material/notification_important:"
)
overview = st.Page(
    "pages/athlethe/overview.py", title="overview", icon=":material/notification_important:"
)


# Title
# st.title("سامانه پایش کشتی گیران آزاد")

# Sidebar Jalali Date Input



pg = st.navigation(
    {
        "ورزشکاران": [athlethes, overview],
        "تست ها:": [strength, stamina, anaerobic, agility, reaction, felexibility, power, muscle_stamina],
        "پرسشنامه ها:": [sleep, stress_anxiety, blood_urine],
        "گزارش": [anaerobic_report, orm],

    }
)

pg.run()







