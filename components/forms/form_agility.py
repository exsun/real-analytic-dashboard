import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.constants import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, update_weight

@st.dialog("تست جدید")
def new_wrestle_specific_record(athletes , record_name, category):
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
        with st.form("wrestle_specific_form", enter_to_submit=False, clear_on_submit=False, border=True):
            bear_duration = st.number_input("مدت زمان آزمون خرسی (ثانیه)", min_value=1, value=20, step=1, key="bear_duration")
            
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


            submitted = st.form_submit_button("محاسبه")
        
# Record Data
        
        if submitted:
            exercise_data = {
                "bear_duration": bear_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "خرسی",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون خرسی (ثانیه)", value=f"{bear_duration}")
    
# Insert Data
            insertRecord(new_record)

# Rerun Page
            st.rerun()




@st.dialog("تست جدید")
def new_wrestle_bear_record(athletes , record_name, category):
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
        with st.form("wrestle_specific_form", enter_to_submit=False, clear_on_submit=False, border=True):
            wrestle_specific_duration = st.number_input("مدت زمان آزمون چابکی ویژه کشتی (ثانیه)", min_value=1, value=20, step=1, key="wrestle_specific_duration")
            
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


            submitted = st.form_submit_button("محاسبه")
        
# Record Data
        
        if submitted:
            exercise_data = {
                "wrestle_specific_duration": wrestle_specific_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "ویژه-کشتی",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون چابکی ویژه کشتی (ثانیه)", value=f"{wrestle_specific_duration}")
    
# Insert Data
            insertRecord(new_record)

# Rerun Page
            st.rerun()


@st.dialog("تست جدید")
def new_wrestle_zone_record(athletes , record_name, category):
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
        with st.form("wrestle_specific_form", enter_to_submit=False, clear_on_submit=False, border=True):
            zone_duration = st.number_input("مدت زمان آزمون منطقه (ثانیه)", min_value=1, value=20, step=1, key="zone_duration")
            
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


            submitted = st.form_submit_button("محاسبه")
        
# Record Data
        
        if submitted:
            exercise_data = {
                "zone_duration": zone_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "منطقه",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون منطقه (ثانیه)", value=f"{zone_duration}")
    
# Insert Data
            insertRecord(new_record)

# Rerun Page
            st.rerun()


@st.dialog("تست جدید")
def new_wrestle_T_record(athletes , record_name, category):
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
        with st.form("wrestle_specific_form", enter_to_submit=False, clear_on_submit=False, border=True):
            T_duration = st.number_input("مدت زمان آزمون T (ثانیه)", min_value=1, value=20, step=1, key="T_duration")
            
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


            submitted = st.form_submit_button("محاسبه")
        
# Record Data
        
        if submitted:
            exercise_data = {
                "T_duration": T_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "T",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون T (ثانیه)", value=f"{T_duration}")
    
# Insert Data
            insertRecord(new_record)

# Rerun Page
            st.rerun()



@st.dialog("تست جدید")
def new_wrestle_illinois_record(athletes , record_name, category):
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
        with st.form("wrestle_specific_form", enter_to_submit=False, clear_on_submit=False, border=True):
            illinois_duration = st.number_input("مدت زمان آزمون illinois (ثانیه)", min_value=1, value=20, step=1, key="illinois_duration")
            
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

            submitted = st.form_submit_button("محاسبه")
        
# Record Data
        
        if submitted:
            exercise_data = {
                "illinois_duration": illinois_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "illinois",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون illinois (ثانیه)", value=f"{illinois_duration}")
    
# Insert Data
            insertRecord(new_record)

# Rerun Page
            st.rerun()
