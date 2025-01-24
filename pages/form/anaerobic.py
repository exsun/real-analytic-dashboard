"anaerobic - بی هوازی"
import streamlit as st
import pandas as pd
from persiantools.jdatetime import JalaliDate
import datetime

# Initialize session state for storing test results
if "anaerobic_test_data" not in st.session_state:
    st.session_state.anaerobic_test_data = []

def gregorian_to_jalali(gregorian_date):
    return JalaliDate.to_jalali(gregorian_date).strftime("%Y-%m-%d")

# Function to calculate performance decrease
def calculate_performance_decrease(time_800m, time_200m):
    if time_800m > 0 and time_200m > 0:
        decrease = ((time_800m - 4 * time_200m) / time_800m) * 100
        return round(decrease, 2)
    return None

# Function to calculate RAST power
def calculate_power(body_mass, distance, time):
    if time > 0:
        return round((body_mass * (distance**2)) / (time**3), 2)
    return 0

# Function to calculate fatigue index for RAST
def calculate_fatigue_index(max_power, min_power):
    if max_power > 0:
        return round(((max_power - min_power) / max_power) * 100, 2)
    return 0

def calculate_performance(performance):
    return 100 - performance
  

# Tabs for different functionalities
tab1, tab2, tab3, tab4 , tab5 = st.tabs(["افت عملکرد", "RAST", "wingate", "Burpee", "📋 تاریخچه"])

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

# Tab 2: RAST Test
with tab2:
    st.subheader("آزمون RAST")
   
    with st.form("rast_form", clear_on_submit=False):
        distance = 35  # Fixed distance for RAST
        sprint_times = [
            st.number_input(f"زمان دوی {i+1} (ثانیه)", min_value=0.1, step=0.01, key=f"sprint_{i+1}")
            for i in range(6)
        ]
        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        # Calculate power for each sprint
        athlete_weight = st.session_state.record_data["athlete_weight"]
        sprint_powers = [calculate_power(athlete_weight, distance, t) for t in sprint_times]
        total_power = sum(sprint_powers)  # Total Anaerobic Power
        average_power = total_power / 6 if total_power > 0 else 0
        max_power = max(sprint_powers)  # Peak Power
        min_power = min(sprint_powers)  # Lowest Power
        fatigue_index = calculate_fatigue_index(max_power, min_power)
        
        # Current time for storage
        current_time = datetime.datetime.now()
        
        # Save results to session state
        st.session_state.anaerobic_test_data.append({
            "Test": "rast",
            "تاریخ": gregorian_to_jalali(current_time),
            "توان اوج (W)": max_power,
            "توان حداقل (W)": min_power,
            "شاخص خستگی (%)": fatigue_index,
            "توان بی‌هوازی کل (W)": total_power,
            "توان میانگین (W)": average_power,
            **{f"توان دوی {i+1} (W)": sprint_powers[i] for i in range(6)}
        })
        
        # Display metrics
        st.metric(label="توان اوج (W)", value=f"{max_power} W")
        st.metric(label="توان میانگین (W)", value=f"{average_power} W")
        st.metric(label="شاخص خستگی (%)", value=f"{fatigue_index}%")
        st.metric(label="توان بی‌هوازی کل (W)", value=f"{total_power} W")


# Tab 3: Wingate Test
with tab3:
    st.subheader("آزمون وینگیت")
     
    with st.form("wingate_form", clear_on_submit=False, enter_to_submit=False):
        peak_power = st.number_input("توان اوج (وات)", min_value=0.1, step=0.1, key="peak_power")
        min_power = st.number_input("توان حداقل (وات)", min_value=0.1, step=0.1, key="min_power")
        duration = st.number_input("مدت زمان آزمون (ثانیه)", min_value=1, step=1, value=30, key="duration")  # Default 30 seconds
        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        if peak_power > 0 and min_power > 0 and duration > 0:
            # Calculate metrics
            fatigue_index = calculate_fatigue_index(peak_power, min_power)
            average_power = (peak_power + min_power) / 2  # Simplified average power calculation
            total_power = average_power * duration
            
            # Current time for storage
            current_time = datetime.datetime.now()
            
            # Save results to session state
            st.session_state.anaerobic_test_data.append({
                "Date (Gregorian)": current_time,
                "Test": "wingate",
                "تاریخ": gregorian_to_jalali(current_time),
                "توان اوج (W)": peak_power,
                "توان حداقل (W)": min_power,
                "شاخص خستگی (%)": fatigue_index,
                "توان بی‌هوازی کل (W)": total_power,
                "توان میانگین (W)": average_power
            })
            
            # Display metrics
            st.metric(label="توان اوج (W)", value=f"{peak_power} W")
            st.metric(label="توان میانگین (W)", value=f"{average_power} W")
            st.metric(label="شاخص خستگی (%)", value=f"{fatigue_index}%")
            st.metric(label="توان بی‌هوازی کل (W)", value=f"{total_power} W")

