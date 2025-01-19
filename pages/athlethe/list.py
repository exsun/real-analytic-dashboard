import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from st_supabase_connection import execute_query
from utils.database import st_supabase_client, list_athlete, list_athlete_history
from persiantools.jdatetime import JalaliDate
from datetime import datetime

from streamlit_nej_datepicker import datepicker_component, Config
import jdatetime

import numpy as np
from datetime import date, timedelta
import string
import time

if "record_data" not in st.session_state:
    st.session_state.record_data = {}

def bar_line_plot(x , y):
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
            xaxis_title="Category",
            yaxis_title="Value",
            barmode='group',
            template="plotly_white"
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)


def strenght_history(results):
    # Pre-process
    results['estimate_power'] = results['raw_data'].apply(lambda x: x['estimate_power'])
    results['estimated_1rm'] = results['raw_data'].apply(lambda x: x['estimated_1rm'])


    col1 , col2 = st.columns(2)

    bar_line_plot(x=results["test_date"], y=results["estimate_power"])
    st.dataframe(results[["test_date", "test_category", "test_name"]],hide_index=True)
    # data_editor_df = df[["weight", "age", "height","name"]]

    # st.data_editor(
    # data_editor_df,
    # column_config={
    #     "name": st.column_config.TextColumn(
    #         "نام و نام خانوادگی",
    #         help="نام ورزشکاران",
    #         default="st.",
    #         max_chars=50,
    #         validate=r"^st\.[a-z_]+$",
    #     ),
    #     "age": st.column_config.NumberColumn(
    #         "سن",
    #         min_value=16,
    #         max_value=32,
    #         help="سن ورزشکاران",
    #         step=1,
    #         format="%d"
    #     ),
    #     "weight": st.column_config.NumberColumn(
    #         "وزن",
    #         min_value=50.0,
    #         max_value=130.0,
    #         help="وزن ورزشکاران",
    #         step=0.1,
    #         format="%.2f"
    #     ),
    #     "height": st.column_config.NumberColumn(
    #         "قد",
    #         min_value=50.0,
    #         max_value=130.0,
    #         help="قد ورزشکاران",
    #         step=1
    #     )
        
    # },
    # hide_index=True,
    # )

@st.fragment()
def show_athlete_history(athletes):
    col1 , col2 = st.columns([2,3])
    with col1:
        athlete_name = st.selectbox("ورزشکار", 
                        athletes["name"], 
                        placeholder="انتخاب کنید"
        )
        athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
        
        athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

        results = pd.DataFrame(list_athlete_history(athlete_id)).sort_values(by='test_date')  
    
        # Add your configuration here

        config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                        color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                        should_highlight_weekends=True, always_open=True,
                        )

        record_date = datepicker_component(config=config)
    with col2:

        st.session_state.record_data["athlete_name"] = athlete_name
        st.session_state.record_data["athlete_weight"] = athlete_weight
        st.session_state.record_data["athlete_id"] = athlete_id
        st.session_state.record_data["record_date"] = record_date
        
        if record_date['from'] and record_date['to'] is not None:
            results = results[(pd.to_datetime(results['test_date']) >= pd.to_datetime(record_date['from'].togregorian())) 
                                & 
                            (pd.to_datetime(results['test_date']) <= pd.to_datetime(record_date['to'].togregorian()))
                            ]
            
        strenght_history(results[results.test_category == "قدرت"])
    st.session_state.record_data["change"] = False

    # st.subheader(f"تاریخ منتخب از {record_date['from']:%y/%m/%d} تا {record_date['to']:%y/%m/%d}")





athletes = pd.DataFrame(list_athlete())

show_athlete_history(athletes)

st.write(st.session_state.record_data["athlete_id"])
# st.session_state.record_data["athlete_weight"] = athlete_weight

# if athlete_name:
#     df = df[["athlete_id","weight", "age", "height","name"]]
#     filtered_data = df[df.name == athlete_name]
#     st.dataframe(filtered_data)
#     st.session_state.record_data["athlete_id"] = filtered_data.athlete_id
#     st.session_state.record_data["athlete_name"] = athlete_name
#     print(st.session_state.record_data["athlete_id"])

# else:
#     st.dataframe(df)


    # print(st.session_state.record_data["athlete_id"])







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

# col1, col2, col3 = st.columns(3)


# # Group by age range
# df["age_group"] = pd.cut(df["age"], bins=[16, 18, 22, 25, 28, 30], labels=["16-18","19-21", "22-24", "25-27", "28-30"])
# age_counts = df["age_group"].value_counts().reset_index()
# age_counts.columns = ["age_group", "count"]

# # Plotly bar chart
# fig = px.bar(
#     age_counts,
#     x="age_group",
#     y="count",
#     title="Age Group Distribution",
#     labels={"age_group": "Age Group", "count": "Number of Athletes"},
#     color_discrete_sequence=["#00CC96"]
# )

# fig.update_layout(
#     xaxis_title="Age Group",
#     yaxis_title="Number of Athletes",
#     template="plotly_white"
# )


# st.plotly_chart(fig)


# # Plotly box plot
# fig = px.bar(
#     df,
#     x="name",
#     y="height",
#     title="Height Distribution",
#     labels={"name":"نام ورزشکار","height": "Height (cm)"},
#     color_discrete_sequence=["#EF553B"]
# )

# fig.update_layout(
#     xaxis_title="نام ورزشکار",
#     yaxis_title="Height (cm)",
#     template="plotly_white"
# )

# st.plotly_chart(fig)

# st.session_state.record_data["date"] = record_date
# st.session_state.record_data["athlete_name"] = athlete_name