"strength - قدرت"
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
from persiantools.jdatetime import JalaliDate
import jdatetime



# Main Content with Tabs
tab1, tab2 = st.tabs(["قدرت نسبی","📋 تاریخچه"])
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 1
if 'strength_data' not in st.session_state:
    st.session_state.strength_data = []

# A reference list of (Reps, Percentage) pairs down to ~35%.
rep_percentage_data = [
    (1,   100),
    (2,    95),
    (3,    93),
    (4,    90),
    (5,    87),
    (6,    85),
    (7,    83),
    (8,    80),
    (9,    77),
    (10,   75),
    (11,   70),  # Typically 11–12 ~70%
    (12,   70),
    (13,   65),  # Typically 13–15 ~65%
    (14,   65),
    (15,   65),
    (16,   60),  # Typically 16–20 ~60%
    (17,   60),
    (18,   60),
    (19,   60),
    (20,   60),
    (25,   50),  # Broad range for higher reps ~50–55%
    (30,   40),
    (35,   35),
]

def epley_1rm(weight, reps):
    return weight * (1 + reps / 30)

def brzycki_1rm(weight, reps):
    denominator = 1.0278 - 0.0278 * reps
    if denominator <= 0:
        return 0  # Avoid division by zero or negative
    return weight / denominator

# Tab 1: Metrics Visualization
with tab1:
    # Sample Data
    data = []

    df_data = pd.DataFrame(data)

    athlete_weigth = st.session_state.record_data["athlete_weight"]
    athlete_name = st.session_state.record_data["athlete_name"] 
    today = st.session_state.record_data["date"]
    
    with st.form("strength_form", enter_to_submit=False, clear_on_submit=False, border=True):
        col1, col2 = st.columns(2)
        with col1:
            exercise = st.selectbox("نام حرکت:",options=EXERCISE_OPTIONS ,key=f"exercise")
            weight = st.number_input("وزن ورنه بلند شده:", min_value=0.0, value=80.0)
        with col2:
            formula = st.selectbox("فرمول محاسبه:",("Brzycki", "Epley"))
            reps = st.number_input("تعداد تکرار تا مرز خستگی:", min_value=1, value=8)

        # Calculate 1RM
        if formula == "Epley":
            estimated_1rm = epley_1rm(weight, reps)
        else:
            estimated_1rm = brzycki_1rm(weight, reps)

        cols = st.columns(2)
        estimate_power = round(estimated_1rm / athlete_weigth, 2)
        submitted = st.form_submit_button("محاسبه")
        if submitted:
            selected_time = st.session_state.record_data["date"]
            strength_data = [{
                "ورزشکار": athlete_name,
                "تاریخ": selected_time,
                "تمرین": exercise,
                "estimate_power": estimate_power,
                "estimated_1rm": estimated_1rm,
                **{f"{rep_count}": round((perc / 100.0) * estimated_1rm, 2) for rep_count, perc in rep_percentage_data}
            }
            ]
            st.session_state.strength_data.append(strength_data[0])

            st.success(f"قدرت نسبی در حرکت {exercise} با موفقیت ذخیره !")
            
            df = pd.DataFrame(st.session_state.strength_data)
            st.dataframe(df)

            st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")


    submit = st.button("ذخیره")

    if submit:
        st.success("اطلاعات با موفقیت ذخیره شد !")
        # Option to download as CSV
        csv = df_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="دانلود اطلاعات (CSV)",
            data=csv,
            file_name=f"{athlete_name}-{today}.csv",
            mime="text/csv"
        )                
#     if len(df_data) > 0:
#         # Main Content with Tabs
#         tab1, tab2, tab3 = st.tabs(["📊 Metrics", "📅 Historical Data", "📋 Summary"])

#         # Tab 1: Metrics Visualization
#         with tab1:
#             st.subheader("Health Metrics Visualization")
#             fig = px.scatter(df_data, x="% of 1RM", y="Weight", color="Reps", size="Weight", hover_name="Reps")
#             st.plotly_chart(fig, use_container_width=True)

#         # Tab 2: Historical Data
#         with tab2:
#             st.subheader("Wrestler Data Table")
#             st.dataframe(df_data, use_container_width=True)

#         # Tab 3: Summary Charts
#         with tab3:
#             st.subheader("Injury Distribution")
#             injury_fig = px.pie(df_data, names="% of 1RM", title="Injury Types Distribution")
#             st.plotly_chart(injury_fig, use_container_width=True)

# # Tab 2: Historical Data
with tab2:
    # Historical Bar Chart
    if st.session_state.strength_data:
        df_history = pd.DataFrame(st.session_state.strength_data).sort_values(by="تاریخ")
        st.dataframe(df_history)

        # Convert Gregorian to Jalali for display

        # Melt the DataFrame for combining metrics
        history_fig_melted_df = pd.melt(
            df_history,
            id_vars=["تاریخ"],
            value_vars=["estimate_power"],
            var_name="estimate_power",
            value_name="قدرت نسبی"
        )

        # Create Grouped Bar Plot
        history_fig = px.bar(
            history_fig_melted_df,
            x="تاریخ",
            y="قدرت نسبی",
            color="estimate_power",
            barmode="group",
            title="تغییرات قدرت نسبی",
            labels={"تاریخ": "تاریخ", "قدرت نسبی": "قدرت نسبی"}

        )
        history_fig.update_layout(
            xaxis=dict(type="category"),
            title_x=0.5,  # Center the title
        )

        # Display the Bar Plot
        # col1, col2 = st.columns(2)
        # with col1:
        st.plotly_chart(history_fig, use_container_width=True)


    else:
        st.info("هنوز داده‌ای ثبت نشده است.")
