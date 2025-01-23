"strength - قدرت"
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
from persiantools.jdatetime import JalaliDate
import jdatetime
import plotly.graph_objects as go
from utils.database import list_athlete, list_athlete_history, insert_test_result
import time
import json
# Main Content with Tabs
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

def bar_line_plot(x , y):
       # Create Bar Plot
        bar_trace = go.Bar(
            x=x,
            y=y,
            name="Bar Plot",
            marker=dict(color='rgb(58, 71, 80)')
        )

        # Create Line Plot
        line_trace = go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name="Line Plot",
            line=dict(color='rgb(255, 100, 100)', width=2)
        )

        # Combine both traces in a single figure
        fig = go.Figure(data=[bar_trace, line_trace])

        # Set layout properties
        fig.update_layout(
            title="Bar Plot with Line Overlay",
            xaxis_title="Category",
            yaxis_title="Value",
            barmode='group',
            template="plotly_white"
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)


# Tab 1: Metrics Visualization

# Using pytz
import pytz

utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
# tehran_time = utc_now.astimezone(tehran_tz)
print("UTC Time:", utc_now)
# print("Tehran Time:", tehran_time)

# Using zoneinfo
from zoneinfo import ZoneInfo


with st.form("strength_form", enter_to_submit=False, clear_on_submit=False, border=True):
    st.subheader("تست قدرت نسبی")

    df_data =  []

    col1, col2 = st.columns(2)
    with col1:
        athletes = pd.DataFrame(list_athlete())
        
        athlete_name = st.selectbox("ورزشکار", 
            athletes["name"], 
            placeholder="انتخاب کنید",
            index=None
        )
        athlete_id = athletes.loc[athletes["name"] == athlete_name, "athlete_id"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "athlete_id"].empty else ""
        athlete_weight = athletes.loc[athletes["name"] == athlete_name, "weight"].values[0] if not athletes.loc[athletes["name"] == athlete_name, "weight"].empty else ""

        st.session_state.record_data["athlete_weight"] = athlete_weight
        st.session_state.record_data["athlete_name"] = athlete_name
        
        exercise = st.selectbox("نام حرکت:",
                                options=EXERCISE_OPTIONS ,
                                placeholder="انتخاب کنید",
                                index=None,
                                key=f"exercise"
                                )
        
        weight = st.number_input("وزن ورنه بلند شده:", 
                                min_value=0.0,
                                placeholder="انتخاب کنید",
                                step=2.5,
                                value=80.0)
        reps = st.number_input("تعداد تکرار تا مرز خستگی:", min_value=1, value=8)
        
        formula = st.selectbox("فرمول محاسبه:",("Brzycki", "Epley"))
        
        day , month, year= st.columns(3)
        with year:
            years = list(range(JalaliDate.today().year+1, 1390, -1))
            selected_year = st.selectbox("", years, index=years.index(JalaliDate.today().year) , key="year")
        with month:
            months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
            selected_month = st.selectbox("", months, index=JalaliDate.today().month - 1 , key="month")
        with day:
            days = list(range(1, 32))
            selected_day = st.selectbox("تاریخ", days, index=JalaliDate.today().day - 1 , key="day")
        record_date = JalaliDate(selected_year, months.index(selected_month) + 1, selected_day, locale="fa")
        gregorian_date = record_date.to_gregorian()
    # Calculate 1RM
    if formula == "Epley":
        estimated_1rm = epley_1rm(weight, reps)
    else:
        estimated_1rm = brzycki_1rm(weight, reps)
        
    cols = st.columns(2)
    
    
    submitted = st.form_submit_button("محاسبه")
    calcuted_data = [(rep_count, perc, round((perc / 100.0) * estimated_1rm, 2)) for rep_count, perc in rep_percentage_data]
    if submitted:
        with st.spinner('در حال محاسبه ...'):
            time.sleep(2.5)
        if athlete_name and exercise:
            estimate_power = round(estimated_1rm / athlete_weight, 2)
            current_date = JalaliDate.to_jalali(datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Tehran"))).strftime("%Y-%m-%d %H:%M:%S")
            selected_time = record_date
            exercise_data = {
                "exercise": exercise,
                "estimate_power": estimate_power,
                "estimated_1rm": round(estimated_1rm, 2),
                "calcuted_data": f"{calcuted_data}"
            }
            # exercise_data = json.dumps(exercise_data)

            test_result = {
                "athlete_id": int(athlete_id),
                "raw_data": exercise_data,
                "test_name": "قدرت نسبی",
                "test_category": "قدرت",
                "test_date": jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "gregorian_date": datetime.now(ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Tehran")).strftime("%Y-%m-%d %H:%M:%S")
            }
          

            for rep_count, perc in rep_percentage_data:

                df_data.append({
                    "% of 1RM": f"{perc}%",
                    "Weight (kg)": round((perc / 100.0) * estimated_1rm, 2),
                    "Reps": rep_count
                })

            st.session_state.strength_data.append(test_result)

            st.success(f"قدرت نسبی در حرکت {exercise} با موفقیت ذخیره !")
            
            df = pd.DataFrame([exercise_data])

            st.dataframe(df)

            st.dataframe(df_data)
            # st.info('برای مشاهده بیشتر به تب تاریخچه بروید.', icon="ℹ️")
            
            insert_test_result(test_result)
        else:
            st.warning("لطفا فرم را کامل کنید !")


submit = st.button("ذخیره")



# if len(st.session_state.strength_data) > 1:
#     print(st.session_state.strength_data)
#     df_history = pd.DataFrame(st.session_state.strength_data)
#     st.dataframe(df_history)

# if submit:
#     st.success("اطلاعات با موفقیت ذخیره شد !")
#     # Option to download as CSV
#     csv = df_history.to_csv(index=False).encode('utf-8')
#     st.download_button(
#         label="دانلود اطلاعات (CSV)",
#         data=csv,
#         file_name=f"{athlete_name}.csv",
#         mime="text/csv"
#     )                
#     # bar_line_plot(x=df_history["test_date"], y=df_history["estimate_power"])

    


# else:
#     st.info("هنوز داده‌ای ثبت نشده است.")
