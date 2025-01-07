"anaerobic - بی هوازی"
import streamlit as st
import pandas as pd
import plotly.express as px
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
tab1, tab2, tab3, tab4 , tab5 = st.tabs(["افت عملکرد ۸۰۰ متر", "RAST", "wingate", "Burpee", "📋 تاریخچه"])

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
# Tab 2: RAST Test
with tab2:
    st.subheader("آزمون RAST")
    st.markdown("""
    **فرمول توان:** 
    $$ P = \\frac{m \\cdot d^2}{t^3} $$

    **شاخص خستگی:** 
    $$ \\text{شاخص خستگی (\%)} = \\frac{\\text{توان اوج} - \\text{توان حداقل}}{\\text{توان اوج}} \\times ۱۰۰ $$

    **توان بی‌هوازی کل:** مجموع توان شش دوی سرعت.
    """)
    
    with st.form("rast_form", clear_on_submit=False):
        body_mass = st.number_input("وزن بدن (کیلوگرم)", min_value=1.0, step=0.1, key="body_mass")
        distance = 35  # Fixed distance for RAST
        sprint_times = [
            st.number_input(f"زمان دوی {i+1} (ثانیه)", min_value=0.1, step=0.01, key=f"sprint_{i+1}")
            for i in range(6)
        ]
        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        # Calculate power for each sprint
        sprint_powers = [calculate_power(body_mass, distance, t) for t in sprint_times]
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
    with st.expander("توضیحات", expanded=False):

        st.markdown("""
        **فرمول توان اوج:** 
        $$ \\text{توان اوج} = \\text{بیشترین توان تولید شده در هر دوره} $$

        **فرمول توان میانگین:** 
        $$ \\text{توان میانگین} = \\frac{\\text{توان کل}}{\\text{مدت زمان آزمون (ثانیه)}} $$

        **شاخص خستگی:** 
        $$ \\text{شاخص خستگی (\%)} = \\frac{\\text{توان اوج} - \\text{توان حداقل}}{\\text{توان اوج}} \\times ۱۰۰ $$

        **توان بی‌هوازی کل:** 
        $$ \\text{توان کل} = \\text{توان میانگین} \\times \\text{مدت زمان آزمون (ثانیه)} $$
        """)

        st.markdown("""
        # آزمون وینگیت (Wingate Test)

        **آزمون وینگیت** یکی از معتبرترین تست‌های بی‌هوازی است که برای ارزیابی توان بی‌هوازی (Anaerobic Power) و شاخص خستگی (Fatigue Index) طراحی شده است. این آزمون معمولاً با استفاده از **دوچرخه ارگومتر** (Cycle Ergometer) انجام می‌شود.

        ---

        ## 🎯 **هدف آزمون وینگیت**
        این آزمون به ارزیابی موارد زیر می‌پردازد:
        1. **توان اوج (Peak Power)**: بالاترین توان تولید شده در طول آزمون.
        2. **توان میانگین (Average Power)**: میانگین توان تولید شده در طول آزمون.
        3. **شاخص خستگی (Fatigue Index)**: میزان کاهش توان از ابتدای آزمون تا انتها.
        4. **توان کل بی‌هوازی (Total Anaerobic Power)**: مجموع انرژی تولید شده در طول آزمون.

        ---

        ## ⚙️ **مراحل اجرای آزمون وینگیت**

        ### 1. **آماده‌سازی**
        - آزمون روی **دوچرخه ارگومتر** انجام می‌شود.
        - وزن بدن فرد اندازه‌گیری شده و برای تنظیم مقاومت دوچرخه استفاده می‌شود (معمولاً **7.5٪ وزن بدن** به‌عنوان مقاومت در نظر گرفته می‌شود).
        - فرد باید به مدت ۵ تا ۱۰ دقیقه گرم کند.

        ### 2. **اجرای آزمون**
        - **مدت آزمون**: ۳۰ ثانیه.
        - فرد باید با حداکثر تلاش ممکن رکاب بزند.
        - مقاومت دوچرخه ثابت است و داده‌های توان در لحظه ثبت می‌شوند.

        ### 3. **اندازه‌گیری متغیرها**
        - **توان اوج (Peak Power)**: بیشترین توان تولید شده در آزمون.
        - **توان حداقل (Minimum Power)**: کمترین توان ثبت‌شده در آزمون.
        - **توان میانگین (Average Power)**: میانگین توان تولید شده.
        - **شاخص خستگی (Fatigue Index)**: میزان کاهش توان از توان اوج تا توان حداقل.

        ---

        ## 📐 **فرمول‌ها و محاسبات**

        ### 1. **توان اوج (Peak Power):**
        \[
        P_{peak} = \text{بیشترین توان تولید شده در آزمون}
        \]

        ### 2. **توان میانگین (Average Power):**
        \[
        P_{avg} = \frac{\text{توان کل}}{\text{مدت زمان آزمون (ثانیه)}}
        \]

        ### 3. **شاخص خستگی (Fatigue Index):**
        \[
        FI = \frac{P_{peak} - P_{min}}{P_{peak}} \times 100
        \]
        - \(P_{peak}\): توان اوج.
        - \(P_{min}\): توان حداقل.

        ### 4. **توان کل بی‌هوازی (Total Anaerobic Power):**
        \[
        P_{total} = P_{avg} \times T
        \]
        - \(T\): مدت زمان آزمون (ثانیه).

        ---

        ## 🔢 **ورودی‌های موردنیاز**
        برای اجرای آزمون و محاسبات، ورودی‌های زیر موردنیاز است:
        1. **توان اوج (Peak Power)**: بیشترین توان تولید شده در طول آزمون.
        2. **توان حداقل (Minimum Power)**: کمترین توان ثبت‌شده.
        3. **مدت زمان آزمون (Duration)**: معمولاً ۳۰ ثانیه.

        ---

        ## 📊 **خروجی‌ها و تفسیر نتایج**

        ### 1. **توان اوج (Peak Power)**:
        - نشان‌دهنده ظرفیت بی‌هوازی فرد.
        - افراد با ظرفیت بی‌هوازی بالا، توان اوج بیشتری دارند.

        ### 2. **توان میانگین (Average Power)**:
        - نشان‌دهنده میانگین تولید توان در طول آزمون.

        ### 3. **شاخص خستگی (Fatigue Index)**:
        - نشان‌دهنده میزان افت توان است.
        - مقدار بالا = کاهش سریع توان.
        - مقدار پایین = حفظ توان و استقامت بیشتر.

        ### 4. **توان کل بی‌هوازی (Total Anaerobic Power)**:
        - نشان‌دهنده مجموع انرژی تولید شده و معیار کلی عملکرد بی‌هوازی است.

        ---

        ## 🏁 **جمع‌بندی**
        **آزمون وینگیت** به شما کمک می‌کند تا:
        - **ظرفیت بی‌هوازی** خود را ارزیابی کنید.
        - **میزان خستگی** و افت توان را اندازه‌گیری کنید.
        - نقاط قوت و ضعف سیستم بی‌هوازی خود را شناسایی کنید.

        این آزمون برای ورزشکاران رشته‌های نیازمند سرعت و توان بالا مانند فوتبال، کشتی، بسکتبال و دوومیدانی بسیار کاربردی است.


        
        """)
        
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
        body_mass = st.number_input("وزن بدن (کیلوگرم)", min_value=1.0, step=0.1, key="burpee_body_mass")
        jump_height = st.number_input("میانگین ارتفاع پرش (متر)", min_value=0.1, step=0.01, key="jump_height")
        duration = st.number_input("مدت زمان آزمون (ثانیه)", min_value=1, value=45, step=1, key="burpee_duration")
        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        if burpee_count > 0 and body_mass > 0 and jump_height > 0:
            
            g = 9.8  # Gravitational acceleration
            
            # Calculate metrics
            avg_power = (burpee_count * body_mass * g * jump_height) / duration
            total_power = avg_power * duration
            
            # Current time for storage
            current_time = datetime.datetime.now()
            
            # Save results to session state
            st.session_state.anaerobic_test_data.append({
                "Date (Gregorian)": current_time,
                "Test": "burpee",
                "تاریخ": gregorian_to_jalali(current_time),
                "تعداد کل بورپی": burpee_count,
                "توان بی‌هوازی متوسط (W)": round(avg_power, 2),
                "توان بی‌هوازی کل (W)": round(total_power, 2)
            })
            
            # Display metrics
            st.metric(label="تعداد کل بورپی", value=burpee_count)
            st.metric(label="توان بی‌هوازی متوسط (W)", value=f"{round(avg_power, 2)} W")
            st.metric(label="توان بی‌هوازی کل (W)", value=f"{round(total_power, 2)} W")

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
