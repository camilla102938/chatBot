import streamlit as st
import psycopg2
import pandas as pd

con = psycopg2.connect(dbname='dev', host='',
                       port='', user='acuser', password='')

st.set_page_config(page_title="app", page_icon="📊")
st.header("app")

show_query = st.sidebar.checkbox('query')

if show_query:
    with open("query_path", 'r') as f:
        sql = f.read()
        df = pd.read_sql_query(sql, con)
