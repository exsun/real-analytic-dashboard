import datetime
import streamlit as st
from persiantools.jdatetime import JalaliDate, JalaliDateTime

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def convert_to_jalali(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")  # Convert to datetime object
    jalali_date = JalaliDate.to_jalali(dt.year, dt.month, dt.day)  # Convert to Jalali
    return f"{jalali_date.year}-{jalali_date.month:02d}-{jalali_date.day:02d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"


