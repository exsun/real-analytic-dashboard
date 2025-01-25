"anaerobic - بی هوازی"
import streamlit as st
import pandas as pd
from persiantools.jdatetime import JalaliDate
import datetime
from utils.database import listAthletes, listAthletesHistory, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from components.charts import bar_line_plot
import json
# Initialize session state for storing test results
if "anaerobic_test_data" not in st.session_state:
    st.session_state.anaerobic_test_data = []

def gregorian_to_jalali(gregorian_date):
    return JalaliDate.to_jalali(gregorian_date).strftime("%Y-%m-%d")

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
def calculate_fatigue_index(max_power, min_power):
    if max_power > 0:
        return round(((max_power - min_power) / max_power) * 100, 2)
    return 0

def performance_decrease_perc(time_800m, time_200m):
    if time_800m > 0 and time_200m > 0:
        decrease = ((time_800m - (time_200m * 4)) / time_800m)
        return round(decrease, 2) * 100
  
st.header("بی هوازی")

athletes = pd.DataFrame(listAthletes())
athlete_name = st.selectbox("ورزشکار", 
    athletes["name"], 
    placeholder="انتخاب کنید",
)
athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

# Tabs for different functionalities
tab1, tab2, tab3, tab4 , tab5 = st.tabs(["افت عملکرد", "RAST", "wingate", "Burpee", "📋 گزارش"])

# Tab 1: Anaerobic Test Input
with tab1:
    st.subheader("محاسبه کاهش عملکرد: آزمون بی‌هوازی (800m-200m)")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("anaerobic_form", clear_on_submit=False):
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
        
        if submitted:
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
                insertRecord(new_record)

            else:
                st.error("لطفاً مقادیر معتبر وارد کنید.")

    with col2:
        performance_decrease_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="افت-عملکرد"))
        if not performance_decrease_records.empty:
            performance_decrease_records['performance_decrease'] = performance_decrease_records['raw_data'].apply(lambda x: x['performance_decrease'])

            bar_line_plot(x=performance_decrease_records["test_date"], y=performance_decrease_records["performance_decrease"], xaxis_title="تاریخ" ,yaxis_title="افت عملکرد", title="میزان افت عملکرد")

            
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

# Tab 2: RAST Test
with tab2:
    st.subheader("آزمون RAST")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("rast_form", clear_on_submit=False):
            distance = 35  # Fixed distance for RAST
            row1 = st.columns(3)
            row2 = st.columns(3)

            sprint_times = [col.number_input(f"زمان {(row1 + row2).index(col) + 1} (ثانیه)", min_value=0.1, step=0.01, key=f"sprint_{(row1 + row2).index(col) + 1}") for col in row1 + row2]
            

           
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
            max_power = round(max(sprint_powers),2)  # Peak Power
            min_power = round(min(sprint_powers),2)   # Lowest Power
            fatigue_index = calculate_fatigue_index(max_power, min_power)
            
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
                "max_power": max_power,
                "min_power": min_power,
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


            # Display metrics
            metrics = st.columns(4)
            metrics[0].metric(label="توان اوج (W)", value=f"{max_power} W")
            metrics[1].metric(label="توان میانگین (W)", value=f"{average_power} W")
            metrics[2].metric(label="شاخص خستگی (%)", value=f"{fatigue_index}%")
            metrics[3].metric(label="توان بی‌هوازی کل (W)", value=f"{total_power} W")
            st.dataframe(exercise_data)
            st.dataframe(sprint_powers_data[0])
            print(sprint_powers_data[0])

            insertRecord(new_record)
    with col2:
        rast_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="RAST"))
        if not rast_records.empty:
            rast_records['total_power'] = rast_records['raw_data'].apply(lambda x: x['total_power'])
            rast_records['average_power'] = rast_records['raw_data'].apply(lambda x: x['average_power'])
            rast_records['max_power'] = rast_records['raw_data'].apply(lambda x: x['max_power'])
            rast_records['fatigue_index'] = rast_records['raw_data'].apply(lambda x: x['fatigue_index'])

            # print(rast_records['sprint_powers'][0])
            # sprint_powers = pd.DataFrame(rast_records['sprint_powers'][0]).transpose()
            # print(sprint_powers['time'])
            bar_line_plot(x=rast_records["test_date"], y=rast_records['max_power'], xaxis_title="تاریخ" ,yaxis_title="توان اوج", title="توان اوج (W)")
            bar_line_plot(x=rast_records["test_date"], y=rast_records['average_power'], xaxis_title="تاریخ" ,yaxis_title="توان میانگین", title="توان میانگین (W)")
            bar_line_plot(x=rast_records["test_date"], y=rast_records['total_power'], xaxis_title="تاریخ" ,yaxis_title="توان بی هوازی", title="توان بی هوازی (W)")
            bar_line_plot(x=rast_records["test_date"], y=rast_records['fatigue_index'], xaxis_title="تاریخ" ,yaxis_title="شاخص خستگی", title="شاخص خستگی (%)")


        else:
            st.info("هنوز داده‌ای ثبت نشده است.")


