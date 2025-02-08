# app.py
import streamlit as st
from streamlit import session_state as state
from streamlit_nej_datepicker import datepicker_component, Config
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import datetime
import pytz
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from st_supabase_connection import execute_query
from utils.database import (
    listAthletes, 
    insertRecord,
    deleteListRecords,
    updateAthleteWeight,
    listAthletesRecordsByName,
    )
from utils.logical_functions import calculate_vo2max_6min, calculate_vo2max_cooper

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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/styles/custom.css")

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

def convert_to_jalali(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")  # Convert to datetime object
    jalali_date = JalaliDate.to_jalali(dt.year, dt.month, dt.day)  # Convert to Jalali
    return f"{jalali_date.year}-{jalali_date.month:02d}-{jalali_date.day:02d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"






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

def update_data(*args, **kwargs):
    copy_data = args[0].copy()
    filtered_df = copy_data.loc[st.session_state[kwargs['records_data']]['deleted_rows']]  
    deleted_data = deleteListRecords(filtered_df['result_id'].to_list())
    st.toast(st.session_state[kwargs['records_data']])

def visual_records_by_athlete(athletes, athletes_records ,athletes_name, test_name, title, xaxis_title, yaxis_title):
        



    
    athlete_id = athletes[athletes["name"].isin(athletes_name)]['athlete_id']
    # athletes_id
    selected_records = athletes_records[athletes_records["athlete_id"].isin(athlete_id)]

    # Extract the name from athlete_name

    selected_records["athlete_name"] = selected_records["athlete_data"].apply(lambda x: x["name"])
    selected_records["athlete_image"] = selected_records["athlete_data"].apply(lambda x: x["image_url"])
    selected_records["updated_datetime"] = selected_records["updated_at"].apply(convert_to_jalali)

    selected_records[yaxis_title] = selected_records["raw_data"].apply(lambda x: x[yaxis_title])

    grouped_df = selected_records.groupby(["athlete_name", "test_date"])[yaxis_title].sum().reset_index()

    # Extract unique athletes
    athletes_list = grouped_df["athlete_name"].unique().tolist()

    # Create a dictionary to store only existing values (No None, No 0s)
    athlete_data = {
        athlete: grouped_df[grouped_df["athlete_name"] == athlete].set_index("test_date")[yaxis_title].to_dict()
        for athlete in athletes_list
    }
    
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
    chart , table = st.columns(2, vertical_alignment="center")
    if selection == "chart":
        # Call the updated function to generate the chart
        multi_bar_line_plot(
            athlete_data=athlete_data, 
            xaxis_title=xaxis_title, 
            yaxis_title=yaxis_title, 
            title=title, 
            athletes=athletes_list
        )
    elif selection == "table":
        selected_records = selected_records.reset_index(drop=True)
        st.data_editor(
            selected_records.filter(items=['athlete_image', 'athlete_name', 'test_date', 'test_category','test_name',yaxis_title, 'updated_datetime']),  
            hide_index=None,
            disabled=('athlete_image','updated_datetime', 'test_category', 'test_name'),
            column_config={
                "athlete_image": st.column_config.ImageColumn(
                    "تصویر",
                    help="athlete_image 🎈",
                    pinned=True,
                ),
                "athlete_name": st.column_config.SelectboxColumn(
                    "ورزشکار",
                    help="athlete_name 🎈",
                    options=athletes["name"],
                    pinned=True,
                ),
                "test_date": st.column_config.TextColumn(
                    "تاریخ",
                    help="تاریخ 🎈",
                ),
                "test_category": st.column_config.TextColumn(
                    "دسته",
                    help="تاریخ 🎈",
                ),
                "test_name": st.column_config.TextColumn(
                    "تست",
                    default=test_name,
                    help="تاریخ 🎈",
                ),
                yaxis_title: st.column_config.NumberColumn(
                    yaxis_title,
                    help=f"{yaxis_title} 🎈",
                ),
                "updated_datetime": st.column_config.TextColumn(
                    "آخرین تغییرات",
                    help="updated_datetime 🎈",
                ),
            },
            num_rows="dynamic",
            on_change=update_data,
            args=(selected_records,),
            kwargs={"records_data":f'{test_name}-records_data'},
            key=f'{test_name}-records_data'
            )
            


def update_weight(*args, **kwargs):

    # print({"weight": round(st.session_state.athlete_weight, 1)})
    updateAthleteWeight(kwargs, {"weight": round(st.session_state.athlete_weight, 1)})
    


@st.dialog("تست جدید")
def new_stamina_record(athletes , item):
    st.title(item)
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

        with st.container(border=True):
            distance_6min = st.number_input("مسافت طی شده (کیلومتر)", min_value=0.0, step=0.01, key="distance_6min")
            record_type = st.selectbox("آزمون", options=["pre-test","post-test"])
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
            
            record_date = record_date.strftime("%Y-%m-%d")
            gregorian_date = gregorian_date.strftime("%Y-%m-%d")

        if st.button("ثبت"):
            with st.spinner('در حال محاسبه ...'):
                time.sleep(2.5)
            vo2max = calculate_vo2max_6min(distance_6min)
            exercise_data = {
                "distance": distance_6min,
                "vo2max": vo2max,
            }       
            new_record = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "۶-دقیقه",
                "test_category": "استقامت",
                "test_date": record_date,
                "gregorian_date": gregorian_date,
            }
            st.metric(label="VO2Max (اکنون)", value=vo2max)
            
            insertRecord(new_record)
            st.rerun()


