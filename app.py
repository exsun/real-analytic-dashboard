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
from components.charts import  multi_bar_line_plot
from components.forms.form_strength import new_strength_relative_strength_record
from components.forms.form_stamina import new_stamina_6min_record, new_stamina_cooper_record
from components.forms.form_anaerobic import new_anaerobic_800_200_record

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
    # st.toast(st.session_state[kwargs['records_data']])

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
        key=f"{yaxis_title}-seletion-view"
    )
    chart , table = st.columns(2, vertical_alignment="center")
    # if selection == "chart":
    with chart:
        # Call the updated function to generate the chart
        multi_bar_line_plot(
            title=title, 
            athlete_data=athlete_data, 
            xaxis_title=xaxis_title, 
            yaxis_title=yaxis_title, 
            athletes=athletes_list
        )
    # elif selection == "table":
    with table:
        selected_records = selected_records.reset_index(drop=True)
        st.data_editor(
            selected_records.filter(items=['athlete_image', 'athlete_name', 'test_date', yaxis_title, 'test_category','test_name', 'updated_datetime']),  
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
            


import random
@st.fragment
def category_records(category):
    categories_keys = list(categories_options[category].keys())
    
    record_name = st.pills(
        "",
        options=categories_keys,
        selection_mode="single",
        default=categories_keys[0],
        key=categories_options[category]
    )

    records = listAthletesRecordsByName(test_name=record_name)
    if records:
        athletes_records = pd.DataFrame(records)
       
        yaxis_title_options = st.selectbox(
            "",
            options=categories_options[category][record_name]['yaxis_title_options'],
            key=record_name
        )
        visual_records_by_athlete(
                                athletes, 
                                athletes_records, 
                                athletes_name, 
                                test_name=category, 
                                title=categories_options[category][record_name]["title"], 
                                xaxis_title=categories_options[category][record_name]["xaxis_title"], 
                                yaxis_title=yaxis_title_options
                                )
    else:
        st.info(f"داده ای برای تست {category} وجود ندارد")
    # categories_options[category][record_name]
    if st.button(":material/add: رکورد جدید", key=categories_options[category][record_name]):
        match record_name:
            case "۶-دقیقه":
                return new_stamina_6min_record(athletes, record_name, category)
            case "cooper":
                return new_stamina_cooper_record(athletes, record_name, category)
            case "قدرت نسبی":
                return new_strength_relative_strength_record(athletes, record_name, category)

            case "افت-عملکرد":
                return new_anaerobic_800_200_record(athletes, record_name, category)



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
     
    config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                    color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                    should_highlight_weekends=True, always_open=True,
                    )

    record_date = datepicker_component(config=config)

categories_options = {
        "قدرت" : {
            "قدرت نسبی": {
                "title":"تست قدرت نسبی", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "relative_strength",
                    "one_repetition_maximum",
                ],
            },   
        },
        "استقامت" : {
            "۶-دقیقه": {
                "title":"تست ۶-دقیقه", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "vo2max",
                ],
            },
            "cooper": {
                "title":"cooper ",
                "xaxis_title": "تاریخ", 
                "yaxis_title_options":[
                    "vo2max",
                ],
               
            }   
        },
        "بی-هوازی" : { 
            "افت-عملکرد": {
                "title":"تست افت-عملکرد", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "performance_decrease",
                    "performance_perc",
                ],
            },
            "RAST": {
                "title":"تست RAST", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "peak_power",
                    "average_power",
                    "total_power",
                    "fatigue_index",
                ],
            },
            "wingate": {
                "title":"تست wingate", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "peak_power",
                    "average_power",
                    "total_power",
                    "fatigue_index",
                ],
            },
            "burpee": {
                "title":"تست burpee", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "burpee_count",
                ],
            },
        },
        "چابکی" : {
            "ویژه کشتی": {
                "title":"تست ویژه کشتی", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "wrestle_specific_duration",
                ],
            },
            "خرسی": {
                "title":"تست خرسی", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "bear_duration",
                ],
            },
            "منطقه": {
                "title":"تست منطقه", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "zone_duration",
                ],
            }, 
            "T": {
                "title":"تست T", 
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "T_duration",
                ],
            }, 
            "illinois": {
                "title":"تست illinois",
                "xaxis_title": "تاریخ",
                "yaxis_title_options":[
                    "illinois_duration",
                ],
            },
        },
        "عکس العمل" : {
            "",    
        },
        "انعطاف پذیری" : {
            "",    
        },
        "استقامت عضلانی" : {
            "",    
        },

    }


@st.fragment
def athletes_records_container():

    
    categories = list(categories_options.keys())
    category = st.pills(
        "",
        options=categories,
        selection_mode="single",
        default=categories[0],
        key="selected_categories"
    )
    st.session_state.records_category_name = category
    with st.container(border=True, key=category):
        st.subheader(category)
    
        category_records(category)
    
    

if athletes_name:
    selected_athletes(athletes_name)

    athletes_records_container()













