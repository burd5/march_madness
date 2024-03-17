import psycopg2
import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from settings import SQL_ACLH_STRING


engine=create_engine(SQL_ACLH_STRING)
connection=engine.connect()
query = text("SELECT * FROM upset_seed_info")
df = pd.read_sql(query, con=connection)