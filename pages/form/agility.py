"agility - چابکی"
import streamlit as st
import pandas as pd
import plotly.express as px
from persiantools.jdatetime import JalaliDate
import datetime

# Initialize session state for storing test results
if "agility_test_data" not in st.session_state:
    st.session_state.agility_test_data = []
tab1, tab2, tab3 = st.tabs(["آزمون چابکی", "توضیحات", "📋 تاریخچه"])

# Tab 1: Zone Agility Test
with tab1:
    st.subheader("آزمون چابکی ویژه کشتی")
    st.markdown("""
    **فرمول امتیاز چابکی:** 
    $$ A = \\frac{\\text{تعداد تغییر جهت}}{\\text{مدت زمان آزمون (ثانیه)}} $$
    """)
    
    with st.form("zone_agility_form", clear_on_submit=False):
        # direction_changes = st.number_input("تعداد تغییر جهت", min_value=1, step=1, key="direction_changes")
        specefic_duration = st.number_input("مدت زمان آزمون ویژه کشتی (ثانیه)", min_value=1, value=20, step=1, key="specefic_duration")
        bear_duration = st.number_input("مدت زمان آزمون خرسی (ثانیه)", min_value=1, value=20, step=1, key="bear_duration")
        zone_duration = st.number_input("مدت زمان آزمون منطقه zone (ثانیه)", min_value=1, value=20, step=1, key="zone_duration")
        T_duration = st.number_input("مدت زمان آزمون T (ثانیه)", min_value=1, value=20, step=1, key="T_duration")
        illinois_duration = st.number_input("مدت زمان آزمون illinois (ثانیه)", min_value=1, value=20, step=1, key="illinois_duration")

        submitted = st.form_submit_button("محاسبه")
    
    if submitted:
        # if direction_changes > 0 and duration > 0:
            selected_time = st.session_state.record_data["date"]

            
            # Save results to session state
            st.session_state.agility_test_data.append({
                "Test": "چابکی",
                "specefic_duration": specefic_duration,
                "bear_duration": bear_duration,
                "zone_duration": zone_duration,
                "T_duration": T_duration,
                "illinois_duration": illinois_duration,
                "تاریخ": selected_time,
            })
            agility_test_data = [{
                "Test": "چابکی",
                "specefic_duration": specefic_duration,
                "bear_duration": bear_duration,
                "zone_duration": zone_duration,
                "T_duration": T_duration,
                "illinois_duration": illinois_duration,
                "تاریخ": selected_time,
            }]

            # Display metrics
            # st.metric(label="امتیاز چابکی", value=f"{round(agility_score, 2)} تغییر جهت/ثانیه")
            # st.metric(label="امتیاز چابکی", value=f"{round(agility_score, 2)} تغییر جهت/ثانیه")

            # st.metric(label="آزمون ویژه کشتی (ثانیه)", value=f"{specefic_duration}")
            # st.metric(label="آزمون خرسی (ثانیه)", value=f"{bear_duration}")
            # st.metric(label="آزمون منطقه zone (ثانیه)", value=f"{zone_duration}")
            # st.metric(label="آزمون T (ثانیه)", value=f"{T_duration}")
            # st.metric(label="آزمون illinois (ثانیه)", value=f"{illinois_duration}")

            df = pd.DataFrame(agility_test_data).sort_values(by="تاریخ")
            
            # Convert Gregorian to Jalali for display

            # Melt the DataFrame for combining metrics
            melted_df = pd.melt(
                df,
                id_vars=["تاریخ"],
                value_vars=["specefic_duration", "bear_duration", "zone_duration", "T_duration", "illinois_duration"],
                var_name="Duration Type",
                value_name="Duration (seconds)"
            )

            # Create Grouped Bar Plot
            fig = px.bar(
                melted_df,
                x="تاریخ",
                y="Duration (seconds)",
                color="Duration Type",
                barmode="group",
                title="تغییرات زمانی در آزمون‌های چابکی",
                labels={"تاریخ": "تاریخ", "Duration (seconds)": "مدت زمان (ثانیه)", "Duration Type": "نوع آزمون"}

            )

            # Display the Bar Plot
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)

