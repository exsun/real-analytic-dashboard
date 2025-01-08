"flexibility - انعطاف پذیری"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
import datetime

# Initialize session state for storing test results
if "flexibility_test_data" not in st.session_state:
    st.session_state.flexibility_test_data = []

tab1, tab2 = st.tabs(["آزمون چابکی", "📋 تاریخچه"])

with tab1:
    st.subheader("آزمون‌های انعطاف‌پذیری")

    with st.form("flexibility_tests_form", clear_on_submit=False):

        reach_distance = st.number_input("فاصله نوک انگشتان (سانتی‌متر)", step=0.1, key="reach_distance")
        shoulder_height = st.number_input("بالا آوردن شانه (سانتی‌متر)", step=0.1, key="shoulder_height")
        upper_body_open = st.number_input("باز شدن بالا تنه (سانتی‌متر)", step=0.1, key="upper_body_open")

        submitted = st.form_submit_button("ثبت")

    if submitted:
        selected_time = st.session_state.record_data["date"]

        # Save results

        flexibility_test_data = [{
            "Test": "انعطاف پذیری",
            "تاریخ": selected_time,
            "فاصله نوک انگشتان": reach_distance,
            "بالا آوردن شانه": shoulder_height,
            "باز شدن بالاتنه": upper_body_open
        }]

        st.session_state.flexibility_test_data.append(flexibility_test_data[0])


        df = pd.DataFrame(flexibility_test_data).sort_values(by="تاریخ")
        
        # Convert Gregorian to Jalali for display

        # Melt the DataFrame for combining metrics
        melted_df = pd.melt(
            df,
            id_vars=["تاریخ"],
            value_vars=["فاصله نوک انگشتان", "بالا آوردن شانه", "باز شدن بالاتنه"],
            var_name="Distance Type",
            value_name="Distance (centemeter)"
        )

        # Create Grouped Bar Plot
        fig = px.bar(
            melted_df,
            x="تاریخ",
            y="Distance (centemeter)",
            color="Distance Type",
            barmode="group",
            title="تغییرات زمانی در آزمون‌های چابکی",
            labels={"تاریخ": "تاریخ", "Distance (centemeter)": "مدت زمان (ثانیه)", "Distance Type": "نوع آزمون"}

        )

        # Display the Bar Plot
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df)

with tab2:
    # Historical Bar Chart
    if st.session_state.flexibility_test_data:
        df_history = pd.DataFrame(st.session_state.flexibility_test_data).sort_values(by="تاریخ")

        # Convert Gregorian to Jalali for display

        # Melt the DataFrame for combining metrics
        history_fig_melted_df = pd.melt(
            df_history,
            id_vars=["تاریخ"],
            value_vars=["فاصله نوک انگشتان", "بالا آوردن شانه", "باز شدن بالاتنه"],
            var_name="Distance Type",
            value_name="Distance (centemeter)"
        )

        # Create Grouped Bar Plot
        history_fig = px.bar(
            history_fig_melted_df,
            x="تاریخ",
            y="Distance (centemeter)",
            color="Distance Type",
            barmode="group",
            title="تغییرات زمانی در آزمون‌های چابکی",
            labels={"تاریخ": "تاریخ", "Distance (centemeter)": "مدت زمان (ثانیه)", "Distance Type": "نوع آزمون"}

        )

        # Display the Bar Plot
        st.plotly_chart(history_fig, use_container_width=True)

        st.dataframe(df_history)

    else:
        st.info("هنوز داده‌ای ثبت نشده است.")
