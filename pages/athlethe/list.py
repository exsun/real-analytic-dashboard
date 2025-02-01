import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from st_supabase_connection import execute_query
from utils.database import (
    listAthletes, 
    getAthleteByName,
    listAthleteRecords, 
    listAthletesWithHistory, 
    listAthletesRecordsByName,
    listAthleteRecordsByCategory,
    FilterRecordsByAthleteId
    )

from persiantools.jdatetime import JalaliDate
from datetime import datetime

from streamlit_nej_datepicker import datepicker_component, Config
import jdatetime

import numpy as np
from datetime import date, timedelta
import string
import time
from components.charts import bar_line_plot, multi_bar_line_plot
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA


# def strenght_history(results):
#     with st.container(border=True):
#         st.subheader("تست قدرت")
#         # Pre-process
#         results['estimate_power'] = results['raw_data'].apply(lambda x: x['estimate_power'])
#         results['estimated_1rm'] = results['raw_data'].apply(lambda x: x['estimated_1rm'])
#         col1 , col2 = st.columns(2)
#         st.dataframe(results,hide_index=True)
#         bar_line_plot(x=results["test_date"], y=results["estimate_power"], xaxis_title="تاریخ" ,yaxis_title="قدرت نسبی", title="estimate_power records")


#         bar_line_plot(x=results["test_date"], y=results["estimated_1rm"], xaxis_title="تاریخ" ,yaxis_title="یک تکرار بیشینه", title="estimated_1rm records")


# @st.fragment
# def show_athlete_results():

#     col1 , col2 = st.columns([4,2])
#     with col2:
    
#         config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
#                         color_primary_light="#ff9494", selection_mode="range",closed_view="button",
#                         should_highlight_weekends=True, always_open=True,
#                         )

#         record_date = datepicker_component(config=config)
#         st.session_state.record_data["record_date_range"] = record_date


#     st.session_state.record_data["change"] = False
#     with col1:
#         athletes = pd.DataFrame(listAthletes())
#         athlete_name = st.selectbox("ورزشکار", 
#                         athletes["name"], 
#                         placeholder="انتخاب کنید"
#         )

#         athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
#         results = pd.DataFrame(listAthleteRecordsByCategory(athlete_id, category="قدرت"))

#         results["date"] = pd.to_datetime(results["gregorian_date"])

#         athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

#         st.session_state.record_data["athlete_name"] = athlete_name
#         st.session_state.record_data["athlete_weight"] = athlete_weight
#         st.session_state.record_data["athlete_id"] = athlete_id

#         # print("gregorian_date",pd.to_datetime(results['gregorian_date']))
#         # print("from",pd.to_datetime(st.session_state.record_data["record_date_range"]['from'].togregorian()))
#         if st.session_state.record_data["record_date_range"] and st.session_state.record_data["record_date_range"]['to']:
#             results = results[(results['date'] >= pd.to_datetime(st.session_state.record_data["record_date_range"]['from'].togregorian())) 
#                                 & 
#                             (results['date'] <= pd.to_datetime(st.session_state.record_data["record_date_range"]['to'].togregorian()))
#                             ]
#         # print(results[results.test_category == "قدرت"])
#         strenght_history(results[results.test_category == "قدرت"])
        

#     # st.subheader(f"تاریخ منتخب از {record_date['from']:%y/%m/%d} تا {record_date['to']:%y/%m/%d}")
with st.container():
    athletes = pd.DataFrame(listAthletes())
    # name, date = st.columns([0.8, 0.2])
    # with name:
    athletes_name = st.segmented_control(
        "ورزشکار", athletes["name"], selection_mode="multi"
    )
    # option_map = {
    #     0: ":material/add:",
    #     1: ":material/zoom_in:",
    #     2: ":material/zoom_out:",
    #     3: ":material/zoom_out_map:",
    # }
    # selection = st.pills(
    #     "ورزشکار", athletes["name"],
    #     selection_mode="single",
    # )
    # with date:
    #     config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
    #                     color_primary_light="#ff9494", selection_mode="range",closed_view="button",
    #                     should_highlight_weekends=True, always_open=False,
    #                     )

    #     record_date = datepicker_component(config=config)




import time



def athlete_cart(i):

    image_url = athletes.loc[athletes["name"] == athletes_name[i], "image_url"].values[0] if not athletes.loc[athletes["name"] == athletes_name[i], "image_url"].empty else ""
    
    st.image(image_url, width=200)
    # with image:

   


@st.fragment
def selected_athletes(grid):
    for i in range(len(athletes_name)):
        container = grid[i].container(border=True)


        with container:
            athlete_cart(i)

if athletes_name:
    row1 = st.columns(len(athletes_name))
    grid = [col.container(height=300, border=False) for col in row1]
    safe_grid = [card.empty() for card in grid]

    selected_athletes(grid)


def visual_records_by_athlete(athletes, athletes_name, test_name):
        

    records = listAthletesRecordsByName(test_name=test_name)
    if records:

        cooper_df = pd.DataFrame(records)
        print(athletes)
        athlete_id = athletes[athletes["name"].isin(athletes_name)]['athlete_id']
        print(athlete_id)

        # athletes_id
        cooper_records = cooper_df[cooper_df["athlete_id"].isin(athlete_id)]

        # Extract the name from athlete_name

        cooper_records["athlete_name"] = cooper_records["athlete_name"].apply(lambda x: x["name"])
        cooper_records["vo2max"] = cooper_records["raw_data"].apply(lambda x: x["vo2max"])
        print(cooper_records)

        grouped_df = cooper_records.groupby(["athlete_name", "test_date"])["vo2max"].sum().reset_index()
        print(grouped_df)
        athletes_list = grouped_df["athlete_name"].unique().tolist()
        dates_value = sorted(grouped_df["test_date"].unique().tolist())

        athlete_data = {athlete: [0] * len(dates_value) for athlete in athletes_list}  # Initialize with zeros
        for _, row in grouped_df.iterrows():
            athlete = row["athlete_name"]
            date_value = row["test_date"]
            score = row["vo2max"]
            
            if date_value in dates_value:
                index = dates_value.index(date_value)
                athlete_data[athlete][index] = score

        print(athlete_data)

        # Call the updated function to generate the chart
        multi_bar_line_plot(
            x=dates_value, 
            y=athlete_data, 
            xaxis_title="تاریخ", 
            yaxis_title="vo2max", 
            title="تست ۶-دقیقه", 
            athletes=athletes_list
        )
    else:
        st.info(f"داده ای برای تست {test_name} وجود ندارد")




@st.fragment
def stamina_records_chart():
    with st.container(border=True):
        visual_records_by_athlete(athletes, athletes_name, test_name="۶-دقیقه")
        visual_records_by_athlete(athletes, athletes_name, test_name="cooper")
        



stamina_records_chart()