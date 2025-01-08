"muscle_stamina - استقامت عضلانی"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
import datetime

# Initialize session state for storing test results
if "muscle_stamina_test_data" not in st.session_state:
    st.session_state.muscle_stamina_test_data = []

tab1, tab2 = st.tabs(["آزمون استقامت عضلانی", "📋 تاریخچه"])

with tab1:
    with st.form("muscle_stamina_tests_form", clear_on_submit=False):

        st.subheader("آزمون استقامت عضلانی")
        st.subheader("دراز و نشست با توپ مدیسین بال (۱۰٪ وزن بدن)")
        body_mass = st.number_input("وزن بدن (کیلوگرم)", min_value=1.0, step=0.1, key="body_mass")
        situp_reps = st.number_input("تعداد دراز و نشست (در یک دقیقه)", min_value=0, step=1, key="situp_reps")
        pullup_reps = st.number_input("تعداد بارفیکس", min_value=0, step=1, key="pullup_reps")
        dip_reps = st.number_input("تعداد دیپ پارالل", min_value=0, step=1, key="dip_reps")

        submitted = st.form_submit_button("ثبت")

        if submitted:
            medicine_ball_weight = body_mass * 0.1
            selected_time = st.session_state.record_data["date"]

            # Save results to session state
            if "muscular_endurance_data" not in st.session_state:
                st.session_state.muscular_endurance_data = []

            muscle_stamina_test_data = [{
                "تاریخ": selected_time,
                "وزن بدن": body_mass,
                "وزن توپ مدیسین بال": round(medicine_ball_weight, 2),
                "دراز و نشست": situp_reps,
                "بارفیکس": pullup_reps,
                "دیپ پارالل": dip_reps
            }]

  
    

            st.session_state.muscle_stamina_test_data.append(muscle_stamina_test_data[0])

            df = pd.DataFrame(muscle_stamina_test_data).sort_values(by="تاریخ")
        

            # Melt the DataFrame for combining metrics
            melted_df = pd.melt(
                df,
                id_vars=["تاریخ"],
                value_vars=["دراز و نشست", "بارفیکس", "دیپ پارالل"],
                var_name="Count Type",
                value_name="Count (centemeter)"
            )

            # Create Grouped Bar Plot
            fig = px.bar(
                melted_df,
                x="تاریخ",
                y="Count (centemeter)",
                color="Count Type",
                barmode="group",
                title="تغییرات زمانی در آزمون‌های چابکی",
                labels={"تاریخ": "تاریخ", "Count (centemeter)": "مدت زمان (ثانیه)", "Count Type": "نوع آزمون"}

            )

            # Display the Bar Plot
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)

with tab2:
    # Historical Bar Chart
    if st.session_state.muscle_stamina_test_data:
        df_history = pd.DataFrame(st.session_state.muscle_stamina_test_data).sort_values(by="تاریخ")

        # Convert Gregorian to Jalali for display

        # Melt the DataFrame for combining metrics
        history_fig_melted_df = pd.melt(
            df_history,
            id_vars=["تاریخ"],
            value_vars=["دراز و نشست", "بارفیکس", "دیپ پارالل"],
            var_name="Count Type",
            value_name="Count (centemeter)"
        )

        # Create Grouped Bar Plot
        history_fig = px.bar(
            history_fig_melted_df,
            x="تاریخ",
            y="Count (centemeter)",
            color="Count Type",
            barmode="group",
            title="تغییرات زمانی در آزمون‌های چابکی",
            labels={"تاریخ": "تاریخ", "Count (centemeter)": "مدت زمان (ثانیه)", "Count Type": "نوع آزمون"}

        )

        # Display the Bar Plot
        st.plotly_chart(history_fig, use_container_width=True)

        st.dataframe(df_history)

    else:
        st.info("هنوز داده‌ای ثبت نشده است.")