# Tab 4: Burpee Test
with tab4:
    st.subheader("آزمون بورپی")
    with st.expander("توضیحات", expanded=False):
        st.markdown("""
        **فرمول تعداد کل:**
        $$ \\text{تعداد کل} = \\text{تعداد بورپی‌های انجام‌شده در مدت آزمون} $$

        **فرمول توان بی‌هوازی متوسط:**
        $$ P_{avg} = \\frac{\\text{تعداد کل} \\cdot m \\cdot g \\cdot h}{\\text{مدت زمان آزمون (ثانیه)}} $$

        **توان بی‌هوازی کل:**
        $$ P_{total} = P_{avg} \\times 45 $$
        """)
        
    with st.form("burpee_form", clear_on_submit=True):
        burpee_count = st.number_input("تعداد کل بورپی", min_value=1, step=1, key="burpee_count")
        jump_height = st.number_input("میانگین ارتفاع پرش (متر)", min_value=0.1, step=0.01, key="jump_height")
        duration = st.number_input("مدت زمان آزمون (ثانیه)", min_value=1, value=45, step=1, key="burpee_duration")
        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        athlete_weight = st.session_state.record_data["athlete_weight"]
        if burpee_count > 0 and athlete_weight > 0 and jump_height > 0:

            g = 9.8  # Gravitational acceleration
            
            # Calculate metrics
            avg_power = round((burpee_count * athlete_weight * g * jump_height) / duration , 2)
            total_power = round(avg_power * duration, 2)
            
            # Current time for storage
            current_time = datetime.datetime.now()
            
            # Save results to session state
            st.session_state.anaerobic_test_data.append({
                "Date (Gregorian)": current_time,
                "Test": "burpee",
                "تاریخ": gregorian_to_jalali(current_time),
                "تعداد کل بورپی": burpee_count,
                "توان بی‌هوازی متوسط (W)": avg_power,
                "توان بی‌هوازی کل (W)": total_power
            })
            
            # Display metrics
            st.metric(label="تعداد کل بورپی", value=burpee_count)
            st.metric(label="توان بی‌هوازی متوسط (W)", value=f"{avg_power} W")
            st.metric(label="توان بی‌هوازی کل (W)", value=f"{total_power} W")

# Tab 5: History
with tab5:
    st.subheader("📋 تاریخچه آزمون‌های بی‌هوازی")


    if st.session_state.anaerobic_test_data:
        # Create DataFrame for display
        df_data = pd.DataFrame(st.session_state.anaerobic_test_data)
    #     # df_data["تاریخ"] = pd.Categorical(df_data["تاریخ"])
    #     df_data = df_data.sort_values(by="تاریخ")

    #     # Display the table
        st.dataframe(df_data)

    #     # Plot performance decrease over time
    #     plot = px.bar(
    #         df_data,
    #         x="تاریخ",
    #         y="عملکرد (%)",
    #         color="عملکرد (%)",  # Assign different colors based on Test Type
    #         barmode="group",  # Group bars by date
    #         title="کاهش عملکرد در طول زمان",
    #         labels={"تاریخ": "Date", "کاهش عملکرد (%)": "Performance Decrease (%)"}
    #     )
    #     # Ensure Plotly respects string format for dates
    #     plot.update_layout(
    #         xaxis=dict(type="category"),
    #         title_x=0.5,  # Center the title
    #     )
    #     st.plotly_chart(plot, use_container_width=False)
    # else:
    #     st.info("هنوز داده‌ای ثبت نشده است.")
