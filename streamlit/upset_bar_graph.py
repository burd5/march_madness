import streamlit as st
import plotly.express as px
import pandas as pd
from settings import URL, KEY
from st_supabase_connection import SupabaseConnection
conn = st.connection("supabase",type=SupabaseConnection)

def seed_upsets(round, start_year, end_year):
    rows = conn.query("*", table="upset_seed_info", ttl="10m").execute()

    upset_seed_info = pd.DataFrame(rows.data)
    rounds = {'Round of 64': 64, 'Round of 32': 32, 'Sweet 16': 16, 'Elite 8': 8, 'Final 4': 4}

    if round == 'All Rounds':
        filtered_df = upset_seed_info[(upset_seed_info["YEAR"].between(start_year, end_year)) &
                                  (upset_seed_info["SEED WON"] > upset_seed_info["SEED LOST"])]
    else:
        filtered_df = upset_seed_info[(upset_seed_info["CURRENT ROUND"] == rounds[round]) & 
                                  (upset_seed_info["YEAR"].between(start_year, end_year)) &
                                  (upset_seed_info["SEED WON"] > upset_seed_info["SEED LOST"])]


    filtered_df["SEED WON"] = filtered_df["SEED WON"].astype(str)
    filtered_df["SEED LOST"] = filtered_df["SEED LOST"].astype(str)

    result_df = filtered_df.groupby(["SEED WON", "SEED LOST"]).size().reset_index(name="Count")

    result_df.rename(columns={"SEED WON": "Winner", 
                            "SEED LOST": "Loser",
                            "Count": "Count"}, inplace=True)

    result_df["Matchup"] = result_df["Winner"] + " vs " + result_df["Loser"]
    result_df = result_df[["Winner", "Loser", "Matchup", "Count"]]
    result_df = result_df.sort_values(by="Count", ascending=False)

    return result_df

def create_bar_graph(df, title):
    fig = px.bar(df, x='Matchup', y='Count')
    fig.update_traces(marker_color='#FCA311') 
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            linecolor='black', 
            linewidth=1,
            tickfont=dict(size=14, color='black', family='Arial'),
            title=dict(text='Matchup', font=dict(size=16, color='black', family='Arial'))
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='black', family='Arial'),
            title=dict(text='Number of Times Upset Occured', font=dict(size=16, color='black', family='Arial'))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14, color='black', family='Arial'),
        title=f'Seed Matchups: {title[0]} ({title[1]} - {title[2]})'
    )
    return fig

# conn = st.connection("postgresql", type="sql")

# rounds = {'Round of 64': 64, 'Round of 32': 32, 'Sweet 16': 16, 'Elite 8': 8, 'Final 4': 4}

# def seed_upsets(round, start_year, end_year):
#     query = f"""select "SEED WON" as "Winner", 
#                                "SEED LOST" as "Loser", 
#                                "SEED WON" || ' vs ' || "SEED LOST" as "Matchup", 
#                                 COUNT(*) as "Count"
#                         from upset_seed_info 
#                         where "SEED WON" > "SEED LOST" AND
#                                             "YEAR" BETWEEN {start_year} AND {end_year}
#                         """ 
#     if round != 'All Rounds':
#        query += f""" AND "CURRENT ROUND" = {rounds[round]}"""

#     query += """ group by "SEED WON", "SEED LOST" order by 4 desc """
    
#     df = conn.query(query)

#     return df