import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query



@st.cache_data
def list_athlete():
    data = execute_query(st.session_state["client"]
                        .table("athletes")
                        .select('athlete_id, name, weight, height, age'), ttl=0)
    return data.data

@st.cache_data
def list_athlete_history(athlete_id):
    test_results = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('*')
                                .eq("athlete_id",athlete_id),
                                 ttl=0)
    return test_results.data
