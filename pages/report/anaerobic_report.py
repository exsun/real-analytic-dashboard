import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

# Sample Data for Testing
if "anaerobic_test_data" not in st.session_state:
    st.session_state.anaerobic_test_data = [
        {
            "Date (Gregorian)": datetime.datetime(2023, 12, 31),
            "test_type": "Performance Decrease",
            "تاریخ": "1402-10-10",
            "Performance Decrease (%)": 15.0
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 1, 1),
            "test_type": "RAST",
            "تاریخ": "1402-10-11",
            "Peak Power (W)": 350,
            "Average Power (W)": 250,
            "Fatigue Index (%)": 20
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 2, 1),
            "test_type": "RAST",
            "تاریخ": "1402-11-11",
            "Peak Power (W)": 460,
            "Average Power (W)": 12,
            "Fatigue Index (%)": 55
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 1, 2),
            "test_type": "Wingate",
            "تاریخ": "1402-10-12",
            "Peak Power (W)": 400,
            "Average Power (W)": 300,
            "Fatigue Index (%)": 25
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 2, 2),
            "test_type": "Wingate",
            "تاریخ": "1402-11-12",
            "Peak Power (W)": 500,
            "Average Power (W)": 350,
            "Fatigue Index (%)": 60
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 3, 2),
            "test_type": "Wingate",
            "تاریخ": "1402-12-12",
            "Peak Power (W)": 450,
            "Average Power (W)": 300,
            "Fatigue Index (%)": 75
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 1, 3),
            "test_type": "Burpee",
            "تاریخ": "1402-10-13",
            "Total Burpees": 40,
            "Average Anaerobic Power (W)": 50
        },
        {
            "Date (Gregorian)": datetime.datetime(2024, 2, 3),
            "test_type": "Burpee",
            "تاریخ": "1402-11-13",
            "Total Burpees": 65,
            "Average Anaerobic Power (W)": 67
        }
    ]

# Convert Data to DataFrame
df_tests = pd.DataFrame(st.session_state.anaerobic_test_data)

# Sidebar for Date Selection
st.subheader("انتخاب تاریخ‌ها برای مقایسه")

# Filter Data Based on Selected Dates

def filter_data(test_type):
    filtered_data = df_tests[df_tests["test_type"] == test_type]

    selected_dates = st.multiselect("تاریخ‌ها را انتخاب کنید:", options=filtered_data["تاریخ"].unique(), key=test_type)

    filtered_data = df_tests[df_tests["تاریخ"].isin(selected_dates)]

    return filtered_data


# Function to Create Radar Chart
def create_radar_chart(data, metrics, title):
    if data.empty:
        st.warning("لطفاً تاریخ‌های معتبر انتخاب کنید.")
        return
    # Melt data for radar chart
    melted_data = pd.melt(
        data,
        id_vars=["تاریخ"],
        value_vars=metrics,
        var_name="Metric",
        value_name="Value"
    )

    # Create radar chart
    fig = px.line_polar(
        melted_data,
        r="Value",
        theta="Metric",
        color="تاریخ",
        line_close=True,
        title=title
    )
    fig.update_traces(fill="toself")
    st.plotly_chart(fig, use_container_width=True)

# Tabs for Each Test
tab1, tab2, tab3, tab4 = st.tabs(["Performance Decrease", "RAST", "Wingate", "Burpee"])

# Performance Decrease Radar Chart
with tab1:
    st.subheader("Radar Chart: Performance Decrease")
    performance_data = filter_data(test_type="Performance Decrease")
    create_radar_chart(
        performance_data,
        metrics=["Performance Decrease (%)"],
        title="Radar Chart: Performance Decrease (%)"
    )

# RAST Radar Chart
with tab2:
    st.subheader("Radar Chart: RAST")
    rast_data = filter_data(test_type="RAST")
    create_radar_chart(
        rast_data,
        metrics=["Peak Power (W)", "Average Power (W)", "Fatigue Index (%)"],
        title="Radar Chart: RAST Test"
    )

# Wingate Radar Chart
with tab3:
    st.subheader("Radar Chart: Wingate")
    wingate_data = filter_data(test_type="Wingate")
    create_radar_chart(
        wingate_data,
        metrics=["Peak Power (W)", "Average Power (W)", "Fatigue Index (%)"],
        title="Radar Chart: Wingate Test"
    )

# Burpee Radar Chart
with tab4:
    st.subheader("Radar Chart: Burpee")
    burpee_data = filter_data(test_type="Burpee")
    create_radar_chart(
        burpee_data,
        metrics=["Total Burpees", "Average Anaerobic Power (W)"],
        title="Radar Chart: Burpee Test"
    )
