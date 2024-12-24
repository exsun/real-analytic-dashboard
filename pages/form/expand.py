import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from components.metrics import EXERCISE_OPTIONS, REP_PERCENTAGE_DATA
from persiantools.jdatetime import JalaliDate

# Title
st.title("سامانه پایش کشتی گیران ایران")

# Main Content with Tabs
tab1, tab2, tab3 = st.tabs(["قدرت", "استقامت", "📋 Summary"])
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 1
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = []

# Tab 1: Metrics Visualization
with tab1:
    date = JalaliDate.to_jalali(datetime.now()).strftime("%Y-%m-%d")

    st.subheader(date)

    # Sample Data
    data = []

    df_data = pd.DataFrame(data)


    # Input Section in Collapsible Expander
    with st.expander("تست قدرت", expanded=True):

        with st.container(border=False):
            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader("مشخصات فردی")
                    athlete_name = st.text_input("نام و نام خانوادگی")
                    athlete_weigth = st.number_input("وزن (kg)", 30, 200, step=1)
                    workout_type = st.selectbox("آزمون", options=["pre-test","post-test"])
                    today = st.text_input("تاریخ", date)

            with col2:
                with st.form("workout_form", enter_to_submit=False, border=True):
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
                            if max_reps > 0:
                                cols = st.columns(2)
                    
                                with cols[0]:
                                    estimate_power = round(max_reps / athlete_weigth, 1)
                                    st.metric("قدرت نسبی", estimate_power)

                                with cols[1]:
                                    st.metric("یک تکرار بیشینه (کیلوگرم)",max_reps)

                            
                                for rep_count, perc in REP_PERCENTAGE_DATA:
                                    weight_at_perc = (perc / 100.0) * max_reps
                                    new_row = pd.Series({
                                            "% of 1RM": perc,
                                            "Weight": round(weight_at_perc, 1),
                                            "Reps": rep_count
                                            })
                                    df_data = pd.concat(
                                        [
                                            df_data, 
                                            pd.DataFrame([new_row], columns=new_row.index)
                                        ]).reset_index(drop=True)


                        
                            
                    add_row = st.form_submit_button("افزودن ردیف جدید")

                    if add_row:
                        st.session_state.num_rows += 1


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
        if len(df_data) > 0:
            # Main Content with Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Metrics", "📅 Historical Data", "📋 Summary"])

            # Tab 1: Metrics Visualization
            with tab1:
                st.subheader("Health Metrics Visualization")
                fig = px.scatter(df_data, x="% of 1RM", y="Weight", color="Reps", size="Weight", hover_name="Reps")
                st.plotly_chart(fig, use_container_width=True)

            # Tab 2: Historical Data
            with tab2:
                st.subheader("Wrestler Data Table")
                st.dataframe(df_data, use_container_width=True)

            # Tab 3: Summary Charts
            with tab3:
                st.subheader("Injury Distribution")
                injury_fig = px.pie(df_data, names="% of 1RM", title="Injury Types Distribution")
                st.plotly_chart(injury_fig, use_container_width=True)

# Tab 2: Historical Data
with tab2:
    st.subheader("Wrestler Data Table")


# Tab 3: Summary Charts
with tab3:
    st.subheader("Injury Distribution")

