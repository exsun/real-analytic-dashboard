import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName

def epley_1rm(weight, reps):
    return weight * (1 + reps / 30)

def brzycki_1rm(weight, reps):
    denominator = 1.0278 - 0.0278 * reps
    if denominator <= 0:
        return 0  # Avoid division by zero or negative
    return weight / denominator


def relative_strength_form(athlete_id, athlete_name, athlete_weight, exercise):
        
        with st.form("relative_strength_form", enter_to_submit=False, clear_on_submit=False, border=True):
            st.subheader("تست قدرت نسبی")
            df_data =  []

            
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

            # Calculate 1RM
            if formula == "Epley":
                estimated_1rm = epley_1rm(lift_weight, max_reps)
            else:
                estimated_1rm = brzycki_1rm(lift_weight, max_reps)
                
            submitted = st.form_submit_button("محاسبه")
            
            calculated_data = [(rep_count, perc, round((perc / 100.0) * estimated_1rm, 2)) for rep_count, perc in REP_PERCENTAGE_DATA]
            if submitted:
                with st.spinner('در حال محاسبه ...'):
                    time.sleep(2.5)
                if athlete_name and exercise:
                    estimate_power = round(estimated_1rm / athlete_weight, 2)
                    # current_date = JalaliDate.to_jalali(datetime.datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Tehran"))).strftime("%Y-%m-%d %H:%M:%S")
                    selected_time = record_date
                    exercise_data = {
                        "exercise": exercise,
                        "estimate_power": estimate_power,
                        "estimated_1rm": round(estimated_1rm, 2),
                        "lift_weight": lift_weight,
                        "max_reps": max_reps,
                        "calculated_data": f"{calculated_data}"
                    }
                    # exercise_data = json.dumps(exercise_data)
                    test_result = {
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
                            "Weight (kg)": round((perc / 100.0) * estimated_1rm, 2),
                            "Reps": rep_count
                        })

                    st.session_state.strength_data.append(test_result)

                    st.success(f"قدرت نسبی در حرکت {exercise} با موفقیت ذخیره !")
                    
                    df = pd.DataFrame([exercise_data])

                    st.dataframe(df)

                    st.dataframe(df_data)

                    insertRecord(test_result)

                    # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
                    
                else:
                    st.warning("لطفا فرم را کامل کنید !")
   
   