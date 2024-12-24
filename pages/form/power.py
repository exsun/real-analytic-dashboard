import streamlit as st
import pandas as pd
from typing import List, Dict
from datetime import datetime
import pytz
from persiantools.jdatetime import JalaliDate
from utils import conn, inset_data_worksheet, init_worksheet
# @st.cache_data
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("styles/custom.css")
rep_percentage_data = [
    (1,   100),
    (2,    95),
    (4,    90),
    (6,    85),
    (8,    80),
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
def calculate_percentages(estimated_1rm: float) -> Dict[str, float]:
    """Calculate percentage values for given max reps"""
    if estimated_1rm > 0:
        return {
            '90%': round(estimated_1rm * 0.9, 1),
            '85%': round(estimated_1rm * 0.85, 1),
            '80%': round(estimated_1rm * 0.8, 1),
            '75%': round(estimated_1rm * 0.75, 1),
            '70%': round(estimated_1rm * 0.7, 1),
            '65%': round(estimated_1rm * 0.65, 1),
            '60%': round(estimated_1rm * 0.60, 1),
            '55%': round(estimated_1rm * 0.55, 1),
            '50%': round(estimated_1rm * 0.50, 1),
            '45%': round(estimated_1rm * 0.45, 1),
            '40%': round(estimated_1rm * 0.4, 1),
            '35%': round(estimated_1rm * 0.35, 1),

        }
    return {k: 0.0 for k in ['90%', '85%', '80%', '75%', '70%', '65%', '60%', '55%', '50%', '45%', '40%', '35%']}

def calculate_1REM(pulled_weight, reps):
    return round(pulled_weight / (1.0278 - (reps * 0.0278)))


st.title("فرم ثبت اطلاعات تست قدرت")

# Exercise options from the original form
EXERCISE_OPTIONS = [
    "پرس سینه", "اسکات", "ددلیفت", "پرس سرشانه", "کلین و جرک",
    "اسنچ", "بارفیکس", "شنا", "پشت بازو", "جلوبازو",
    "لانگز", "پرس پا", "ساق پا", "پلنک", "زیربغل",
    "پشت پا", "جلوی پا", "هیپ تراست", "پرس دمبل", "اسکات از جلو"
]

# Initialize session state for dynamic rows
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 1

if 'workout_data' not in st.session_state:
    st.session_state.workout_data = []




        
# Create form
with st.form("workout_form", enter_to_submit=False, border=True):
    col1, col2 = st.columns(2)

    with col1:
        workout_type = st.selectbox(
            "آزمون",
            options=["pre-test","post-test"]
        )
    with col2:
        today = JalaliDate.to_jalali(datetime.now()).strftime("%Y-%m-%d")
        st.text_input("تاریخ", today)


    col1, col2 = st.columns(2)

    with col1:
        athlete_name = st.text_input("نام ورزشکار")
        # Athlete name input

    with col2:
        
        athlete_weigth = st.number_input(
                "وزن ورزشکار",
                min_value=40
        )

    
    for i in range(st.session_state.num_rows):

        with st.container(border=True):


            col1, col2 = st.columns(2)
            with col1:
                exercise = st.selectbox(
                    "نام حرکت",
                    options=EXERCISE_OPTIONS,
                    key=f"exercise_{i}"
                )
            
            with col2:
                max_reps = st.number_input(
                    "یک تکرار بیشینه",
                    key=f"max_reps_{i}",
                    min_value=0
                )

            # estimated_1rm = calculate_1REM(pulled_weight, reps)
         
            if max_reps > 0:
                # percentages = calculate_percentages(estimated_1rm)
                cols = st.columns(13)
                
                # for idx, (label, value) in enumerate(percentages.items()):
                #     with cols[idx]:
                #         st.metric(label, value)
                with cols[0]:
                    estimate_power = round(max_reps / athlete_weigth, 1)
                    st.metric("قدرت نسبی", estimate_power)

                with cols[1]:
                    st.metric("یک تکرار بیشینه (کیلوگرم)",max_reps)

                df_data = []
                for rep_count, perc in rep_percentage_data:
                    weight_at_perc = (perc / 100.0) * max_reps
                    df_data.append({
                        "% of 1RM": f"{perc}%",
                        "Weight": f"{weight_at_perc:.2f}",
                        "Reps": rep_count
                    })
                df = pd.DataFrame(df_data)
                st.dataframe(df,hide_index=True)
                # confirm = st.button("ثبت",key=f"confirm_{i}")
                chart_data = pd.DataFrame(
                    {
                        "Weight": df['Weight'],
                        "% of 1RM": df['% of 1RM'],
                        # "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
                    }
                )

                st.line_chart(chart_data, x="% of 1RM", y="Weight")

    col1, col2 = st.columns(2)
    with col1:
        add_row = st.form_submit_button("افزودن ردیف جدید")
    with col2:
        submit_form = st.form_submit_button("ثبت اطلاعات")

if add_row:
    st.session_state.num_rows += 1

if submit_form and athlete_name:
    # Collect form data
    workout_data = []
    for i in range(st.session_state.num_rows):
        exercise = st.session_state[f"exercise_{i}"]
        estimated_1rm = st.session_state[f"max_reps_{i}"]
        
        if estimated_1rm > 0:  # Only add rows with valid estimated_1rm
            percentages = calculate_percentages(estimated_1rm)
            workout_data.append({
                "نام ورزشکار": athlete_name,
                "تاریخ" : today,
                "نام حرکت": exercise,
                "حداکثر تکرار": estimated_1rm,
                "قدرت نسبی": estimate_power,
                **percentages
            })
    
    if workout_data:
        # Convert to DataFrame and display
        df = pd.DataFrame(workout_data)
        st.success("اطلاعات با موفقیت ثبت شد!")
        st.dataframe(df)
        
        # Option to download as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="دانلود اطلاعات (CSV)",
            data=csv,
            file_name=f"./static/workout_data_{athlete_name}.csv",
            mime="text/csv"
        )
        # init_worksheet(conn, "wrestle")
        inset_data_worksheet(conn, "wrestling", df)
        
        # Clear form option
        if st.button("ثبت اطلاعات جدید"):
            st.session_state.num_rows = 1
            st.session_state.workout_data = []

else: 
    st.warning("اطلاعات به درستی وارد نشده است !")
