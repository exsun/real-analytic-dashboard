"flexibility - انعطاف پذیری"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
import datetime
from utils.database import listAthletes, listAthletesHistory, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from components.charts import bar_line_plot
from persiantools.jdatetime import JalaliDate, JalaliDateTime

# Initialize session state for storing test results
if "flexibility_test_data" not in st.session_state:
    st.session_state.flexibility_test_data = []

st.header("انعطاف پذیری")
athletes = pd.DataFrame(listAthletes())
athlete_name = st.selectbox("ورزشکار", 
    athletes["name"], 
    placeholder="انتخاب کنید",
)
athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""

tab1, tab2, tab3, tab4 = st.tabs(["آزمون sit & reach" , "آزمون بالا آوردن شانه" , "آزمون بالا آوردن شانه" , "📋 گزارش"])

with tab1:
    st.subheader("آزمون sit & reach")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("sit_reach_tests_form", enter_to_submit=False, clear_on_submit=False, border=True):
            sit_reach_distance = st.number_input("فاصله (سانتی‌متر)", step=0.1, key="sit_reach_distance")

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
            # Save results
            exercise_data = {
                "sit_reach_distance": sit_reach_distance,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "sit_reach",
                "test_category": "انعطاف پذیری",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="sit_reach (اکنون)", value=sit_reach)
            
            insertRecord(new_record)

    with col2:
        sit_reach_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="sit_reach"))
        if not sit_reach_records.empty:
            sit_reach_records['sit_reach_distance'] = sit_reach_records['raw_data'].apply(lambda x: x['sit_reach_distance'])

            bar_line_plot(x=sit_reach_records["test_date"], y=sit_reach_records["sit_reach_distance"], xaxis_title="تاریخ" ,yaxis_title="فاصله (سانتی متر)", title=" آزمون sit & reach")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

        

with tab2:
    # Historical Bar Chart
    st.subheader("آزمون بالا آوردن شانه")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("shoulder_lift_tests_form", enter_to_submit=False, clear_on_submit=False, border=True):

            shoulder_lift_distance = st.number_input("بالا آوردن شانه (سانتی‌متر)", step=0.1, key="shoulder_lift_distance")
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
            selected_time = st.session_state.record_data["date"]

            # Save results
            exercise_data = {
                "shoulder_lift_distance": shoulder_lift_distance,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "shoulder_lift",
                "test_category": "انعطاف پذیری",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="shoulder_lift (اکنون)", value=shoulder_lift_distance)
            
            insertRecord(new_record)

    with col2:
        shoulder_lift_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="shoulder_lift"))
        if not shoulder_lift_records.empty:
            shoulder_lift_records['shoulder_lift_distance'] = shoulder_lift_records['raw_data'].apply(lambda x: x['shoulder_lift_distance'])

            bar_line_plot(x=shoulder_lift_records["test_date"], y=shoulder_lift_records["shoulder_lift_distance"], xaxis_title="تاریخ" ,yaxis_title="فاصله (سانتی متر)", title=" آزمون بالا آوردن شانه")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

with tab3:
    st.subheader("آزمون باز شدن بالا تنه")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("upper_body_opening_tests_form", enter_to_submit=False, clear_on_submit=False, border=True):

            upper_body_opening_distance = st.number_input("باز شدن بالا تنه (سانتی‌متر)", step=0.1, key="upper_body_opening_distance")
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
            selected_time = st.session_state.record_data["date"]

            # Save results
            exercise_data = {
                "upper_body_opening_distance": upper_body_opening_distance,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "upper_body_opening",
                "test_category": "انعطاف پذیری",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="Upper body opening (اکنون)", value=upper_body_opening_distance)
            
            insertRecord(new_record)
    with col2:
        upper_body_opening_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="upper_body_opening"))
        if not upper_body_opening_records.empty:
            upper_body_opening_records['upper_body_opening_distance'] = upper_body_opening_records['raw_data'].apply(lambda x: x['upper_body_opening_distance'])

            bar_line_plot(x=upper_body_opening_records["test_date"], y=upper_body_opening_records["upper_body_opening_distance"], xaxis_title="تاریخ" ,yaxis_title="فاصله (سانتی متر)", title=" آزمون بالا آوردن شانه")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")




with tab4:
    st.subheader("📋 گزارش")