with tab2:
    with st.expander("توضیحات آزمون خرسی"):
        st.markdown("""
            ## آزمون خرسی (Bear Crawl Test)

            **هدف آزمون:** 
            - ارزیابی قدرت، استقامت و چابکی کشتی‌گیر.

            ---

            ## ⚙️ **مراحل اجرای آزمون**
            1. یک مسیر با طول مشخص (مثلاً **۱۰ متر**) تعیین کنید.
            2. کشتی‌گیر باید با استفاده از حرکت خرسی مسیر را طی کند:
            - دست‌ها و پاها روی زمین.
            - بدن نزدیک به زمین.
            3. زمان تکمیل مسیر ثبت می‌شود.

            ---

            ## 📐 **فرمول‌ها و محاسبات**

            ### 1. **زمان آزمون:**
            \[
            T = \text{مدت زمان تکمیل مسیر (ثانیه)}
            \]

            ### 2. **توان متوسط:**
            \[
            P = \\frac{m \\cdot d}{T}
            \]
            - \( m \): وزن بدن (کیلوگرم).
            - \( d \): طول مسیر (متر).
            - \( T \): زمان تکمیل مسیر (ثانیه).

            ---

            ## 🔢 **ورودی‌های موردنیاز**
            1. وزن بدن.
            2. طول مسیر.
            3. زمان تکمیل مسیر.

            ---

            ## 📊 **خروجی‌ها**
            - **زمان آزمون (ثانیه):** مدت زمان تکمیل مسیر.
            - **توان متوسط (W):** توان تخمینی بر اساس وزن بدن و زمان.


        """)

    with st.expander("توضیحات آزمون زون zone"):
        st.markdown("""
            ## آزمون چابکی زون (Zone Agility Test)

            **هدف آزمون:** 
            - ارزیابی توانایی کشتی‌گیر برای تغییر جهت سریع در محدوده مشخص.

            ---

            ## ⚙️ **مراحل اجرای آزمون**
            1. محدوده‌ای به ابعاد **۵x۵ متر** مشخص کنید.
            2. کشتی‌گیر باید به‌سرعت در جهات تصادفی که توسط مربی مشخص می‌شود حرکت کند.
            3. مدت زمان آزمون معمولاً **۲۰ ثانیه** است.
            4. تعداد تغییرات جهت در طول آزمون ثبت می‌شود.

            ---

            ## 📐 **فرمول و محاسبات**
            **امتیاز چابکی:** 
            $$ A = \\frac{\\text{تعداد تغییر جهت}}{\\text{مدت زمان آزمون (ثانیه)}} $$

            ---

            ## 🔢 **ورودی‌های موردنیاز**
            1. تعداد تغییرات جهت.
            2. مدت زمان آزمون.

            ---

            ## 📊 **خروجی‌ها**
            - **امتیاز چابکی (A):** تعداد تغییرات جهت در هر ثانیه.


        """)

    with st.expander("توضیحات آزمون T"):
        st.markdown("""
            ## آزمون چابکی T (T Agility Test)

            **هدف آزمون:** 
            - ارزیابی توانایی کشتی‌گیر برای تغییر جهت به جلو، عقب و طرفین.

            ---

            ## ⚙️ **مراحل اجرای آزمون**
            1. مسیری به شکل حرف T تنظیم کنید:
            - نقطه شروع (پایین T) تا بالای T (۱۰ متر).
            - حرکت به طرفین T (۵ متر به هر طرف).
            2. کشتی‌گیر باید به ترتیب مسیر مشخص‌شده را حرکت کند:
            - حرکت مستقیم به جلو.
            - حرکت جانبی به طرفین.
            - بازگشت به نقطه شروع.
            3. زمان تکمیل مسیر ثبت می‌شود.

            ---

            ## 📐 **فرمول و محاسبات**
            **زمان آزمون:** 
            زمان کل برای تکمیل مسیر.

            ---

            ## 🔢 **ورودی‌های موردنیاز**
            1. زمان تکمیل مسیر.

            ---

            ## 📊 **خروجی‌ها**
            - **زمان آزمون (ثانیه):** مدت زمان تکمیل مسیر.

        """)


    with st.expander("توضیحات آزمون illinois"):
        st.markdown("""
            ## آزمون چابکی ایلینوی (Illinois Agility Test)

            **هدف آزمون:** 
            - ارزیابی توانایی کشتی‌گیر برای تغییر جهت سریع در یک مسیر مشخص.

            ---

            ## ⚙️ **مراحل اجرای آزمون**
            1. مسیر آزمون شامل ۸ مخروط است:
            - فاصله طولی: ۱۰ متر.
            - فاصله عرضی بین مخروط‌ها: ۳ متر.
            2. کشتی‌گیر باید به ترتیب مسیر مشخص‌شده حرکت کند.
            3. زمان تکمیل مسیر ثبت می‌شود.

            ---

            ## 📐 **فرمول و محاسبات**
            **زمان آزمون:** 
            زمان کل برای تکمیل مسیر.

            ---

            ## 🔢 **ورودی‌های موردنیاز**
            1. زمان تکمیل مسیر.

            ---

            ## 📊 **خروجی‌ها**
            - **زمان آزمون (ثانیه):** مدت زمان تکمیل مسیر.


        """)


with tab3:
    # Historical Bar Chart
    if st.session_state.agility_test_data:
        df_history = pd.DataFrame(st.session_state.agility_test_data).sort_values(by="تاریخ")

        # Convert Gregorian to Jalali for display

        # Melt the DataFrame for combining metrics
        melted_df = pd.melt(
            df_history,
            id_vars=["تاریخ"],
            value_vars=["specefic_duration", "bear_duration", "zone_duration", "T_duration", "illinois_duration"],
            var_name="Duration Type",
            value_name="Duration (seconds)"
        )

        # Create Grouped Bar Plot
        plot = px.bar(
            melted_df,
            x="تاریخ",
            y="Duration (seconds)",
            color="Duration Type",
            barmode="group",
            title="تغییرات زمانی در آزمون‌های چابکی",
            labels={"تاریخ": "تاریخ", "Duration (seconds)": "مدت زمان (ثانیه)", "Duration Type": "نوع آزمون"}
        )

        plot.update_layout(
            xaxis=dict(type="category"),
            title_x=0.5,  # Center the title
        )

        # Display the Bar Plot
        st.plotly_chart(plot, use_container_width=True)
        st.dataframe(df_history)

    else:
        st.info("هنوز داده‌ای ثبت نشده است.")
