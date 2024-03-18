import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from settings import SQL_ACLH_STRING
import os

# engine=create_engine(SQL_ACLH_STRING)
# connection=engine.connect()

engine=create_engine(st.secrets["SQL_ALCH_STRING"])
connection=engine.connect()

def team_info(team, year):
    query = f"""select
        "YEAR" as "Year",
        "TEAM" as "Team",
        "SEED" as "Seed",
        "CONF" as "Conference",
        "EXP" as "Average of how many years players have played Division I basketball",
        "TALENT RANK" as "Talent Rank",
        "WIN%" as "Win %",
        "2PT%" as "2 point % made",
        "2PT%D" as "2 point % allowed",
        "3PT%" as "3 point % made",
        "3PT%D" as "3 point % allowed",
        "FT%" as "Free Throw %",
        "BLK%" as "Percent of shots blocked",
        "2PTR" as "Percent of shots taken from 2 points",
        "3PTR" as "Percent of shots taken from 3 point line",
        "ROUND" as "Farthest Round in this Tournament",
        "K TEMPO RANK" as "KenPom Tempo Rank",
        "KO RANK" as "KenPom Raw Offensive Officiency Rank",
        "KD RANK" as "KenPom Raw Defensive Efficiency",
        "TOV%" as "Percent of Turnovers Committed",
        "TOV%D" as "Percent of Turnovers Forced",
        "OREB%" as "Percent of Rebounds Grabbed on Offensive End",
        "DREB%" as "Percent of Rebounds Grabbed on Defensive End"
        from kenpom_barttorvik
        where "TEAM" = '{team}' AND
                "YEAR" = {year}
        """ 
    st.cache_data.clear()

    df = pd.read_sql(text(query), con=connection)
    return df

def return_table(df, team_num, name, year):
    alignment = 'right' if team_num == 1 else 'left'
    if df.empty:
        st.markdown(f"<h4 style='text-align: center; color:red;'>{name} Not in {year} Tournament</h4>", unsafe_allow_html=True)
    if not df.empty:
        for column in df.columns:
            if column not in ['index', 'TEAM ID']:
                st.write(f"<h4 style='text-align: {alignment}; color: orange;'>{column.replace('_', ' ').title()}</h4>", unsafe_allow_html=True)
                st.write(f"<h5 style='text-align: {alignment};'>{df[column].iloc[0]}</h5>", unsafe_allow_html=True)

# def team_info(team, year):
#     rows = conn.query("*", table="kenpom_barttorvik", ttl="10m").execute()
#     kenpom_barttorvik = pd.DataFrame(rows.data)
#     filtered_df = kenpom_barttorvik[(kenpom_barttorvik["TEAM"] == team) & (kenpom_barttorvik["YEAR"] == year)]

#     filtered_df = filtered_df[["YEAR", "TEAM", "SEED", "CONF", "EXP", "TALENT RANK", "WIN%", "2PT%", "2PT%D",
#                             "3PT%", "3PT%D", "FT%", "BLK%", "2PTR", "3PTR", "ROUND", "K TEMPO RANK", 
#                             "KO RANK", "KD RANK", "TOV%", "TOV%D", "OREB%", "DREB%"]]

#     filtered_df.columns = ["Year", "Team", "Seed", "Conference", "Average of how many years players have played Division I basketball",
#                         "Talent Rank", "Win %", "2 point % made", "2 point % allowed", "3 point % made", 
#                         "3 point % allowed", "Free Throw %", "Percent of shots blocked", "Percent of shots taken from 2 points",
#                         "Percent of shots taken from 3 point line", "Farthest Round in this Tournament", "KenPom Tempo Rank",
#                         "KenPom Raw Offensive Officiency Rank", "KenPom Raw Defensive Efficiency", "Percent of Turnovers Committed",
#                         "Percent of Turnovers Forced", "Percent of Rebounds Grabbed on Offensive End", 
#                         "Percent of Rebounds Grabbed on Defensive End"]

#     return filtered_df