# app.py
import streamlit as st
from streamlit import session_state as state
from streamlit_nej_datepicker import datepicker_component, Config
from persiantools.jdatetime import JalaliDate
from datetime import datetime
import pytz
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from st_supabase_connection import execute_query
from utils.database import (
    listAthletes, 
    listTests,
    getAthleteByName,
    listAthleteRecords, 
    listAthletesWithHistory, 
    listAthletesRecordsByName,
    listAthleteRecordsByCategory,
    FilterRecordsByAthleteId
    )


from streamlit_nej_datepicker import datepicker_component, Config
import numpy as np
from datetime import date, timedelta
from components.charts import bar_line_plot, multi_bar_line_plot

import time


st.set_page_config(
    page_title="ارزیابی عملکرد کشتی",
    page_icon="🎯",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={}
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/styles/custom.css")

try:
    st.session_state["client"] = st.connection(
        name="supabase",
        type=SupabaseConnection,
        ttl=0,
    )
    st.session_state["initialized"] = True
except Exception as e:
    st.error(
        f"""Client initialization failed
        {e}""",
        icon="❌",
    )
    st.session_state["initialized"] = False


if "record_data" not in st.session_state:
    st.session_state.record_data = {}


# # Widgets shared by all the pages
# strength = st.Page(
#     "pages/form/strength.py", title="قدرت", icon=":material/notification_important:"
# )
# stamina = st.Page(
#     "pages/form/stamina.py", title="استقامت", icon=":material/notification_important:"
# )
# anaerobic = st.Page(
#     "pages/form/anaerobic.py", title="بی هوازی", icon=":material/notification_important:"
# )
# agility = st.Page(
#     "pages/form/agility.py", title="چابکی", icon=":material/notification_important:"
# )
# reaction = st.Page(
#     "pages/form/reaction.py", title="عکس العمل", icon=":material/notification_important:"
# )
# felexibility = st.Page(
#     "pages/form/felexibility.py", title="انعطاف پذیری", icon=":material/notification_important:"
# )
# power = st.Page(
#     "pages/form/power.py", title="توان", icon=":material/notification_important:"
# )
# muscle_stamina = st.Page(
#     "pages/form/muscle_stamina.py", title="استقامت عضلانی", icon=":material/power:"
# )
# sleep = st.Page(
#     "pages/form/sleep.py", title="خواب", icon=":material/sleep:"
# )
# stress_anxiety = st.Page(
#     "pages/form/stress_anxiety.py", title="استرس - اضطراب", icon=":material/sleep:"
# )
# blood_urine = st.Page(
#     "pages/form/blood_urine.py", title="خون - ادرار", icon=":material/sleep:"
# )
# anaerobic_report = st.Page(
#     "pages/report/anaerobic_report.py", title="بی هوازی", icon=":material/sleep:"
# )
# orm = st.Page(
#     "pages/form/orm.py", title="orm", icon=":material/notification_important:"
# )
# athlethes = st.Page(
#     "pages/athlethe/list.py", title="ورزشکاران", icon=":material/notification_important:"
# )


# # Title
# # st.title("سامانه پایش کشتی گیران آزاد")

# # Sidebar Jalali Date Input



# pg = st.navigation(
#     {
#         "ورزشکاران": [athlethes],
#         "تست ها:": [strength, stamina, anaerobic, agility, reaction, felexibility, power, muscle_stamina],
#         "پرسشنامه ها:": [sleep, stress_anxiety, blood_urine],
#         "گزارش": [anaerobic_report, orm],

#     }
# )

# pg.run()








def athlete_cart(i):

    image_url = athletes.loc[athletes["name"] == athletes_name[i], "image_url"].values[0] if not athletes.loc[athletes["name"] == athletes_name[i], "image_url"].empty else ""
    
    st.image(image_url, width=200)

   


@st.fragment
def selected_athletes(athletes_name):
    row1 = st.columns(len(athletes_name))
    grid = [col.container(height=300, border=False) for col in row1]
    safe_grid = [card.empty() for card in grid]
    for i in range(len(athletes_name)):
        container = grid[i].container(border=True)


        with container:
            athlete_cart(i)

def column_change():
    print("selected_drill")
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
    
        selection = st.pills(
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
            st.data_editor(
                selected_records,
                column_config={
                    "athlete_name": st.column_config.TextColumn(
                        "athlete_name",
                        help="Streamlit **widget** commands 🎈",
                        default="st.",
                        max_chars=50,
                      
                    )
                },
                hide_index=True,
                num_rows="dynamic",
                on_change=column_change
                )
    else:
        st.info(f"داده ای برای تست {title} وجود ندارد")




@st.fragment
def stamina_records_chart():
    with st.expander("استقامت", expanded=True):
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





# with st.sidebar: 
left, center, right = st.columns([1,3,1])
with left:

    col1, col2 = st.columns(2)
    
    with col1:
        athletes = pd.DataFrame(listAthletes())
        athletes_name = st.pills(
            "",
            options=athletes["name"],
            selection_mode="multi",
            key="athletes_name"

        )
    with col2:
        tests = pd.DataFrame(listTests())
        tests_name = st.pills(
            "",
            options=tests["test_name"],
            selection_mode="multi",
            key="tests_name"
        )

with center:
    if athletes_name:
        # selected_athletes(athletes_name)
        
        stamina_records_chart()
        agility_records_chart()
        strength_records_chart()
        anerobic_records_chart()

with right:
    config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                    color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                    should_highlight_weekends=True, always_open=True,
                    )

    record_date = datepicker_component(config=config)












