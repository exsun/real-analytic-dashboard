"stamina - اسقامت"
import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
from persiantools.jdatetime import JalaliDate


tab1, tab2, tab3 = st.tabs(["۶ دقیقه", "Cooper", "📋 گزارش"])

# Initialize session state for VO2Max data if not already set
if "vo2max_data" not in st.session_state:
    st.session_state.vo2max_data = []

# Function to calculate VO2Max for the 6-Minute Test
def calculate_vo2max_6min(distance_km):
    return round(distance_km * 33, 2)

# Function to calculate VO2Max for the Cooper Test
def calculate_vo2max_cooper(distance_km):
    distance_meters = distance_km * 1000
    return round((distance_meters - 504.9) / 44.73, 2)

# Tab 1: 6-Minute Test
with tab1:
    st.subheader("محاسبه VO2Max: 6-Minute Test")
    with st.form("6min_form", clear_on_submit=False):
        distance_6min = st.number_input("مسافت طی شده (کیلومتر)", min_value=0.0, step=0.01, key="distance_6min")
        record_type = st.selectbox("آزمون", options=["pre-test","post-test"])
        submitted_6min = st.form_submit_button("محاسبه")
    
    if submitted_6min and distance_6min > 0:
        vo2max_6min = calculate_vo2max_6min(distance_6min)
        current_time = JalaliDate.to_jalali(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.vo2max_data.append({"تاریخ": current_time, "VO2Max": vo2max_6min, "Test Type": "6-Minute"})
        st.metric(label="VO2Max (اکنون)", value=vo2max_6min)

# Tab 2: Cooper Test
with tab2:
    st.subheader("محاسبه VO2Max: Cooper Test")
    with st.form("cooper_form", clear_on_submit=False):
        distance_cooper = st.number_input("مسافت طی شده (کیلومتر)", min_value=0.0, step=0.01, key="distance_cooper")
        record_type = st.selectbox("آزمون", options=["pre-test","post-test"])
        submitted_cooper = st.form_submit_button("محاسبه")
    
    if submitted_cooper and distance_cooper > 0:
        vo2max_cooper = calculate_vo2max_cooper(distance_cooper)
        current_time = JalaliDate.to_jalali(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.vo2max_data.append({"تاریخ": current_time, "VO2Max": vo2max_cooper, "Test Type": "Cooper"})
        st.metric(label="VO2Max (اکنون)", value=vo2max_cooper)

# Tab 3: History
with tab3:
    st.subheader("📋 تاریخچه")
    if st.session_state.vo2max_data:
        df_data = pd.DataFrame(st.session_state.vo2max_data)
        st.dataframe(df_data)

        # Plot VO2Max data using Plotly
        vo2max_plot = px.bar(
            df_data, 
            x="تاریخ", 
            y="VO2Max", 
            color="Test Type", 
            title="VO2Max تغییرات",
            labels={"تاریخ": "Date", "VO2Max": "VO2Max", "Test Type": "Test Type"}
        )
        st.plotly_chart(vo2max_plot, use_container_width=True)
    else:
        st.info("هنوز داده‌ای ثبت نشده است.")