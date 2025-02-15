import streamlit as st
import datetime
import time
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import pandas as pd
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, update_weight
from utils.logical_functions import calculate_performance_decrease, performance_decrease_perc
from components.constants import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA

# Function to calculate performance decrease
def calculate_performance_decrease(time_800m, time_200m):
    if time_800m > 0 and time_200m > 0:
        decrease = (time_800m / 4) - time_200m
        return round(decrease, 2)
    return None

# Function to calculate RAST power
def calculate_power(body_mass, distance, time):
    if time > 0:
        return round((body_mass * (distance**2)) / (time**3), 2)
    return 0

# Function to calculate fatigue index for RAST
def rast_fatigue_index(peak_power, lowest_power, sprint_times):
    if peak_power > 0:
        return round(((peak_power - lowest_power) / sum(sprint_times)) , 2)
    return 0
def wingate_fatigue_index(peak_power, lowest_power):
    if peak_power > 0:
        return round(((peak_power - lowest_power) / peak_power) * 100 , 2)
    return 0

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

                    
                    if st.button("ذخیره"):
                        insertRecord(new_record)
                        st.rerun()

                    # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
                    
                else:
                    st.warning("لطفا فرم را کامل کنید !")

@st.dialog("تست جدید")

def new_anaerobic_rast_record(athletes , record_name, category):
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

        with st.form("rast_form", enter_to_submit=False, clear_on_submit=False, border=True):
            st.subheader("تست افت عملکرد")
            
            distance = 35  # Fixed distance for RAST
            row1 = st.columns(3)
            row2 = st.columns(3)

            sprint_times = [col.number_input(f"زمان {(row1 + row2).index(col) + 1} (ثانیه)", min_value=10.0, step=0.1, key=f"sprint_{(row1 + row2).index(col) + 1}") for col in row1 + row2]
            

           
            day , month, year= st.columns(3)
            with year:
                years = list(range(JalaliDate.today().year+1, 1390, -1))
                selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year) , key="rast-year")
            with month:
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
                selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1 , key="rast-month")
            with day:
                days = list(range(1, 32))
                selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1 , key="rast-day")
            selected_time = st.time_input("زمان", datetime.time(8, 45))

            record_date = JalaliDateTime(selected_year, months.index(selected_month) + 1, selected_day, locale="en")
            gregorian_date = record_date.to_gregorian()
            
            record_date = record_date.strftime("%Y-%m-%d") + " " + selected_time.strftime("%H:%M:%S")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")  + " " + selected_time.strftime("%H:%M:%S")

            submitted = st.form_submit_button("محاسبه")
            
        if submitted:
            # Calculate power for each sprint
            sprint_powers = [calculate_power(athlete_weight, distance, t) for t in sprint_times]
            total_power = round(sum(sprint_powers),2)  # Total Anaerobic Power
            average_power = round(total_power / 6, 2) if total_power > 0 else 0
            peak_power = round(max(sprint_powers),2)  # Peak Power
            lowest_power = round(min(sprint_powers),2)   # Lowest Power
            fatigue_index = rast_fatigue_index(peak_power, lowest_power, sprint_times)
            
            # Current time for storage
            current_time = datetime.datetime.now()
            
            # Save results to session state
     
            sprint_powers_data = [{                
                **{f"sprint_{i+1}": {
                    "time": sprint_times[i],
                    "power": sprint_powers[i]

                    } for i in range(len(sprint_times))}
                }]
            
            exercise_data = {
                "total_power": total_power,
                "average_power": average_power,
                "peak_power": peak_power,
                "lowest_power": lowest_power,
                "fatigue_index": fatigue_index,
                "sprint_powers": sprint_powers_data


            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "RAST",
                "test_category": "بی-هوازی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }


            metrics = st.columns(4)
            metrics[0].metric(label="توان اوج (W)", value=f"{peak_power} W")
            metrics[1].metric(label="توان میانگین (W)", value=f"{average_power} W")
            metrics[2].metric(label="شاخص خستگی (%)", value=f"{fatigue_index}%")
            metrics[3].metric(label="توان بی‌هوازی کل (W)", value=f"{total_power} W")

                    
            if st.button("ذخیره"):
                insertRecord(new_record)
                st.rerun()


            # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
            
        else:
            st.warning("لطفا فرم را کامل کنید !")



@st.dialog("تست جدید")

def new_anaerobic_wingate_record(athletes , record_name, category):
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

        with st.form("wingate_form", enter_to_submit=False, clear_on_submit=False, border=True):
            peak_power = st.number_input("توان اوج (وات)", min_value=0.1, step=0.1, key="peak_power")
            lowest_power = st.number_input("توان حداقل (وات)", min_value=0.1, step=0.1, key="lowest_power")
            duration = st.number_input("مدت زمان آزمون (ثانیه)", min_value=1, step=1, value=30, key="duration")  # Default 30 seconds
            
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

            submitted = st.form_submit_button("محاسبه")
            
        if submitted:
            if peak_power > 0 and lowest_power > 0 and duration > 0:
                # Calculate metrics
                fatigue_index = wingate_fatigue_index(peak_power, lowest_power)
                average_power = round((peak_power + lowest_power) / 2 , 2)  # Simplified average power calculation
                total_power = round(average_power * duration, 2)
               
                exercise_data = {
                    "total_power": total_power,
                    "average_power": average_power,
                    "peak_power": peak_power,
                    "lowest_power": lowest_power,
                    "fatigue_index": fatigue_index,
                }       
                new_record = {
                    "athlete_id": int(athlete_id),
                    "raw_data": exercise_data,
                    "test_name": "wingate",
                    "test_category": "بی-هوازی",
                    "test_date": record_date,
                    "gregorian_date": gregorian_date
                }

                metrics = st.columns(4)
                # Display metrics
                metrics[0].metric(label="توان اوج (W)", value=f"{peak_power} W")
                metrics[1].metric(label="توان میانگین (W)", value=f"{average_power} W")
                metrics[2].metric(label="شاخص خستگی (%)", value=f"{fatigue_index}%")
                metrics[3].metric(label="توان بی‌هوازی کل (W)", value=f"{total_power} W")


                    
                if st.button("ذخیره"):
                    insertRecord(new_record)
                    st.rerun()

            # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
            
        else:
            st.warning("لطفا فرم را کامل کنید !")





@st.dialog("تست جدید")

def new_anaerobic_burpee_record(athletes , record_name, category):
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

        with st.form("burpee_form", enter_to_submit=False, clear_on_submit=False, border=True):
            burpee_count = st.number_input("تعداد کل بورپی", min_value=1, step=1, key="burpee_count")
            duration = st.number_input("مدت زمان آزمون (ثانیه)", min_value=1, value=45, step=1, key="burpee_duration")
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

            submitted = st.form_submit_button("محاسبه")
            
        if submitted:
            exercise_data = {
                "burpee_count": burpee_count,
                "duration": duration,
            } 

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "burpee",
                "test_category": "بی-هوازی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
            
            # Display metrics
            st.metric(label="تعداد کل بورپی", value=burpee_count)

            
            if st.button("ذخیره"):
                insertRecord(new_record)
                st.rerun()


            # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
            
        else:
            st.warning("لطفا فرم را کامل کنید !")
