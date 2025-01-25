import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query



@st.cache_resource
def listAthletes():
    data = execute_query(st.session_state["client"]
                        .table("athletes")
                        .select('athlete_id, name, weight, height, age')
                        .order(column="created_at"),
                        ttl=0)
    return data.data

@st.cache_resource
def listAthletesHistory(athlete_id):
    test_results = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('*')
                                .eq("athlete_id",athlete_id),
                                 ttl=0)
    return test_results.data

def insertRecord(new_record):
    try:
        execute_query(st.session_state["client"]
                                .table("test_results")
                                .insert(new_record),
                                ttl=0)
        st.success("آزمون با موفقیت ثبت شد")
        st.info(new_record['test_date'])
    except:
        st.warning("ثبت تست با خطا مواجه شد !!!")
        st.info(new_record['test_date'])

def listAthleteRecordsByCategory(athlete_id, category):
    test_results = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('*')
                                .eq("athlete_id",athlete_id)
                                .eq("test_category", category)
                                .order(column="gregorian_date"),

                                 ttl=0)
    return test_results.data

def listAthleteRecordsByCategoryByName(athlete_id, category, test_name):
    test_results = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('*')
                                .eq("athlete_id",athlete_id)
                                .eq("test_category", category)
                                .eq("test_name", test_name)
                                .order(column="gregorian_date"),

                                 ttl=0)
    return test_results.data

def listAthleteRecordsByName(athlete_id, test_name):
    test_results = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('*')
                                .eq("athlete_id",athlete_id)
                                .eq("test_name", test_name)
                                .order(column="gregorian_date"),

                                 ttl=0)
    return test_results.data