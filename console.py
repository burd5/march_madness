import psycopg2
from settings import DATABASE_URL
import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection, url="https://qjvaztljeffutvqxkymb.supabase.co", key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqdmF6dGxqZWZmdXR2cXhreW1iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTA2MzE5MzQsImV4cCI6MjAyNjIwNzkzNH0.64R0euDNbTGARB7QdClJCseAumuu3eXYfPh40nM-7sw")

# Perform query.
rows = conn.query("*", table="upset_seed_info", ttl="10m").execute()

upset_seed_info = pd.DataFrame(rows.data)

filtered_df = upset_seed_info[(upset_seed_info["SEED WON"] > upset_seed_info["SEED LOST"]) & 
                              (upset_seed_info["YEAR"].between(2008, 2023))]

filtered_df["SEED WON"] = filtered_df["SEED WON"].astype(str)
filtered_df["SEED LOST"] = filtered_df["SEED LOST"].astype(str)
# Group by "SEED WON" and "SEED LOST", then count occurrences
result_df = filtered_df.groupby(["SEED WON", "SEED LOST"]).size().reset_index(name="Count")

# Rename columns to match the SQL query
result_df.rename(columns={"SEED WON": "Winner", 
                          "SEED LOST": "Loser",
                          "Count": "Count"}, inplace=True)

# Create the "Matchup" column
result_df["Matchup"] = result_df["Winner"] + " vs " + result_df["Loser"]

# Reordering columns to match SQL query
result_df = result_df[["Winner", "Loser", "Matchup", "Count"]]

print(result_df)