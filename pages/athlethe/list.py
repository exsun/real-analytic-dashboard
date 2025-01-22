import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from st_supabase_connection import execute_query
from utils.database import list_athlete, list_athlete_history
from persiantools.jdatetime import JalaliDate
from datetime import datetime

from streamlit_nej_datepicker import datepicker_component, Config
import jdatetime

import numpy as np
from datetime import date, timedelta
import string
import time


def bar_line_plot(x , y, xaxis_title, yaxis_title):
       # Create Bar Plot
        bar_trace = go.Bar(
            x=x,
            y=y,
            name="Bar Plot",
            marker=dict(color='rgb(58, 71, 80)')
        )

        # Create Line Plot
        line_trace = go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name="Line Plot",
            line=dict(color='rgb(255, 100, 100)', width=2)
        )

        # Combine both traces in a single figure
        fig = go.Figure(data=[bar_trace, line_trace])

        # Set layout properties
        fig.update_layout(
            title="Bar Plot with Line Overlay",
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            barmode='group',
            template="plotly_white",
            xaxis=dict(type="category"),
            title_x=0.5,  # Center the title
        )
            

        # Display the plot in Streamlit
        st.plotly_chart(fig)


def strenght_history(results):
    with st.container(border=True):
        st.subheader("تست قدرت")
        # Pre-process
        results['estimate_power'] = results['raw_data'].apply(lambda x: x['estimate_power'])
        results['estimated_1rm'] = results['raw_data'].apply(lambda x: x['estimated_1rm'])
        col1 , col2 = st.columns(2)
        st.dataframe(results,hide_index=True)
        bar_line_plot(x=results["test_date"], y=results["estimate_power"], xaxis_title="تاریخ" ,yaxis_title="قدرت نسبی")

        bar_line_plot(x=results["test_date"], y=results["estimated_1rm"], xaxis_title="تاریخ" ,yaxis_title="یک تکرار بیشینه")


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
        athletes = pd.DataFrame(list_athlete())
        athlete_name = st.selectbox("ورزشکار", 
                        athletes["name"], 
                        placeholder="انتخاب کنید"
        )

        athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
        # print("result",list_athlete_history(athlete_id))
        results = pd.DataFrame(list_athlete_history(athlete_id)).sort_values(by='test_date')  
        # print(results)
        # results["timestamp"] = pd.to_datetime(results["gregorian_date"])
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