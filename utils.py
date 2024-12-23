import streamlit as st
import pandasql as psql
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

import gspread
import pandas as pd
import time

@st.cache_data
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource
def init_connection():
    conn = st.connection("gsheets", type=GSheetsConnection)
    # st.help(conn)
    return conn

conn = init_connection()


def init_worksheet(conn, worksheet_name):
    # click button to update worksheet
    # This is behind a button to avoid exceeding Google API Quota
    conn.create(
        worksheet=worksheet_name
    )

    # Display our Spreadsheet as st.dataframe




def inset_data_worksheet(conn, worksheet_name, dataframe):
    try:
        print(type(dataframe))
        print(dataframe)
        conn.update(worksheet=worksheet_name, data=dataframe)
        st.success("اطلاعات با موفقیت ذخیره شد !")
        st.cache_data.clear()
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")



@st.cache_data(ttl=3600, show_spinner="Fetching data from API...")  # 👈 Cache data for 1 hour (=3600 seconds)
def load_data(worksheet_name: str):
    return conn.read(worksheet=worksheet_name)


# Google Sheets authentication and fetching data with retry logic
def get_google_sheet_data(spreadsheet_id, range_name, creds_file, expected_headers):
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(range_name)
    data = worksheet.get_all_records(expected_headers=expected_headers)
    
    return pd.DataFrame(data)

# Load and cache data from Google Sheets with retry logic
@st.cache_data(ttl=3600)
def load_data_with_retry(spreadsheet_id, range_name, creds_file, expected_headers, retries=3, delay=5):
    for attempt in range(retries):
        try:
            data = get_google_sheet_data(spreadsheet_id, range_name, creds_file, expected_headers)
            return data
        except (ConnectionError, gspread.exceptions.APIError, gspread.exceptions.GSpreadException) as e:
            st.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    st.error("All attempts to fetch data from Google Sheets failed.")
    return pd.DataFrame()

# use secret variables
SPREADSHEET_ID = st.secrets.google_credentials.SPREADSHEET_ID
RANGE_NAME = st.secrets.google_credentials.RANGE_NAME
CREDS_FILE = st.secrets.google_credentials.CREDS_FILE
EXPECTED_HEADERS = ['شناسه اختصاصی', 'سن']

def replace_spaces_in_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Replace spaces with underscores in all column names of the DataFrame.
    
    Parameters:
    - data (pd.DataFrame): Input DataFrame with various columns.
    
    Returns:
    - pd.DataFrame: Modified DataFrame with updated column names.
    """
    data.columns = [col.replace(" ", "_") for col in data.columns]
    # data.style.set_properties(**{'text-align': 'right'})
    dfStyler = data.style.set_properties(**{'text-align': 'right', 'display': 'grid'})
    dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'right')])])

    return data

