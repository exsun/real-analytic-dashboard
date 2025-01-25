import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from st_supabase_connection import execute_query
from utils.database import listAthletes, listAthletesHistory, listAthleteRecordsByCategory
from persiantools.jdatetime import JalaliDate
from datetime import datetime

from streamlit_nej_datepicker import datepicker_component, Config
import jdatetime

import numpy as np
from datetime import date, timedelta
import string
import time
from components.charts import bar_line_plot


def strenght_history(results):
    with st.container(border=True):
        st.subheader("تست قدرت")
        # Pre-process
        results['estimate_power'] = results['raw_data'].apply(lambda x: x['estimate_power'])
        results['estimated_1rm'] = results['raw_data'].apply(lambda x: x['estimated_1rm'])
        col1 , col2 = st.columns(2)
        st.dataframe(results,hide_index=True)
        bar_line_plot(x=results["test_date"], y=results["estimate_power"], xaxis_title="تاریخ" ,yaxis_title="قدرت نسبی", title="estimate_power records")


        bar_line_plot(x=results["test_date"], y=results["estimated_1rm"], xaxis_title="تاریخ" ,yaxis_title="یک تکرار بیشینه", title="estimated_1rm records")


@st.fragment
def show_athlete_results():

    col1 , col2 = st.columns([4,2])
    with col2:
    
        config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                        color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                        should_highlight_weekends=True, always_open=True,
                        )

        record_date = datepicker_component(config=config)
        st.session_state.record_data["record_date_range"] = record_date


    st.session_state.record_data["change"] = False
    with col1:
        athletes = pd.DataFrame(listAthletes())
        athlete_name = st.selectbox("ورزشکار", 
                        athletes["name"], 
                        placeholder="انتخاب کنید"
        )

        athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
        results = pd.DataFrame(listAthleteRecordsByCategory(athlete_id, category="قدرت"))

        results["date"] = pd.to_datetime(results["gregorian_date"])

        athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

        st.session_state.record_data["athlete_name"] = athlete_name
        st.session_state.record_data["athlete_weight"] = athlete_weight
        st.session_state.record_data["athlete_id"] = athlete_id

        # print("gregorian_date",pd.to_datetime(results['gregorian_date']))
        # print("from",pd.to_datetime(st.session_state.record_data["record_date_range"]['from'].togregorian()))
        if st.session_state.record_data["record_date_range"] and st.session_state.record_data["record_date_range"]['to']:
            results = results[(results['date'] >= pd.to_datetime(st.session_state.record_data["record_date_range"]['from'].togregorian())) 
                                & 
                            (results['date'] <= pd.to_datetime(st.session_state.record_data["record_date_range"]['to'].togregorian()))
                            ]
        # print(results[results.test_category == "قدرت"])
        strenght_history(results[results.test_category == "قدرت"])
        

    # st.subheader(f"تاریخ منتخب از {record_date['from']:%y/%m/%d} تا {record_date['to']:%y/%m/%d}")






show_athlete_results()

st.write(st.session_state.record_data["athlete_id"])







# data_editor_df = df[["weight", "age", "height","name"]]

# st.data_editor(
#     data_editor_df,
#     column_config={
#         "name": st.column_config.TextColumn(
#             "نام و نام خانوادگی",
#             help="نام ورزشکاران",
#             default="st.",
#             max_chars=50,
#             validate=r"^st\.[a-z_]+$",
#         ),
#         "age": st.column_config.NumberColumn(
#             "سن",
#             min_value=16,
#             max_value=32,
#             help="سن ورزشکاران",
#             step=1,
#             format="%d"
#         ),
#         "weight": st.column_config.NumberColumn(
#             "وزن",
#             min_value=50.0,
#             max_value=130.0,
#             help="وزن ورزشکاران",
#             step=0.1,
#             format="%.2f"
#         ),
#         "height": st.column_config.NumberColumn(
#             "قد",
#             min_value=50.0,
#             max_value=130.0,
#             help="قد ورزشکاران",
#             step=1
#         )
        
#     },
#     hide_index=True,
# )


# st.session_state.record_data["date"] = record_date
# st.session_state.record_data["athlete_name"] = athlete_name