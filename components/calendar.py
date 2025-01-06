import streamlit as st
from streamlit_nej_datepicker import datepicker_component, Config

config = Config(
    locale="fa",  # 'fa' for Jalali, 'en' for Gregorian
    color_primary="#007bff",  # Customize color
    selection_mode="single"  # Choose 'single', 'range', or 'multiple'
)

# Add the date picker to the sidebar
with st.sidebar:
    st.markdown("## Select a Date")
    selected_date = datepicker_component(config=config)
