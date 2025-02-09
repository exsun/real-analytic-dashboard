import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, update_weight
from utils.logical_functions import calculate_performance_decrease, performance_decrease_perc

@st.dialog("تست جدید")
def new_anaerobic_800_200_record(athletes , record_name, category):
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

        with st.form("performance_decrease_form", enter_to_submit=False, clear_on_submit=False, border=True):
            st.subheader("تست افت عملکرد")
            
            time_800m = st.number_input("زمان 800 متر (ثانیه)", min_value=0.0, step=0.1, key="time_800m")
            time_200m = st.number_input("زمان 200 متر (ثانیه)", min_value=0.0, step=0.1, key="time_200m")
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
            
            if submitted and time_800m > 0 and time_200m > 0:
                with st.spinner('در حال محاسبه ...'):
                    time.sleep(2.5)
                if time_800m > 0 and time_200m > 0:
                    performance_decrease = calculate_performance_decrease(time_800m, time_200m)
                    performance_perc = performance_decrease_perc(time_800m, time_200m)
                

                    # Save the results to session state
                
                    exercise_data = {
                        "duration_800m": time_800m,
                        "duration_200m": time_200m,
                        "performance_decrease": performance_decrease,
                        "performance_perc": performance_perc

                    }   
                    new_record = {
                        "athlete_id": int(athlete_id),
                        "raw_data": exercise_data,
                        "test_name": "افت-عملکرد",
                        "test_category": "بی-هوازی",
                        "test_date": record_date,
                        "gregorian_date": gregorian_date
                    }
                    
                    # Display results
                    st.metric(label="افت عملکرد (%)", value=f"{performance_perc}%")
                    st.metric(label="افت عملکرد میزان", value=f"{performance_decrease}%")

                    insertRecord(new_record)
                    
                    st.rerun()


                    # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
                    
                else:
                    st.warning("لطفا فرم را کامل کنید !")