@st.fragment
def stamina_records_chart():
    with st.expander("استقامت", expanded=True):
        st.subheader("استقامت")
        test_options = {
            "۶-دقیقه": {
                "title":"تست ۶-دقیقه", "xaxis_title":"تاریخ", "yaxis_title":"vo2max"
            }, 
            "cooper": {"title":"cooper ", "xaxis_title":"تاریخ", "yaxis_title":"vo2max"}
               
        }
        # print(test_options[0])
        selection = st.pills(
            "",
            options=test_options,
            selection_mode="single",
            default="۶-دقیقه",
            key=f"استقامت"
        )
        records = listAthletesRecordsByName(test_name=selection)
        if records:
            athletes_records = pd.DataFrame(records)
            visual_records_by_athlete(athletes, athletes_records, athletes_name, 
                                      test_name=selection, 
                                      title=test_options[selection]["title"], 
                                      xaxis_title=test_options[selection]["xaxis_title"], 
                                      yaxis_title=test_options[selection]["yaxis_title"])
        else:
            st.info(f"داده ای برای تست {selection} وجود ندارد")

        if st.button(":material/add: رکورد جدید", key=selection):
                
            new_stamina_record(athletes, selection)


@st.fragment
def strength_records_chart():
    with st.expander("قدرت"):
        st.subheader("قدرت")
        test_options = {
            "قدرت نسبی": {"title":"قدرت نسبی ", "xaxis_title":"تاریخ", "yaxis_title":"estimate_power"}
               
        }
        # print(test_options[0])
        selection = st.pills(
            "",
            options=test_options,
            selection_mode="single",
            default="قدرت نسبی",
            key=f"قدرت"
        )
        if selection:
            visual_records_by_athlete(athletes, athletes_name, test_name=selection, title=test_options[selection]["title"], xaxis_title=test_options[selection]["xaxis_title"], yaxis_title=test_options[selection]["yaxis_title"])
            
        
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
with st.sidebar:

    col1, col2 = st.columns([2,1])
    
    with col1:
        athletes = pd.DataFrame(listAthletes())
        athletes_name = st.pills(
            "",
            options=athletes["name"],
            selection_mode="multi",
            default=athletes["name"],
            key="athletes_name"

        )
        # tests = pd.DataFrame(listTests())
        # tests_name = st.pills(
        #     "",
        #     options=tests["test_name"],
        #     selection_mode="multi",
        #     key="tests_name"
        # )
    config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                    color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                    should_highlight_weekends=True, always_open=True,
                    )

    record_date = datepicker_component(config=config)


if athletes_name:
    # selected_athletes(athletes_name)
    
    stamina_records_chart()
    # agility_records_chart()
    # strength_records_chart()
    # anerobic_records_chart()












