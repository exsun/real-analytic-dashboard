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
from utils.database import listAthletes, insertRecord, listAthleteRecordsByCategory, listAthleteRecordsByCategoryByName, listAthleteRecordsByName
from components.charts import bar_line_plot
from components.forms.form_strength import relative_strength_form

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
athletes['athlete_id'] = athletes['athlete_id'].astype(int)



tab1, tab2 = st.tabs(["قدرت نسبی",  "📋 گزارش"])
with tab1:


# Tab 1: Metrics Visualization

    col1, col2 = st.columns(2)
    with col1:

        exercise = st.selectbox("نام حرکت:",
                        options=EXERCISE_OPTIONS ,
                        placeholder="انتخاب کنید",
                        index=None,
                        key=f"exercise"
                        )
        relative_strength_form(athlete_id, athlete_name, athlete_weight, exercise)
   
    with col2:
        strength_records = pd.DataFrame(listAthleteRecordsByName(athlete_id, test_name="قدرت نسبی"))
        if not strength_records.empty:
            strength_records['estimate_power'] = strength_records['raw_data'].apply(lambda x: x['estimate_power'])
            strength_records['estimated_1rm'] = strength_records['raw_data'].apply(lambda x: x['estimated_1rm'])

            strength_records['exercise'] = strength_records['raw_data'].apply(lambda x: x['exercise'])
            strength_records = strength_records[strength_records['exercise'] == exercise]
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

