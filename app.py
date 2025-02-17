# app.py
import streamlit as st
from streamlit_nej_datepicker import datepicker_component, Config
from st_supabase_connection import SupabaseConnection
import pandas as pd
from utils.database import (
    listAthletes,
    deleteListRecords,
    listAthletesRecordsByName
    )
from utils.tools import local_css, convert_to_jalali
from components.charts import  multi_bar_line_plot, multi_line_plot, multi_bar_plot
from components.forms.form_strength import new_strength_relative_strength_record
from components.forms.form_stamina import new_stamina_6min_record, new_stamina_cooper_record
from components.forms.form_anaerobic import (
    new_anaerobic_800_200_record, 
    new_anaerobic_rast_record, 
    new_anaerobic_wingate_record,
    new_anaerobic_burpee_record
    )
from components.forms.form_agility import (
    new_wrestle_specific_record, 
    new_wrestle_zone_record, 
    new_wrestle_T_record, 
    new_wrestle_illinois_record, 
    new_wrestle_bear_record
    )
from components.forms.form_felexibility import (
    sit_reach_form,
    shoulder_lift_form,
    upper_body_opening_form
    )

from components.forms.form_muscle_stamina import (
    situp_form,
    pullup_form,
    dip_parallel_form
    )
from components.constants import CATEGORIES_OPTIONS, EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
import jdatetime
from typing import List, Union, Dict


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
if "athlete_weight" not in st.session_state:
    st.session_state.athlete_weight = 0


local_css("assets/styles/custom.css")

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

