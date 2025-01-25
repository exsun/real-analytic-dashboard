"agility - چابکی"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
import datetime
from utils.database import listAthletes, listAthletesHistory, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import time
from components.charts import bar_line_plot

# Initialize session state for storing test results
if "agility_test_data" not in st.session_state:
    st.session_state.agility_test_data = []
athletes = pd.DataFrame(listAthletes())
athlete_name = st.selectbox("ورزشکار", 
    athletes["name"], 
    placeholder="انتخاب کنید",
)
athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["آزمون چابکی ویژه کشتی", "آزمون خرسی","آزمون منطقه", "آزمون T", "آزمون illinois",  "📋 گزارش"])

# Tab 1: Zone Agility Test
with tab1:
    st.subheader("آزمون چابکی ویژه کشتی")
  
    col1, col2 = st.columns(2)
    with col1:
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
        
        if submitted:
            exercise_data = {
                "wrestle_specific_duration": wrestle_specific_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "wrestle_specific",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون چابکی ویژه کشتی (ثانیه)", value=f"{wrestle_specific_duration}")
    
            insertRecord(new_record)

    with col2:
        wrestle_specific_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="wrestle_specific"))
        if not wrestle_specific_records.empty:
            wrestle_specific_records['wrestle_specific_duration'] = wrestle_specific_records['raw_data'].apply(lambda x: x['wrestle_specific_duration'])

            bar_line_plot(x=wrestle_specific_records["test_date"], y=wrestle_specific_records["wrestle_specific_duration"], xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون چابکی ویژه کشتی (ثانیه)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")
with tab2:
    st.subheader("آزمون خرسی")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("bear_form", enter_to_submit=False, clear_on_submit=False, border=True):
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
        
        if submitted:
            exercise_data = {
                "bear_duration": bear_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "bear",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون خرسی (ثانیه)", value=f"{bear_duration}")
    
            insertRecord(new_record)

    with col2:
        bear_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="bear"))
        if not bear_records.empty:
            bear_records['bear_duration'] = bear_records['raw_data'].apply(lambda x: x['bear_duration'])

            bar_line_plot(x=bear_records["test_date"], y=bear_records["bear_duration"], xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون خرسی (ثانیه)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

with tab3:
    st.subheader("آزمون منطقه")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("zone_form", enter_to_submit=False, clear_on_submit=False, border=True):
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
        
        if submitted:
            exercise_data = {
                "zone_duration": zone_duration,
            }

            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "zone",
                "test_category": "چابکی",
                "test_date": record_date,
                "gregorian_date": gregorian_date
            }
        
            st.metric(label="آزمون منطقه (ثانیه)", value=f"{zone_duration}")
    
            insertRecord(new_record)

    with col2:
        zone_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="zone"))
        if not zone_records.empty:
            zone_records['zone_duration'] = zone_records['raw_data'].apply(lambda x: x['zone_duration'])

            bar_line_plot(x=zone_records["test_date"], y=zone_records["zone_duration"], xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون منطقه (ثانیه)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")
with tab4:
    st.subheader("آزمون T")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("T_form", enter_to_submit=False, clear_on_submit=False, border=True):
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
    
            insertRecord(new_record)

    with col2:
        T_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="T"))
        if not T_records.empty:
            T_records['T_duration'] = T_records['raw_data'].apply(lambda x: x['T_duration'])

            bar_line_plot(x=T_records["test_date"], y=T_records["T_duration"], xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون T (ثانیه)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

with tab5:
    st.subheader("آزمون illinois")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("illinois_form", enter_to_submit=False, clear_on_submit=False, border=True):
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
    
            insertRecord(new_record)

    with col2:
        illinois_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="illinois"))
        if not illinois_records.empty:
            illinois_records['illinois_duration'] = illinois_records['raw_data'].apply(lambda x: x['illinois_duration'])

            bar_line_plot(x=illinois_records["test_date"], y=illinois_records["illinois_duration"], xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون illinois (ثانیه)")
        else:
            st.info("هنوز داده‌ای ثبت نشده است.")

with tab6:
    st.subheader("📋 گزارش")
    # if st.session_state.agility_test_data:
    #     df_history = pd.DataFrame(st.session_state.agility_test_data).sort_values(by="تاریخ")

    #     # Convert Gregorian to Jalali for display

    #     # Melt the DataFrame for combining metrics
    #     melted_df = pd.melt(
    #         df_history,
    #         id_vars=["تاریخ"],
    #         value_vars=["specefic_duration", "bear_duration", "zone_duration", "T_duration", "illinois_duration"],
    #         var_name="Duration Type",
    #         value_name="Duration (seconds)"
    #     )

    #     # Create Grouped Bar Plot
    #     plot = px.bar(
    #         melted_df,
    #         x="تاریخ",
    #         y="Duration (seconds)",
    #         color="Duration Type",
    #         barmode="group",
    #         title="تغییرات زمانی در آزمون‌های چابکی",
    #         labels={"تاریخ": "تاریخ", "Duration (seconds)": "مدت زمان (ثانیه)", "Duration Type": "نوع آزمون"}
    #     )

    #     plot.update_layout(
    #         xaxis=dict(type="category"),
    #         title_x=0.5,  # Center the title
    #     )

    #     # Display the Bar Plot
    #     st.plotly_chart(plot, use_container_width=True)
    #     st.dataframe(df_history)

    # else:
    #     st.info("هنوز داده‌ای ثبت نشده است.")
