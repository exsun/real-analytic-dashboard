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
from streamlit_image_select import image_select


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

def visual_records_by_athlete(athletes, athletes_name, test_name, title, xaxis_title, yaxis_title):
        

    records = listAthletesRecordsByName(test_name=test_name)
    if records:

        records_df = pd.DataFrame(records)
        athlete_id = athletes[athletes["name"].isin(athletes_name)]['athlete_id']

        # athletes_id
        selected_records = records_df[records_df["athlete_id"].isin(athlete_id)]

        # Extract the name from athlete_name

        selected_records["athlete_name"] = selected_records["athlete_name"].apply(lambda x: x["name"])
        selected_records[yaxis_title] = selected_records["raw_data"].apply(lambda x: x[yaxis_title])

        grouped_df = selected_records.groupby(["athlete_name", "test_date"])[yaxis_title].sum().reset_index()
        athletes_list = grouped_df["athlete_name"].unique().tolist()
        dates_value = sorted(grouped_df["test_date"].unique().tolist())

        athlete_data = {athlete: [0] * len(dates_value) for athlete in athletes_list}  # Initialize with zeros
        for _, row in grouped_df.iterrows():
            athlete = row["athlete_name"]
            date_value = row["test_date"]
            score = row[yaxis_title]
            
            if date_value in dates_value:
                index = dates_value.index(date_value)
                athlete_data[athlete][index] = score

        option_map = {
            "chart": ":material/monitoring:",
            "table": ":material/table:",
        }
    
        selection = st.segmented_control(
            "",
            options=option_map.keys(),
            format_func=lambda option: option_map[option],
            selection_mode="single",
            default="chart",
            key=f"{title}-seletion-view"
        )

        if selection == "chart":
            # Call the updated function to generate the chart
            multi_bar_line_plot(
                x=dates_value, 
                y=athlete_data, 
                xaxis_title=xaxis_title, 
                yaxis_title=yaxis_title, 
                title=title, 
                athletes=athletes_list
            )
        else: 
            st.dataframe(selected_records)
    else:
        st.info(f"داده ای برای تست {title} وجود ندارد")




@st.fragment
def stamina_records_chart():
    with st.expander("استقامت"):
        st.subheader("استقامت")
        visual_records_by_athlete(athletes, athletes_name, test_name="۶-دقیقه", title="تست ۶-دقیقه", xaxis_title="تاریخ", yaxis_title="vo2max")
        visual_records_by_athlete(athletes, athletes_name, test_name="cooper", title="cooper ", xaxis_title="تاریخ", yaxis_title="vo2max")
        
@st.fragment
def strength_records_chart():
    with st.expander("قدرت"):
        st.subheader("قدرت")
        visual_records_by_athlete(athletes, athletes_name,test_name="قدرت نسبی", title="قدرت نسبی ", xaxis_title="تاریخ", yaxis_title="estimate_power")
        
@st.fragment
def anerobic_records_chart():
    with st.expander("بی هوازی"):
        st.subheader("بی هوازی")
        visual_records_by_athlete(athletes, athletes_name,test_name="performance_decrease", xaxis_title="تاریخ" ,yaxis_title="افت عملکرد", title="آزمون ۸۰۰−۲۰۰ متر")
        
@st.fragment
def agility_records_chart():
    with st.expander("چابکی"):
        st.subheader("چابکی")
        visual_records_by_athlete(athletes, athletes_name,test_name="wrestle_specific_duration", xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون چابکی ویژه کشتی")
        visual_records_by_athlete(athletes, athletes_name,test_name="bear_duration", xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون خرسی")
        visual_records_by_athlete(athletes, athletes_name,test_name="zone_duration", xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون منطقه")
        visual_records_by_athlete(athletes, athletes_name,test_name="T_duration", xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون T (ثانیه)")
        visual_records_by_athlete(athletes, athletes_name,test_name="illinois_duration", xaxis_title="تاریخ" ,yaxis_title="مدت زمان", title="آزمون illinois (ثانیه)")




@st.fragment
def felexibility_records_chart():
    with st.expander("انعطاف پذیری"):
        st.subheader("انعطاف پذیری")
        visual_records_by_athlete(athletes, athletes_name,test_name="sit_reach_distance", xaxis_title="تاریخ" ,yaxis_title="فاصله (سانتی متر)", title=" آزمون sit & reach")
        visual_records_by_athlete(athletes, athletes_name,test_name="shoulder_lift_distance", xaxis_title="تاریخ" ,yaxis_title="فاصله (سانتی متر)", title=" آزمون بالا آوردن شانه")
        visual_records_by_athlete(athletes, athletes_name,test_name="upper_body_opening_distance", xaxis_title="تاریخ" ,yaxis_title="فاصله (سانتی متر)", title=" آزمون باز شدن بالا تنه")

     
     
with st.container():
    athletes = pd.DataFrame(listAthletes())
    # img = image_select("Label", athletes["image_url"].to_list())
   
    # Display the pills selection.
    with st.sidebar: 
        athletes_name = st.pills(
            "ورزشکاران",
            options=athletes["name"],
            selection_mode="multi",
        )
        config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                        color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                        should_highlight_weekends=True, always_open=True,
                        )

        record_date = datepicker_component(config=config)




    cols = st.columns(2)
    with cols[0]:
        stamina_records_chart()

        agility_records_chart()
    with cols[1]:
        strength_records_chart()

        anerobic_records_chart()






import time



def athlete_cart(i):

    image_url = athletes.loc[athletes["name"] == athletes_name[i], "image_url"].values[0] if not athletes.loc[athletes["name"] == athletes_name[i], "image_url"].empty else ""
    
    st.image(image_url, width=200)

   


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




