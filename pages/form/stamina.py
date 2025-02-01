"stamina - اسقامت"
import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
from persiantools.jdatetime import JalaliDate
from components.charts import bar_line_plot
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import jdatetime
from zoneinfo import ZoneInfo
import time


# Initialize session state for VO2Max data if not already set
if "vo2max_data" not in st.session_state:
    st.session_state.vo2max_data = []

# Function to calculate VO2Max for the 6-Minute Test
def calculate_vo2max_6min(distance_km):
    return round(distance_km * 33, 2)

# Function to calculate VO2Max for the Cooper Test
def calculate_vo2max_cooper(distance_km):
    distance_meters = distance_km * 1000
    return round((distance_meters - 504.9) / 44.73, 2)



st.header("استقامت")
athletes = pd.DataFrame(listAthletes())
athlete_name = st.selectbox("ورزشکار", 
    athletes["name"], 
    placeholder="انتخاب کنید",
)
athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""

tab1, tab2, tab3 = st.tabs(["۶ دقیقه", "Cooper", "📋 گزارش"])

# Tab 1: 6-Minute Test
with tab1:
    st.subheader("تست ۶ دقیقه")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("6min_form", clear_on_submit=False, enter_to_submit=False):
        

            distance_6min = st.number_input("مسافت طی شده (کیلومتر)", min_value=0.0, step=0.01, key="distance_6min")
            record_type = st.selectbox("آزمون", options=["pre-test","post-test"])
            day , month, year= st.columns(3)
            with year:
                years = list(range(JalaliDate.today().year+1, 1390, -1))
                selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year) , key="year")
            with month:
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
                selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1 , key="month")
            with day:
                days = list(range(1, 32))
                selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1 , key="day")
            selected_time = st.time_input("زمان", datetime.time(8, 45))

            record_date = JalaliDateTime(selected_year, months.index(selected_month) + 1, selected_day, locale="en")
            gregorian_date = record_date.to_gregorian()
            
            record_date = record_date.strftime("%Y-%m-%d") + " " + selected_time.strftime("%H:%M:%S")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")  + " " + selected_time.strftime("%H:%M:%S")


            submitted_6min = st.form_submit_button("محاسبه")
        
        if submitted_6min and distance_6min > 0:
            with st.spinner('در حال محاسبه ...'):
                time.sleep(2.5)
            vo2max = calculate_vo2max_6min(distance_6min)
            exercise_data = {
                "distance_6min": "6-Minute",
                "vo2max": vo2max,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "۶-دقیقه",
                "test_category": "استقامت",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="VO2Max (اکنون)", value=vo2max)
            
            insertRecord(new_record)
            
    with col2:
        sixmin_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="۶-دقیقه"))
        if not sixmin_records.empty:
            sixmin_records['vo2max'] = sixmin_records['raw_data'].apply(lambda x: x['vo2max'])

            bar_line_plot(x=sixmin_records["test_date"], y=sixmin_records["vo2max"], xaxis_title="تاریخ" ,yaxis_title="VO2max", title="6-min-vo2max records")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

# Tab 2: Cooper Test
with tab2:
    st.subheader("تست cooper")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("cooper_form", clear_on_submit=False, enter_to_submit=False):
        
         
            distance_cooper = st.number_input("مسافت طی شده (کیلومتر)", min_value=0.0, step=0.01, key="distance_cooper")
            record_type = st.selectbox("آزمون", options=["pre-test","post-test"])
            day , month, year= st.columns(3)
            with year:
                years = list(range(JalaliDate.today().year+1, 1390, -1))
                selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year))
            with month:
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
                selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1 )
            with day:
                days = list(range(1, 32))
                selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1 )
            selected_time = st.time_input("زمان", datetime.time(8, 45))

            record_date = JalaliDateTime(selected_year, months.index(selected_month) + 1, selected_day, locale="en")
            gregorian_date = record_date.to_gregorian()

            record_date = record_date.strftime("%Y-%m-%d") + " " + selected_time.strftime("%H:%M:%S")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")  + " " + selected_time.strftime("%H:%M:%S")

            submitted_cooper = st.form_submit_button("محاسبه")
        
        if submitted_cooper and distance_cooper > 0:
            vo2max_cooper = calculate_vo2max_cooper(distance_cooper)
            exercise_data = {
                "distance": distance_cooper,
                "vo2max": vo2max_cooper,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "cooper",
                "test_category": "استقامت",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="VO2Max (اکنون)", value=vo2max_cooper)
            
            insertRecord(new_record)
            
    with col2:
        cooper_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="cooper"))
        if not cooper_records.empty:
            cooper_records['vo2max'] = cooper_records['raw_data'].apply(lambda x: x['vo2max'])

            bar_line_plot(x=cooper_records["test_date"], y=cooper_records["vo2max"], xaxis_title="تاریخ" ,yaxis_title="VO2max", title="cooper-vo2max")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")
# Tab 3: History
with tab3:
    st.subheader("📋 گزارش")
    if not sixmin_records.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(sixmin_records)
        with col2:
            bar_line_plot(x=sixmin_records["test_date"], y=sixmin_records["vo2max"], xaxis_title="تاریخ" ,yaxis_title="vo2max", title="6-min-vo2max history")
    else:
        st.info("هنوز داده‌ای ثبت نشده است.")

    if not cooper_records.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(cooper_records)
        with col2:
            bar_line_plot(x=cooper_records["test_date"], y=cooper_records["vo2max"], xaxis_title="تاریخ" ,yaxis_title="vo2max", title="cooper-vo2max history")
    else:
        st.info("هنوز داده‌ای ثبت نشده است.")