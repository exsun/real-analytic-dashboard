"strength - قدرت"
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import jdatetime
import plotly.graph_objects as go
import time
import json
import pytz
from zoneinfo import ZoneInfo
from utils.database import listAthletes, listAthletesHistory, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from components.charts import bar_line_plot

# Main Content with Tabs
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 1

if 'strength_data' not in st.session_state:
    st.session_state.strength_data = []

# A reference list of (Reps, Percentage) pairs down to ~35%.

def epley_1rm(weight, reps):
    return weight * (1 + reps / 30)

def brzycki_1rm(weight, reps):
    denominator = 1.0278 - 0.0278 * reps
    if denominator <= 0:
        return 0  # Avoid division by zero or negative
    return weight / denominator

st.header("قدرت")
athletes = pd.DataFrame(listAthletes())
athlete_name = st.selectbox("ورزشکار", 
    athletes["name"], 
    placeholder="انتخاب کنید",
)
athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

tab1, tab2 = st.tabs(["قدرت نسبی",  "📋 گزارش"])
with tab1:
# Tab 1: Metrics Visualization
    exercise = st.selectbox("نام حرکت:",
                            options=EXERCISE_OPTIONS ,
                            placeholder="انتخاب کنید",
                            index=None,
                            key=f"exercise"
                            )
    col1, col2 = st.columns(2)
    with col1:
        with st.form("strength_form", enter_to_submit=False, clear_on_submit=False, border=True):
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
                    current_date = JalaliDate.to_jalali(datetime.datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Tehran"))).strftime("%Y-%m-%d %H:%M:%S")
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
                    print(record_date.strftime("%Y-%m-%d") + jdatetime.datetime.now().strftime("%H:%M:%S"))
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
                    # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
                    
                    insertRecord(test_result)
                else:
                    st.warning("لطفا فرم را کامل کنید !")
    with col2:
        strength_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="قدرت نسبی"))
        strength_records['estimate_power'] = strength_records['raw_data'].apply(lambda x: x['estimate_power'])
        strength_records['estimated_1rm'] = strength_records['raw_data'].apply(lambda x: x['estimated_1rm'])

        strength_records['exercise'] = strength_records['raw_data'].apply(lambda x: x['exercise'])
        strength_records = strength_records[strength_records['exercise'] == exercise]
        if not strength_records.empty:
            bar_line_plot(x=strength_records["test_date"], y=strength_records["estimate_power"], xaxis_title="تاریخ" ,yaxis_title="قدرت نسبی", title="estimate_power records")
            bar_line_plot(x=strength_records["test_date"], y=strength_records["estimated_1rm"], xaxis_title="تاریخ" ,yaxis_title="یک تکرار بیشینه", title="estimated_1rm records")

        else:
            st.info("هنوز داده‌ای ثبت نشده است.")


# Tab 3: History
with tab2:
    st.subheader("📋 گزارش")
    if not strength_records.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(strength_records)
        with col2:
            bar_line_plot(x=strength_records["test_date"], y=strength_records["estimate_power"], xaxis_title="تاریخ" ,yaxis_title="قدرت نسبی", title="قدرت نسبی")
    else:
        st.info("هنوز داده‌ای ثبت نشده است.")

    if not strength_records.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(strength_records)
        with col2:
            bar_line_plot(x=strength_records["test_date"], y=strength_records["estimated_1rm"], xaxis_title="تاریخ" ,yaxis_title="یک تکرار بیشینه", title="یک تکرار بیشینه")
    else:
        st.info("هنوز داده‌ای ثبت نشده است.")

