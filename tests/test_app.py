from unittest.mock import mock_open, patch

import pandas as pd
import pytest
import streamlit as st
from pandas.testing import assert_frame_equal

from streamlit_gsheets import GSheetsConnection


@pytest.fixture()
def expected_df():
    return pd.DataFrame(
        {
            "date": ["01/01/1975", "01/02/1975", "01/03/1975", "01/04/1975", "01/05/1975"],
            "births": [265775, 241045, 268849, 247455, 254545],
        }
    )
     

def test_streamlit_gsheets_connection(expected_df: pd.DataFrame):

    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.read(worksheet="Example", usecols=[0, 1])
    df = df.head()

    assert_frame_equal(df , expected_df)


def test_query_streamlit_sheet():

    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.query("select date from Example where births = 265775")

    assert len(df) == 1
    assert df["date"].values[0] == "01/01/1975"


def test_query_worksheet_streamlit_sheet():

    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.query("select date from Example where births = 257455")

    assert len(df) == 1
    assert df["date"].values[0] == "01/01/1976"


# secrets_contents = """
# [connections.test_connection_name]
# spreadsheet = "https://docs.google.com/spreadsheets/d/1JDy9md2VZPz4JbYtRPJLs81_3jUK47nx6GYQjgU8qNY/edit"
# """

# @patch("builtins.open", mock_open(read_data=secrets_contents))
# def test_secrets_contents(expected_df):
#     conn = st.connection("test_connection_name", type=GSheetsConnection)

#     df = conn.read()

#     assert_frame_equal(df.head(), expected_df)


def test_no_secrets_contents():
    conn = st.connection("other_connection_name", type=GSheetsConnection)

    with pytest.raises(ValueError, match="Spreadsheet must be specified"):
        conn.read()