def visual_records_by_athlete(
        athletes, 
        athletes_records ,
        athletes_name, 
        record_category, 
        record_name,
        record_option, 
        title, 
        xaxis, 
        yaxis, 
        xaxis_title, 
        yaxis_title, 
        chart_selector_col):
    
    athlete_id = athletes[athletes["name"].isin(athletes_name)]['athlete_id']
    selected_records = athletes_records[athletes_records["athlete_id"].isin(athlete_id)]

    table , chart = st.columns(2, vertical_alignment="top")
    # record_option
    
    # Extract the name from athlete_name

    selected_records["athlete_name"] = selected_records["athlete_data"].apply(lambda x: x["name"])
    selected_records["athlete_image"] = selected_records["athlete_data"].apply(lambda x: x["image_url"])
    selected_records["updated_datetime"] = selected_records["updated_at"].apply(convert_to_jalali)

    selected_records[yaxis] = selected_records["raw_data"].apply(lambda x: x[yaxis])
    print("--------->",yaxis)
    if yaxis in ('relative_strength','relative_strength'):

        selected_records['exercise'] = selected_records["raw_data"].apply(lambda x: x['exercise'])
        exercise = table.selectbox("نام حرکت:",
                options=selected_records['exercise'].unique() ,
                placeholder="انتخاب کنید",
                key=f"exercise"
                )
        selected_records = selected_records[selected_records['exercise'] == exercise]

    grouped_df = selected_records.groupby(["athlete_name", xaxis])[yaxis].sum().reset_index()

    # Extract unique athletes
    athletes_list = grouped_df["athlete_name"].unique().tolist()

    # Create a dictionary to store only existing values (No None, No 0s)
    athlete_data = {
        athlete: grouped_df[grouped_df["athlete_name"] == athlete].set_index(xaxis)[yaxis].to_dict()
        for athlete in athletes_list
    }
    option_map = {
        "bar": ":material/equalizer:",
        "line": ":material/show_chart:",

    }

    chart_view = chart_selector_col.segmented_control(
        "نمودار",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
        default="bar",
        key=f"{yaxis_title}-seletion-view"
    )
    with chart:
        if chart_view == "bar":
            # if selection == "chart":
            with chart:
                # Call the updated function to generate the chart
                multi_bar_plot(
                    title=title, 
                    athlete_data=athlete_data, 
                    xaxis_title=xaxis_title, 
                    yaxis_title=yaxis_title, 
                    athletes=athletes_list
                )
        elif chart_view == "line":
            # if selection == "chart":
            with chart:
                # Call the updated function to generate the chart
                multi_line_plot(
                    title=title, 
                    athlete_data=athlete_data, 
                    xaxis_title=xaxis_title, 
                    yaxis_title=yaxis_title, 
                    athletes=athletes_list
                )
        else:
            st.info("لطفا یک گزینه را انتخاب کنید")
    # elif selection == "table":
    with table:
        selected_records = selected_records.reset_index(drop=True)
        st.data_editor(
            selected_records.filter(items=['athlete_image', 'athlete_name', 'test_date', yaxis, 'test_category','test_name', 'updated_datetime']),  
            hide_index=None,
            disabled=('athlete_image','updated_datetime', 'test_category', 'test_name'),
            column_config={
                "athlete_image": st.column_config.ImageColumn(
                    "تصویر",
                    help="athlete_image 🎈",
                    pinned=True,
                ),
                "athlete_name": st.column_config.TextColumn(
                    "ورزشکار",
                    help="athlete_name 🎈",
                    pinned=True,
                ),
                "test_date": st.column_config.TextColumn(
                    "تاریخ",
                    help="تاریخ 🎈",
                ),
                "test_category": st.column_config.TextColumn(
                    "دسته",
                    help="نام دسته 🎈",
                ),
                "test_name": st.column_config.TextColumn(
                    "تست",
                    default=record_category,
                    help="نام تست 🎈",
                ),
                yaxis: st.column_config.NumberColumn(
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
            kwargs={"records_data":f'{record_category}-records_data'},
            key=f'{record_category}-records_data'
            )
            


import random
@st.fragment
def category_records(record_category):
    categories_keys = list(CATEGORIES_OPTIONS[record_category].keys())
    record_selector_col, metric_selector_col, chart_selector_col = st.columns(3, vertical_alignment="top")

    record_name = record_selector_col.pills(
        "آزمون",
        options=categories_keys,
        selection_mode="single",
        default=categories_keys[0],
        key=CATEGORIES_OPTIONS[record_category]
    )
    if record_name:
   
        records = listAthletesRecordsByName(test_name=record_name, range_date=range_record_date)
        record_option = CATEGORIES_OPTIONS[record_category][record_name]
        if st.button(":material/add: رکورد جدید", key=record_option):
            match record_name:
                case "۶-دقیقه":
                    return new_stamina_6min_record(athletes, record_name, record_category)
                case "cooper":
                    return new_stamina_cooper_record(athletes, record_name, record_category)
                case "قدرت نسبی":
                    return new_strength_relative_strength_record(athletes, record_name, record_category)
                case "افت-عملکرد":
                    return new_anaerobic_800_200_record(athletes, record_name, record_category)
                case "RAST":
                    return new_anaerobic_rast_record(athletes, record_name, record_category)
                case "wingate":
                    return new_anaerobic_wingate_record(athletes, record_name, record_category)
                case "burpee":
                    return new_anaerobic_burpee_record(athletes, record_name, record_category)
                case "ویژه-کشتی":
                    return new_wrestle_specific_record(athletes, record_name, record_category)
                case "خرسی":
                    return new_wrestle_bear_record(athletes, record_name, record_category)
                case "منطقه":
                    return new_wrestle_zone_record(athletes, record_name, record_category)
                case "T":
                    return new_wrestle_T_record(athletes, record_name, record_category)
                case "illinois":
                    return new_wrestle_illinois_record(athletes, record_name, record_category)
                case "sit&reach":
                    return sit_reach_form(athletes, record_name, record_category)
                case "بالا-آوردن-شانه":
                    return shoulder_lift_form(athletes, record_name, record_category)
                case "باز-شدن-بالا-تنه":
                    return upper_body_opening_form(athletes, record_name, record_category)
                case "دراز-نشست":
                    return situp_form(athletes, record_name, record_category)
                case "بارفیکس":
                    return pullup_form(athletes, record_name, record_category)
                case "دیپ-پارالل":
                    return dip_parallel_form(athletes, record_name, record_category)

        if records:
            athletes_records = pd.DataFrame(records)

            yaxis_title_options = metric_selector_col.pills(
                "معیار اندازه گیری",
                options=record_option['yaxis_title_options'],
                default=record_option['yaxis_title_options'][0],
                selection_mode="single",
                key=record_name
            )
            if yaxis_title_options:
                
                selected_index = record_option['yaxis_title_options'].index(yaxis_title_options)

                visual_records_by_athlete(
                                        athletes, 
                                        athletes_records, 
                                        athletes_name, 
                                        record_category=record_category, 
                                        record_name=record_name,
                                        record_option=record_option,
                                        title=record_option["title"], 
                                        xaxis=record_option["xaxis"], 
                                        yaxis=record_option['yaxis_options'][selected_index],
                                        xaxis_title=record_option["xaxis_title"], 
                                        yaxis_title=yaxis_title_options,
                                        chart_selector_col=chart_selector_col
                                        )
            else:
                st.info("لطفا یک گزینه را انتخاب کنید")
        else:
            st.info(f"داده ای برای تست {record_category} وجود ندارد")
    

    else:
        st.info("لطفا یک گزینه را انتخاب کنید")

# with st.sidebar: 
left, center, right = st.columns([1,3,1])
with st.sidebar:

    col1, col2 = st.columns([2,2])
    
    with col1:
        athletes = pd.DataFrame(listAthletes())
        athletes_name = st.pills(
            "",
            options=athletes["name"],
            selection_mode="multi",
            default=athletes["name"],
            key="athletes_name"

        )
     
    config = Config(dark_mode=True, locale="fa", color_primary="#124d24",
                   
                    color_primary_light="#124d24", selection_mode="range",closed_view="button",
                    should_highlight_weekends=True, always_open=True,
                    default_value={"from":jdatetime.date.today(), "to":jdatetime.date.today()}
                    )

    range_record_date = datepicker_component(config=config)

@st.fragment
def athletes_records_container():

    
    categories = list(CATEGORIES_OPTIONS.keys())
    category = st.pills(
        "",
        options=categories,
        selection_mode="single",
        default=categories[0],
        key="selected_categories"
    )
    if category:
        st.session_state.records_category_name = category
        with st.container(border=True, key=category):

            category_records(category)
    else:
        st.info("لطفا یک گزینه را انتخاب کنید")    

if athletes_name:
    # selected_athletes(athletes_name)
    # col1, col2, col3 = st.columns(3)
    # with col1.container(border=True):
    #     st.metric(label="قدرت", value="۷۲", delta="۱٫۲ %")
    # with col2.container(border=True):
    #     st.metric(label="استقامت", value="۶۸", delta="۶٫۸ %")
        
    # with col3.container(border=True):
    #     st.metric(label="چابکی", value="۱۸", delta="۹٫۷ %")

    athletes_records_container()













