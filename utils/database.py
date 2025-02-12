import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

@st.cache_resource
def listAthletes():
    data = execute_query(st.session_state["client"]
                        .table("test_athletes")
                        .select('*')
                        .order(column="weight"),
                        ttl=0)
    return data.data

@st.cache_resource
def listRecordCategory():
    data = execute_query(st.session_state["client"]
                        .table("test_records_category")
                        .select('test_name')
                        .order(column="created_at"),
                        ttl=0)
    return data.data

@st.cache_resource
def getAthleteByName(athlete_name):
    data = execute_query(st.session_state["client"]
                        .table("test_athletes")
                        .select('athlete_id, name, weight, height, age')
                        .eq("name",athlete_name),
                        ttl=0)
    return data.data

@st.cache_resource
def listAthletesWithHistory():
    records = execute_query(st.session_state["client"]
                                .table("test_athletes")
                                .select('name, weight, height, records(test_name, test_category, raw_data)'),
                                ttl=0)
    return records.data

def FilterRecordsByAthleteId(athletes_id):
    print("FilterRecordsByAthleteId", athletes_id)

    athletes_records = execute_query(st.session_state["client"]
                                .table("test_records")
                                .select('athlete_id, test_date, test_name, test_category, raw_data, athlete_name:test_athletes(name)')
                                .filter("athlete_id","in",athletes_id),
                                 ttl=0)
    return athletes_records.data

@st.cache_resource
def listAthleteRecords(athlete_id):
    records = execute_query(st.session_state["client"]
                                .table("test_records")
                                .select('*')
                                .eq("athlete_id",athlete_id),
                                 ttl=0)
    return records.data

def insertRecord(new_record):
    try:
        execute_query(st.session_state["client"]
                                .table("test_records")
                                .insert(new_record),
                                ttl=0)
        st.success("آزمون با موفقیت ثبت شد")
        st.info(new_record['test_date'])
    except:
        st.warning("ثبت تست با خطا مواجه شد !!!")
        st.info(new_record['test_date'])

def listAthleteRecordsByCategory(athlete_id, category):
    records = execute_query(st.session_state["client"]
                                .table("test_records")
                                .select('*')
                                .eq("athlete_id",athlete_id)
                                .eq("test_category", category)
                                .order(column="gregorian_date"),
                                ttl=0)
    return records.data

def listAthleteRecordsByCategoryByName(athlete_id, category, test_name):
    records = execute_query(st.session_state["client"]
                                .table("test_records")
                                .select('*')
                                .eq("athlete_id",athlete_id)
                                .eq("test_category", category)
                                .eq("test_name", test_name)
                                .order(column="gregorian_date"),
                                ttl=0)
    return records.data

def listAthleteRecordsByName(athlete_id, test_name):
    records = execute_query(st.session_state["client"]
                                .table("test_records")
                                .select('*')
                                .eq("athlete_id",athlete_id)
                                .eq("test_name", test_name)
                                .order(column="gregorian_date"),
                                ttl=0
                                )
    return records.data

import jdatetime
def listAthletesRecordsByName(test_name, range_date):

    records = execute_query(st.session_state["client"]
                                .table("test_records")
                                .select('result_id','athlete_id, test_date, gregorian_date, test_name, test_category, raw_data, updated_at, athlete_data:test_athletes(name, image_url)')
                                .eq("test_name", test_name)
                                .gte("test_date", range_date['from'].strftime("%Y-%m-%d") if range_date != None and range_date['from'] != None else jdatetime.date(year=1403, month=1, day=1).strftime("%Y-%m-%d"))
                                .lte("test_date", range_date['to'].strftime("%Y-%m-%d") if range_date != None and range_date['to'] != None else jdatetime.date.today().strftime("%Y-%m-%d"))
                                .order(column="gregorian_date"),
                                ttl=0
                                )
    return records.data

def deleteListRecords(records_id):
    print(records_id)
    deleted_data = execute_query(st.session_state["client"]
                                .table("test_records")
                                .delete().in_("result_id",records_id)
                                )
    return deleted_data.data

def updateAthleteWeight(athlete_id, updated_athlete):
    key, value = next(iter(athlete_id.items()))

    updated_data = execute_query(st.session_state["client"]
                                .table("test_athletes")
                                .update(updated_athlete)
                                .eq(key, value)
                                )

    return updated_data.data


def update_weight(*args, **kwargs):

    updateAthleteWeight(kwargs, {"weight": round(st.session_state.athlete_weight, 1)})
    
