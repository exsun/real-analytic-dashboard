"anaerobic - بی هوازی"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
import datetime

# Initialize session state for storing test results
if "anaerobic_test_data" not in st.session_state:
    st.session_state.anaerobic_test_data = []

# Function to calculate performance decrease
def calculate_performance_decrease(time_800m, time_200m):
    if time_800m > 0 and time_200m > 0:
        decrease = ((time_800m - 4 * time_200m) / time_800m) * 100
        return round(decrease, 2)
    return None
def calculate_performance(performance):
    return 100 - performance
  

# Tabs for different functionalities
tab1, tab2 = st.tabs(["Anaerobic Test Input", "📋 تاریخچه"])

# Tab 1: Anaerobic Test Input
with tab1:
    st.subheader("محاسبه کاهش عملکرد: آزمون بی‌هوازی (800m-200m)")
    with st.form("anaerobic_form", clear_on_submit=False):
        time_800m = st.number_input("زمان 800 متر (ثانیه)", min_value=0.0, step=0.1, key="time_800m")
        time_200m = st.number_input("زمان 200 متر (ثانیه)", min_value=0.0, step=0.1, key="time_200m")
        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        if time_800m > 0 and time_200m > 0:
            performance_decrease = calculate_performance_decrease(time_800m, time_200m)
            performance = calculate_performance(performance_decrease)
            selected_time = st.session_state.record_data["date"]
            
            # Save the results to session state
            st.session_state.anaerobic_test_data.append({
                "تاریخ": selected_time,
                "زمان 800 متر (ثانیه)": time_800m,
                "زمان 200 متر (ثانیه)": time_200m,
                "عملکرد (%)": performance,
                "کاهش عملکرد (%)": performance_decrease
            })
            
            # Display results
            st.metric(label="کاهش عملکرد (%)", value=f"{performance_decrease}%")
        else:
            st.error("لطفاً مقادیر معتبر وارد کنید.")

# Tab 2: History
with tab2:
    st.subheader("📋 تاریخچه آزمون‌های بی‌هوازی")
    if st.session_state.anaerobic_test_data:
        # Create DataFrame for display
        df_data = pd.DataFrame(st.session_state.anaerobic_test_data)
        # df_data["تاریخ"] = pd.Categorical(df_data["تاریخ"])
        df_data = df_data.sort_values(by="تاریخ")

        # Display the table
        st.dataframe(df_data)

        # Plot performance decrease over time
        plot = px.bar(
            df_data,
            x="تاریخ",
            y="عملکرد (%)",
            color="عملکرد (%)",  # Assign different colors based on Test Type
            barmode="group",  # Group bars by date
            title="کاهش عملکرد در طول زمان",
            labels={"تاریخ": "Date", "کاهش عملکرد (%)": "Performance Decrease (%)"}
        )
        # Ensure Plotly respects string format for dates
        plot.update_layout(
            xaxis=dict(type="category"),
            title_x=0.5,  # Center the title
        )
        st.plotly_chart(plot, use_container_width=False)
    else:
        st.info("هنوز داده‌ای ثبت نشده است.")