# Tab 3: Wingate Test
with tab3:
    st.subheader("آزمون وینگیت")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("wingate_form", clear_on_submit=False, enter_to_submit=False):
            peak_power = st.number_input("توان اوج (وات)", min_value=0.1, step=0.1, key="peak_power")
            min_power = st.number_input("توان حداقل (وات)", min_value=0.1, step=0.1, key="min_power")
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
            if peak_power > 0 and min_power > 0 and duration > 0:
                # Calculate metrics
                fatigue_index = calculate_fatigue_index(peak_power, min_power)
                average_power = round((peak_power + min_power) / 2 , 2)  # Simplified average power calculation
                total_power = round(average_power * duration, 2)
               
                exercise_data = {
                    "total_power": total_power,
                    "average_power": average_power,
                    "max_power": peak_power,
                    "min_power": min_power,
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

                insertRecord(new_record)

    with col2:
        wingate_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="wingate"))
        if not wingate_records.empty:
            wingate_records['total_power'] = wingate_records['raw_data'].apply(lambda x: x['total_power'])
            wingate_records['average_power'] = wingate_records['raw_data'].apply(lambda x: x['average_power'])
            wingate_records['max_power'] = wingate_records['raw_data'].apply(lambda x: x['max_power'])
            wingate_records['fatigue_index'] = wingate_records['raw_data'].apply(lambda x: x['fatigue_index'])

            bar_line_plot(x=wingate_records["test_date"], y=wingate_records['max_power'], xaxis_title="تاریخ" ,yaxis_title="توان اوج", title="توان اوج (W) wingate")
            bar_line_plot(x=wingate_records["test_date"], y=wingate_records['average_power'], xaxis_title="تاریخ" ,yaxis_title="توان میانگین", title="توان میانگین (W) wingate")
            bar_line_plot(x=wingate_records["test_date"], y=wingate_records['total_power'], xaxis_title="تاریخ" ,yaxis_title="توان بی هوازی", title="توان بی هوازی (W) wingate")
            bar_line_plot(x=wingate_records["test_date"], y=wingate_records['fatigue_index'], xaxis_title="تاریخ" ,yaxis_title="شاخص خستگی", title="شاخص خستگی (%) wingate")


        else:
            st.info("هنوز داده‌ای ثبت نشده است.")


# Tab 4: Burpee Test
with tab4:
    st.subheader("آزمون بورپی")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("burpee_form", clear_on_submit=False, enter_to_submit=False):
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
            insertRecord(new_record)

    with col2:
        burpee_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="burpee"))
        if not burpee_records.empty:
            burpee_records['burpee_count'] = burpee_records['raw_data'].apply(lambda x: x['burpee_count'])

            bar_line_plot(x=burpee_records["test_date"], y=burpee_records["burpee_count"], xaxis_title="تاریخ" ,yaxis_title="burpee", title="تعداد برپی ها")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")
# Tab 5: History
with tab5:
    st.subheader("📋 تاریخچه آزمون‌های بی‌هوازی")

