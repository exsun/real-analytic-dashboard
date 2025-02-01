"muscle_stamina - استقامت عضلانی"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.charts import bar_line_plot
import datetime
import time

# Initialize session state for storing test results
if "muscle_stamina_test_data" not in st.session_state:
    st.session_state.muscle_stamina_test_data = []

st.header("استقامت عضلانی")
athletes = pd.DataFrame(listAthletes())
athlete_name = st.selectbox("ورزشکار", 
    athletes["name"], 
    placeholder="انتخاب کنید",
)
athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

tab1, tab2, tab3, tab4 = st.tabs(["آزمون دراز و نشست", "آزمون بارفیکس", "آزمون دیپ پارالل", "📋 گزارش"])

with tab1:
    st.subheader("آزمون استقامت عضلانی")
    st.subheader("دراز و نشست با توپ مدیسین بال (۱۰٪ وزن بدن)")
  
    col1, col2 = st.columns(2)
    with col1:
        with st.form("situp_form", enter_to_submit=False, clear_on_submit=False, border=True):

            situp_reps = st.number_input("تعداد دراز و نشست (در یک دقیقه)", min_value=0, step=1, key="situp_reps")
            # medicine_ball_weight = st.number_input("وزن توپ مدیسن بال", min_value=0, step=1, key="medicine_ball")
            
            day , month, year= st.columns(3)
            with year:
                years = list(range(JalaliDate.today().year+1, 1390, -1))
                selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year))
            with month:
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
                selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1)
            with day:
                days = list(range(1, 32))
                selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1)
            selected_time = st.time_input("زمان", datetime.time(8, 45))

            record_date = JalaliDateTime(selected_year, months.index(selected_month) + 1, selected_day, locale="en")
            gregorian_date = record_date.to_gregorian()
            
            record_date = record_date.strftime("%Y-%m-%d") + " " + selected_time.strftime("%H:%M:%S")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")  + " " + selected_time.strftime("%H:%M:%S")

            submitted = st.form_submit_button("ثبت")

            if submitted:

                exercise_data = {
                    "situp_reps": situp_reps,
                    # "medicine_ball_weight": medicine_ball_weight
                }

                new_record = {
                    "athlete_id": int(athlete_id),
                    "raw_data": exercise_data,
                    "test_name": "situp",
                    "test_category": "muscle_stamina",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }
                insertRecord(new_record)

    with col2:
        situp_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="situp"))
        if not situp_records.empty:
            situp_records['situp_reps'] = situp_records['raw_data'].apply(lambda x: x['situp_reps'])

            bar_line_plot(x=situp_records["test_date"], y=situp_records["situp_reps"], xaxis_title="تاریخ" ,yaxis_title="تعداد", title="آزمون دراز نشست (تعداد)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

with tab2:   
    st.subheader("آزمون بارفیکس")
  
    col1, col2 = st.columns(2)
    with col1:
        with st.form("pullup_form", enter_to_submit=False, clear_on_submit=False, border=True):
            
            pullup_reps = st.number_input("تعداد بارفیکس", min_value=0, step=1, key="pullup_reps")

            day , month, year= st.columns(3)
            with year:
                years = list(range(JalaliDate.today().year+1, 1390, -1))
                selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year))
            with month:
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
                selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1)
            with day:
                days = list(range(1, 32))
                selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1)
            selected_time = st.time_input("زمان", datetime.time(8, 45))

            record_date = JalaliDateTime(selected_year, months.index(selected_month) + 1, selected_day, locale="en")
            gregorian_date = record_date.to_gregorian()
            
            record_date = record_date.strftime("%Y-%m-%d") + " " + selected_time.strftime("%H:%M:%S")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")  + " " + selected_time.strftime("%H:%M:%S")

            submitted = st.form_submit_button("ثبت")

            if submitted:

                exercise_data = {
                    "pullup_reps": pullup_reps,
                }

                new_record = {
                    "athlete_id": int(athlete_id),
                    "raw_data": exercise_data,
                    "test_name": "pullup",
                    "test_category": "muscle_stamina",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }
                insertRecord(new_record)

    with col2:
        pullup_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="pullup"))
        if not pullup_records.empty:
            pullup_records['pullup_reps'] = pullup_records['raw_data'].apply(lambda x: x['pullup_reps'])

            bar_line_plot(x=pullup_records["test_date"], y=pullup_records["pullup_reps"], xaxis_title="تاریخ" ,yaxis_title="تعداد", title="آزمون بارفیکس (تعداد)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

with tab3:   
    st.subheader("آزمون دیپ پارالل")
  
    col1, col2 = st.columns(2)
    with col1:
        with st.form("dip_parallel_form", enter_to_submit=False, clear_on_submit=False, border=True):
            
            dip_parallel_reps = st.number_input("تعداد دیپ پارالل", min_value=0, step=1, key="dip_parallel_reps")

            day , month, year= st.columns(3)
            with year:
                years = list(range(JalaliDate.today().year+1, 1390, -1))
                selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year))
            with month:
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
                selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1)
            with day:
                days = list(range(1, 32))
                selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1)
            selected_time = st.time_input("زمان", datetime.time(8, 45))

            record_date = JalaliDateTime(selected_year, months.index(selected_month) + 1, selected_day, locale="en")
            gregorian_date = record_date.to_gregorian()
            
            record_date = record_date.strftime("%Y-%m-%d") + " " + selected_time.strftime("%H:%M:%S")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")  + " " + selected_time.strftime("%H:%M:%S")

            submitted = st.form_submit_button("ثبت")

            if submitted:

                exercise_data = {
                    "dip_parallel_reps": dip_parallel_reps,
                }

                new_record = {
                    "athlete_id": int(athlete_id),
                    "raw_data": exercise_data,
                    "test_name": "dip_parallel",
                    "test_category": "muscle_stamina",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }
                insertRecord(new_record)

    with col2:
        dip_parallel_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="dip_parallel"))
        if not dip_parallel_records.empty:
            dip_parallel_records['dip_parallel_reps'] = dip_parallel_records['raw_data'].apply(lambda x: x['dip_parallel_reps'])

            bar_line_plot(x=dip_parallel_records["test_date"], y=dip_parallel_records["dip_parallel_reps"], xaxis_title="تاریخ" ,yaxis_title="تعداد", title="آزمون دیپ پارالل (تعداد)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")