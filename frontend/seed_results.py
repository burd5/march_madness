import streamlit as st
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from settings import SQL_ACLH_STRING
import os

# engine=create_engine(SQL_ACLH_STRING)
# connection=engine.connect()

engine=create_engine(st.secrets["SQL_ALCH_STRING"])
connection=engine.connect()

def get_seed_results():
    query = f"""select "SEED" as "Seed",
                   "PAKE RANK" as "Performance Against Computer Expectations (PAKE)",
                   "PASE RANK" as "Performance Against Seed Expectations (PASE)"
            from seed_results
            """ 

    df = pd.read_sql(text(query), con=connection)
    return df

def create_scatter_plot(seed_results):
    fig = px.scatter(seed_results, x='Performance Against Computer Expectations (PAKE)', y='Performance Against Seed Expectations (PASE)', text='Seed', title='Seeds that Over/Under Perform: PAKE & PASE (2008-2023)')
    fig.update_xaxes(showgrid=False, tickmode='linear', tick0=1, dtick=1)
    fig.update_yaxes(showgrid=False, tickmode='linear', tick0=1, dtick=1)
    fig.update_traces(marker=dict(symbol='circle', size=20, color='orange'), textfont=dict(color='black'))
    fig.update_layout(xaxis=dict(title=dict(text='Rank: Performance Against Computer Expectations (PAKE)', font=dict(color='black')), tickfont=dict(color='black')), 
                  yaxis=dict(title=dict(text='Rank: Performance Against Seed Expectations (PASE)', font=dict(color='black')), tickfont=dict(color='black')),
                  font=dict(color='black'))
    return fig



 # rows = conn.query("*", table="seed_results", ttl="10m").execute()
    # seed_results = pd.DataFrame(rows.data)
    # filtered_df = seed_results[["SEED", "PAKE RANK", "PASE RANK"]]

    # filtered_df.columns = ["Seed", "Performance Against Computer Expectations (PAKE)", "Performance Against Seed Expectations (PASE)"]

    # return filtered_df