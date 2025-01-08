# app.py
import streamlit as st
from streamlit import session_state as state
from streamlit_nej_datepicker import datepicker_component, Config
from persiantools.jdatetime import JalaliDate
from datetime import datetime
import pytz

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
# orm = st.Page(
#     "pages/form/orm.py", title="orm", icon=":material/notification_important:"
# )
# dashboard = st.Page(
#     "pages/dashboard.py", title="قدرت", icon=":material/notification_important:"
# )


# Title
st.title("سامانه پایش کشتی گیران ایران")

# Sidebar Jalali Date Input



if "record_data" not in st.session_state:
    st.session_state.record_data = {}

col1, col2 = st.columns(2)
    
with col1:
    col12, col13 = st.columns(2,vertical_alignment="top")
    with col12:
        athlete_name = st.text_input("نام ورزشکار", key="athlete_name")
    with col13:
        athlete_weight = st.number_input("وزن ورزشکار", key="athlete_weight")



with col2:
    years = list(range(JalaliDate.today().year+1, 1390, -1))
    months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    days = list(range(1, 32))

    col21, col22, col23 = st.columns(3,vertical_alignment="top")

    with col21:
        selected_year = st.selectbox("سال", years, index=years.index(JalaliDate.today().year))
    with col22:
        selected_month = st.selectbox("ماه", months, index=JalaliDate.today().month - 1)
    with col23:
        selected_day = st.selectbox("روز", days, index=JalaliDate.today().day - 1)

    # Convert to Jalali Date
    record_date = JalaliDate(selected_year, months.index(selected_month) + 1, selected_day)

    # Convert to Gregorian for internal processing (if needed)
    gregorian_date = record_date.to_gregorian()

    # Display Selected Jalali Date
#     if not record_date:
#         # st.session_state.record_date = None

#     else:
#         st.subheader(record_date)
#         st.session_state.record_data["date"] = record_date
# if not athlete_name:

    

# else:
st.session_state.record_data["date"] = record_date
st.session_state.record_data["athlete_name"] = athlete_name
st.session_state.record_data["athlete_weight"] = athlete_weight

# with col1:
#     st.subheader(athlete_name)
# with col2:
#     st.subheader(record_date)
if athlete_name and athlete_weight != 0.0:
    pg = st.navigation(
        {
            "تست ها:": [strength, stamina, anaerobic, agility, reaction, felexibility, power, muscle_stamina],
            "پرسشنامه ها:": [sleep, stress_anxiety, blood_urine],
            "گزارش": [anaerobic_report]

        }
    )

    pg.run()







