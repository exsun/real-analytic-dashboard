import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import time


@st.cache_data
def get_data():
    """Generate random sales data for Widget A through Widget Z"""

    product_names = ["Widget " + letter for letter in string.ascii_uppercase]
    average_daily_sales = np.random.normal(1_000, 300, len(product_names))
    products = dict(zip(product_names, average_daily_sales))

    data = pd.DataFrame({})
    sales_dates = np.arange(date(2023, 1, 1), date(2024, 1, 1), timedelta(days=1))
    for product, sales in products.items():
        data[product] = np.random.normal(sales, 300, len(sales_dates)).round(2)
    data.index = sales_dates
    data.index = data.index.date
    return data


@st.fragment
def show_daily_sales(data):
    time.sleep(1)
    with st.container(height=100):
        selected_date = st.date_input(
            "Pick a day ",
            value=date(2023, 1, 1),
            min_value=date(2023, 1, 1),
            max_value=date(2023, 12, 31),
            key="selected_date",
        )

    if "previous_date" not in st.session_state:
        st.session_state.previous_date = selected_date
    previous_date = st.session_state.previous_date
    st.session_state.previous_date = selected_date
    is_new_month = selected_date.replace(day=1) != previous_date.replace(day=1)
    if is_new_month:
        st.rerun()

    with st.container(height=510):
        st.header(f"Best sellers, {selected_date:%m/%d/%y}")
        top_ten = data.loc[selected_date].sort_values(ascending=False)[0:10]
        cols = st.columns([1, 4])
        cols[0].dataframe(top_ten)
        cols[1].bar_chart(top_ten)

    with st.container(height=510):
        st.header(f"Worst sellers, {selected_date:%m/%d/%y}")
        bottom_ten = data.loc[selected_date].sort_values()[0:10]
        cols = st.columns([1, 4])
        cols[0].dataframe(bottom_ten)
        cols[1].bar_chart(bottom_ten)


def show_monthly_sales(data):
    time.sleep(1)
    selected_date = st.session_state.selected_date
    this_month = selected_date.replace(day=1)
    next_month = (selected_date.replace(day=28) + timedelta(days=4)).replace(day=1)

    st.container(height=100, border=False)
    with st.container(height=510):
        st.header(f"Daily sales for all products, {this_month:%B %Y}")
        monthly_sales = data[(data.index < next_month) & (data.index >= this_month)]
        st.write(monthly_sales)
    with st.container(height=510):
        st.header(f"Total sales for all products, {this_month:%B %Y}")
        st.bar_chart(monthly_sales.sum())


st.title("Daily vs monthly sales, by product")
st.markdown("This app shows the 2023 daily sales for Widget A through Widget Z.")

data = get_data()
print(data)
daily, monthly = st.columns(2)
with daily:
    show_daily_sales(data)
with monthly:
    show_monthly_sales(data)


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_recent_data(last_timestamp):
    """Generate and return data from last timestamp to now, at most 60 seconds."""
    now = datetime.now()
    if now - last_timestamp > timedelta(seconds=60):
        last_timestamp = now - timedelta(seconds=60)
    sample_time = timedelta(seconds=0.5)  # time between data points
    next_timestamp = last_timestamp + sample_time
    timestamps = np.arange(next_timestamp, now, sample_time)
    sample_values = np.random.randn(len(timestamps), 2)

    data = pd.DataFrame(sample_values, index=timestamps, columns=["A", "B"])
    return data


if "data" not in st.session_state:
    st.session_state.data = get_recent_data(datetime.now() - timedelta(seconds=60))

if "stream" not in st.session_state:
    st.session_state.stream = False


def toggle_streaming():
    st.session_state.stream = not st.session_state.stream


st.title("Data feed")
st.sidebar.slider(
    "Check for updates every: (seconds)", 0.5, 5.0, value=1.0, key="run_every"
)
st.sidebar.button(
    "Start streaming", disabled=st.session_state.stream, on_click=toggle_streaming
)
st.sidebar.button(
    "Stop streaming", disabled=not st.session_state.stream, on_click=toggle_streaming
)

if st.session_state.stream is True:
    run_every = st.session_state.run_every
else:
    run_every = None


@st.fragment(run_every=run_every)
def show_latest_data():
    last_timestamp = st.session_state.data.index[-1]
    st.session_state.data = pd.concat(
        [st.session_state.data, get_recent_data(last_timestamp)]
    )
    st.session_state.data = st.session_state.data[-100:]
    st.line_chart(st.session_state.data)


show_latest_data()