import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query



@st.cache_resource
def listAthletes():
    data = execute_query(st.session_state["client"]
                        .table("athletes")
                        .select('athlete_id, name, weight, height, age, image_url')
                        .order(column="weight"),
                        ttl=0)
    return data.data

@st.cache_resource
def listTests():
    data = execute_query(st.session_state["client"]
                        .table("tests")
                        .select('test_name')
                        .order(column="created_at"),
                        ttl=0)
    return data.data

@st.cache_resource
def getAthleteByName(athlete_name):
    data = execute_query(st.session_state["client"]
                        .table("athletes")
                        .select('athlete_id, name, weight, height, age')
                        .eq("name",athlete_name),
                        ttl=0)
    return data.data

@st.cache_resource
def listAthletesWithHistory():
    test_results = execute_query(st.session_state["client"]
                                .table("athletes")
                                .select('name, weight, height, test_results(test_name, test_category, raw_data)'),
                                ttl=0)
    return test_results.data

def FilterRecordsByAthleteId(athletes_id):
    print("FilterRecordsByAthleteId", athletes_id)

    athletes_records = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('athlete_id, test_date, test_name, test_category, raw_data, athlete_name:athletes(name)')
                                .filter("athlete_id","in",athletes_id),
                                 ttl=0)
    return athletes_records.data

@st.cache_resource
def listAthleteRecords(athlete_id):
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


def listAthletesRecordsByName(test_name):
    test_results = execute_query(st.session_state["client"]
                                .table("test_results")
                                .select('result_id','athlete_id, test_date, gregorian_date, test_name, test_category, raw_data, updated_at, athlete_data:athletes(name, image_url)')
                                .eq("test_name", test_name)
                                .order(column="gregorian_date"),
                                 ttl=0)
    return test_results.data

def deleteListRecords(records_id):
    print(records_id)
    deleted_data = execute_query(st.session_state["client"]
                                .table("test_results")
                                .delete().in_("result_id",records_id)
                                )
    return deleted_data.data