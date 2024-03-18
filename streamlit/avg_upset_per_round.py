import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from settings import SQL_ACLH_STRING
import os

db_url = os.environ.get('ALCH_STRING')
engine=create_engine(db_url)
connection=engine.connect()
# engine=create_engine(SQL_ACLH_STRING)
# connection=engine.connect()

def get_upset_count(start_year, end_year):
    query = f"""select
                      ROUND(AVG("FIRST ROUND"), 1) as "First Round Upsets",
                      ROUND(AVG("SECOND ROUND"), 1) as "Second Round Upsets",
                      ROUND(AVG("SWEET 16"), 1) as "Sweet 16 Upsets",
                      ROUND(AVG("ELITE 8"), 1) as "Elite 8 Upsets",
                      ROUND(AVG("FINAL 4"), 1) as "Final Four Upsets"
               from upset_count
               where "YEAR" BETWEEN {start_year} AND {end_year}
            """
    
    df = pd.read_sql(text(query), con=connection)
    df_transposed = df.T
    df_transposed.reset_index(inplace=True)
    df_transposed.columns = ['Round', 'Upsets']
    return df_transposed


def create_line_graph(df, start_year, end_year):
    fig = px.line(df, x='Round', y='Upsets')

    fig.update_layout(
        title=f'Avg Number of Upsets per Year ({start_year} - {end_year})',
        xaxis=dict(
            tickfont=dict(color='black'),  
            linecolor='black',  
            linewidth=1, 
            title=dict(text='Round', font=dict(size=16, color='black', family='Arial'))
        ),
        yaxis=dict(
            tickfont=dict(color='black'),  
            linecolor='black', 
            linewidth=1,
            title=dict(text='Avg Number of Upsets', font=dict(size=16, color='black', family='Arial'))  
        ),
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',  
        font=dict(color='black'),  
    )

    fig.update_traces(line=dict(color='#8B4513'))

    return fig


# def get_upset_count(start_year, end_year):
#     query = f"""select
#                       ROUND(AVG("FIRST ROUND"), 1) as "First Round Upsets",
#                       ROUND(AVG("SECOND ROUND"), 1) as "Second Round Upsets",
#                       ROUND(AVG("SWEET 16"), 1) as "Sweet 16 Upsets",
#                       ROUND(AVG("ELITE 8"), 1) as "Elite 8 Upsets",
#                       ROUND(AVG("FINAL 4"), 1) as "Final Four Upsets"
#                from upset_count
#                where "YEAR" BETWEEN {start_year} AND {end_year}
#             """
    
#     df = conn.query(query)
#     df_transposed = df.T
#     df_transposed.reset_index(inplace=True)
#     df_transposed.columns = ['Round', 'Upsets']
#     return df_transposed


# from st_supabase_connection import SupabaseConnection
# import pandas as pd
# from settings import URL,KEY
# conn = st.connection("supabase",type=SupabaseConnection)

# rows = conn.query("*", table="upset_count", ttl="10m").execute()
# upset_count = pd.DataFrame(rows.data)
# filtered_df = upset_count[(upset_count["YEAR"].between(start_year, end_year))]

# first_round_avg = filtered_df["FIRST ROUND"].mean()
# second_round_avg = filtered_df["SECOND ROUND"].mean()
# sweet_16_avg = filtered_df["SWEET 16"].mean()
# elite_8_avg = filtered_df["ELITE 8"].mean()
# final_four_avg = filtered_df["FINAL 4"].mean()

# result_df = pd.DataFrame({
# "Round": ["First Round", "Second Round", "Sweet 16", "Elite 8", "Final Four"],
# "Upsets": [round(first_round_avg, 1),
#                     round(second_round_avg, 1),
#                     round(sweet_16_avg, 1),
#                     round(elite_8_avg, 1),
#                     round(final_four_avg, 1)]
# })

# return result_df