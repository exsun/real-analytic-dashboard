import numpy as np
import pandas as pd
import streamlit as st
from persiantools.jdatetime import JalaliDate
from datetime import datetime
from streamlit_nej_datepicker import datepicker_component, Config

from faker import Faker
@st.cache_data
def get_profile_dataset(number_of_items: int = 20, seed: int = 0) -> pd.DataFrame:
    new_data = []

    fake = Faker()
    np.random.seed(seed)
    Faker.seed(seed)

    for i in range(number_of_items):
        profile = fake.profile()
        new_data.append(
            {
                "name": profile["name"],
                "daily_activity": np.random.rand(25),
                "activity": np.random.randint(2, 90, size=12),
            }
        )

    profile_df = pd.DataFrame(new_data)
    return profile_df


column_configuration = {
    "name": st.column_config.TextColumn(
        "Name", help="The name of the user", max_chars=100, width="medium"
    ),
    "activity": st.column_config.LineChartColumn(
        "Activity (1 year)",
        help="The user's activity over the last 1 year",
        width="large",
        y_min=0,
        y_max=100,
    ),
    "daily_activity": st.column_config.BarChartColumn(
        "Activity (daily)",
        help="The user's activity in the last 25 days",
        width="medium",
        y_min=0,
        y_max=1,
    ),
}

select, compare = st.tabs(["Select members", "Compare selected"])

with select:
    st.header("All members")

    df = get_profile_dataset()
    table, timelime  = st.columns([4,1], vertical_alignment="top")

    with table:
        st.subheader("ورزشکاران")
        event = st.dataframe(
            df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )
    with timelime:
        config = Config(dark_mode=True, locale="fa", color_primary="#ff4b4b",
                color_primary_light="#ff9494", selection_mode="range",closed_view="button",
                should_highlight_weekends=True, always_open=True,
                )

        record_date = datepicker_component(config=config)

    st.header("Selected members")
    people = event.selection.rows
    filtered_df = df.iloc[people]
    st.dataframe(
        filtered_df,
        column_config=column_configuration,
        use_container_width=True,
    )

with compare:
    activity_df = {}
    for person in people:
        activity_df[df.iloc[person]["name"]] = df.iloc[person]["activity"]
    activity_df = pd.DataFrame(activity_df)

    daily_activity_df = {}
    for person in people:
        daily_activity_df[df.iloc[person]["name"]] = df.iloc[person]["daily_activity"]
    daily_activity_df = pd.DataFrame(daily_activity_df)

    if len(people) > 0:
        st.header("Daily activity comparison")
        st.bar_chart(daily_activity_df)
        st.header("Yearly activity comparison")
        st.line_chart(activity_df)
    else:
        st.markdown("No members selected.")



@st.dialog("مشخصات ورزشکار")
def athelthe():
    name = st.text_input("name")
    age = st.text_input("age")
    gender = st.text_input("gender")
    weight = st.text_input("weight")
    height = st.text_input("height")
    style = st.selectbox("style", ["free-style", "greco-roman"])

    years = list(range(JalaliDate.today().year+1, 1390, -1))
    months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    days = list(range(1, 32))

    col21, col22, col23 = st.columns(3,vertical_alignment="top")

    with col21:
        selected_year = st.selectbox("سال", years, index=years.index(JalaliDate.today().year))
    with col22:
        selected_month = st.selectbox("ماه", months, index=JalaliDate.today().month - 1)
    with col23:
        selected_day = st.selectbox("روز", days, index=JalaliDate.today().day - 1)

    if st.button("Submit"):
        st.session_state.athelthe = ({
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "style": style
            })
        st.rerun()

# if "athelthe" not in st.session_state:
st.write("ورزشکار جدید اضافه کنید")
if st.button("ورزشکار جدید"):
    athelthe()

if st.session_state.athelthe:
 
    f"You athelthe: {st.session_state.athelthe['name']}"
    st.json(st.session_state.athelthe)

else:
    st.session_state.athelthe = {}
