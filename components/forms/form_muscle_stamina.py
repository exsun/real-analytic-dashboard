import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.constants import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, update_weight

@st.dialog("تست جدید")
def situp_form(athletes , record_name, category):
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
        with st.form("situp_form", enter_to_submit=False, clear_on_submit=False, border=True):
       
            situp_reps = st.number_input("تعداد دراز و نشست (در یک دقیقه)", min_value=0, step=1, key="situp_reps")
            medicine_ball_weight = st.number_input("وزن توپ مدیسن بال", min_value=0, step=1, key="medicine_ball")
            
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
                    "medicine_ball_weight": medicine_ball_weight
                }

                new_record = {
                    "athlete_id": int(athlete_id),
                    "raw_data": exercise_data,
                    "test_name": "دراز-نشست",
                    "test_category": "استقامت-عضلانی",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }

# Insert Data

                    
                insertRecord(new_record)
                    
                st.rerun()


@st.dialog("تست جدید")
def pullup_form(athletes , record_name, category):
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
        with st.form("situp_form", enter_to_submit=False, clear_on_submit=False, border=True):
                   
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
                    "test_name": "بارفیکس",
                    "test_category": "استقامت-عضلانی",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }
# Insert Data

                    
                insertRecord(new_record)
                    
                st.rerun()


@st.dialog("تست جدید")
def dip_parallel_form(athletes , record_name, category):
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
                    "test_name": "دیپ-پارالل",
                    "test_category": "استقامت-عضلانی",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }

# Insert Data

                    
                insertRecord(new_record)
                    
                st.rerun()
