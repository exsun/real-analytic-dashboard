import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.constants import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, update_weight


@st.dialog("تست جدید")
def sit_reach_form(athletes , record_name, category):
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
        with st.form("sit_reach_form", enter_to_submit=False, clear_on_submit=False, border=True):
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
                "test_name": "sit&reach",
                "test_category": "انعطاف پذیری",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="sit_reach (اکنون)", value=sit_reach_distance)
            
# Insert Data
                    
            insertRecord(new_record)

            st.rerun()



@st.dialog("تست جدید")
def shoulder_lift_form(athletes , record_name, category):
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
        with st.form("sit_reach_form", enter_to_submit=False, clear_on_submit=False, border=True):
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

            # Save results
            exercise_data = {
                "shoulder_lift_distance": shoulder_lift_distance,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "بالا-آوردن-شانه",
                "test_category": "انعطاف پذیری",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="shoulder_lift (اکنون)", value=shoulder_lift_distance)
            
# Insert Data

                    
            insertRecord(new_record)
                
            st.rerun()


@st.dialog("تست جدید")
def upper_body_opening_form(athletes , record_name, category):
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
        with st.form("sit_reach_form", enter_to_submit=False, clear_on_submit=False, border=True):

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

            # Save results
            exercise_data = {
                "upper_body_opening_distance": upper_body_opening_distance,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "باز-شدن-بالا-تنه",
                "test_category": "انعطاف پذیری",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            st.metric(label="Upper body opening (اکنون)", value=upper_body_opening_distance)
            
# Insert Data

                    
            insertRecord(new_record)
                
            st.rerun()