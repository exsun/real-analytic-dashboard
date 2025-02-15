
import streamlit as st
from utils.database import insertRecord, update_weight
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import time, datetime
from utils.logical_functions import calculate_vo2max_6min, calculate_vo2max_cooper

@st.dialog("تست جدید")
def new_stamina_6min_record(athletes , record_name, category):
    st.title(record_name)
    athlete_name = st.selectbox("ورزشکار", 
        athletes["name"], 
        placeholder="انتخاب کنید",
        index=None
    )
    if athlete_name:
        athlete_weight_value = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""
        athletes['athlete_id'] = athletes['athlete_id'].astype(int)
        athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""

        athlete_weight = st.number_input("وزن",
            value=athlete_weight_value,
            placeholder="انتخاب کنید",
            on_change=update_weight,
            args=(athlete_weight_value,),
            kwargs={"athlete_id": int(athlete_id)},
            step=0.1,
            format="%0.1f",
            key="athlete_weight",
        )
        # st.info(round(st.session_state.athlete_weight, 1))

        with st.container(border=True):
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
            
            record_date = record_date.strftime("%Y-%m-%d")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")

        if st.button("ثبت"):
            with st.spinner('در حال محاسبه ...'):
                time.sleep(2.5)
            vo2max = calculate_vo2max_6min(distance_6min)
            exercise_data = {
                "distance": distance_6min,
                "vo2max": vo2max,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": record_name,
                "test_category": category,
                "test_date": record_date,
                "gregorian_date": gregorian_date,
            }
            st.metric(label="VO2Max (اکنون)", value=vo2max)
            

                    
            if st.button("ذخیره"):
                insertRecord(new_record)
                st.rerun()
                
@st.dialog("تست جدید")
def new_stamina_cooper_record(athletes , record_name, category):
    st.title(record_name)
# User Data
    athlete_name = st.selectbox("ورزشکار", 
        athletes["name"], 
        placeholder="انتخاب کنید",
        index=None
    )
    if athlete_name:
        athlete_weight_value = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""
        athletes['athlete_id'] = athletes['athlete_id'].astype(int)
        athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
        # Update Weight
        athlete_weight = st.number_input("وزن",
            value=athlete_weight_value,
            placeholder="انتخاب کنید",
            on_change=update_weight,
            args=(athlete_weight_value,),
            kwargs={"athlete_id": int(athlete_id)},
            step=0.1,
            format="%0.1f",
            key="athlete_weight",
        )
# Record Input
        with st.container(border=True):
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
# Record Data
        if st.button("محاسبه") and distance_cooper > 0:
            vo2max_cooper = calculate_vo2max_cooper(distance_cooper)
            exercise_data = {
                "distance": distance_cooper,
                "vo2max": vo2max_cooper,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": record_name,
                "test_category": category,
                "test_date": record_date,
                "gregorian_date": gregorian_date,
            }
            st.metric(label="VO2Max (اکنون)", value=vo2max_cooper)
# Insert Data

                    
            if st.button("ذخیره"):
                insertRecord(new_record)
                st.rerun()