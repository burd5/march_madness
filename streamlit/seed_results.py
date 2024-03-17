import streamlit as st
import plotly.express as px
import pandas as pd
from settings import URL,KEY
from st_supabase_connection import SupabaseConnection
conn = st.connection("supabase",type=SupabaseConnection, url=URL, key=KEY)

def get_seed_results():
    rows = conn.query("*", table="seed_results", ttl="10m").execute()
    seed_results = pd.DataFrame(rows.data)
    filtered_df = seed_results[["SEED", "PAKE RANK", "PASE RANK"]]

    filtered_df.columns = ["Seed", "Performance Against Computer Expectations (PAKE)", "Performance Against Seed Expectations (PASE)"]

    return filtered_df

def create_scatter_plot(seed_results):
    fig = px.scatter(seed_results, x='Performance Against Computer Expectations (PAKE)', y='Performance Against Seed Expectations (PASE)', text='Seed', title='Seeds that Over/Under Perform: PAKE & PASE (2008-2023)')
    fig.update_xaxes(showgrid=False, tickmode='linear', tick0=1, dtick=1)
    fig.update_yaxes(showgrid=False, tickmode='linear', tick0=1, dtick=1)
    fig.update_traces(marker=dict(symbol='circle', size=20, color='orange'), textfont=dict(color='black'))
    fig.update_layout(xaxis=dict(title=dict(text='Rank: Performance Against Computer Expectations (PAKE)', font=dict(color='black')), tickfont=dict(color='black')), 
                  yaxis=dict(title=dict(text='Rank: Performance Against Seed Expectations (PASE)', font=dict(color='black')), tickfont=dict(color='black')),
                  font=dict(color='black'))
    return fig


# query = f"""select "SEED" as "Seed",
#                    "PAKE RANK" as "Performance Against Computer Expectations (PAKE)",
#                    "PASE RANK" as "Performance Against Seed Expectations (PASE)"
#             from seed_results
#             """ 

# df = conn.query(query)

# return df