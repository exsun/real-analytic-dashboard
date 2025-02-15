import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.constants import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, update_weight

def epley_1rm(weight, reps):
    return weight * (1 + reps / 30)

def brzycki_1rm(weight, reps):
    denominator = 1.0278 - 0.0278 * reps
    if denominator <= 0:
        return 0  # Avoid division by zero or negative
    return weight / denominator

@st.dialog("تست جدید")
def new_strength_relative_strength_record(athletes , record_name, category):
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
            df_data =  []

            exercise = st.selectbox("نام حرکت:",
                            options=EXERCISE_OPTIONS ,
                            placeholder="انتخاب کنید",
                            index=None,
                            key=f"exercise"
                            )
            lift_weight = st.number_input("وزن ورنه بلند شده:", 
                                    min_value=0.0,
                                    placeholder="انتخاب کنید",
                                    step=2.5,
                                    value=80.0)
            max_reps = st.number_input("تعداد تکرار تا مرز خستگی:", min_value=1, value=8)
            
            formula = st.selectbox("فرمول محاسبه:",("Brzycki", "Epley"))
            
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

# Record Data

            # Calculate 1RM
            if formula == "Epley":
                one_repetition_maximum = epley_1rm(lift_weight, max_reps)
            else:
                one_repetition_maximum = brzycki_1rm(lift_weight, max_reps)
                
            calculated_data = [(rep_count, perc, round((perc / 100.0) * one_repetition_maximum, 2)) for rep_count, perc in REP_PERCENTAGE_DATA]

        if st.button("محاسبه") and exercise:
            with st.spinner('در حال محاسبه ...'):
                time.sleep(2.5)
            if athlete_name and exercise:
                relative_strength = round(one_repetition_maximum / athlete_weight, 2)
                # current_date = JalaliDate.to_jalali(datetime.datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Tehran"))).strftime("%Y-%m-%d %H:%M:%S")
                selected_time = record_date
                exercise_data = {
                    "exercise": exercise,
                    "relative_strength": relative_strength,
                    "one_repetition_maximum": round(one_repetition_maximum, 2),
                    "lift_weight": lift_weight,
                    "max_reps": max_reps,
                    "calculated_data": f"{calculated_data}"
                }

                new_record = {
                    "athlete_id": int(athlete_id),
                    "raw_data": exercise_data,
                    "test_name": "قدرت نسبی",
                    "test_category": "قدرت",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }
        
                for rep_count, perc in REP_PERCENTAGE_DATA:

                    df_data.append({
                        "% of 1RM": f"{perc}%",
                        "Weight (kg)": round((perc / 100.0) * one_repetition_maximum, 2),
                        "Reps": rep_count
                    })


                st.success(f"قدرت نسبی در حرکت {exercise} با موفقیت ذخیره !")
                
                df = pd.DataFrame([exercise_data])

                st.dataframe(df)

                st.dataframe(df_data)

# Insert Data

                    
                insertRecord(new_record)
                st.rerun()