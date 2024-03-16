import streamlit as st
conn = st.connection("postgresql", type="sql")


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
    
    df = conn.query(query)
    return df

def return_table(df, team_num, name, year):
    alignment = 'right' if team_num == 1 else 'left'
    if df.empty:
        st.markdown(f"<h4 style='text-align: center; color:red;'>{name} Not in {year} Tournament</h4>", unsafe_allow_html=True)
    if not df.empty:
        for column in df.columns:
            if column not in ['index', 'TEAM ID']:
                st.write(f"<h4 style='text-align: {alignment}; color: orange;'>{column.replace('_', ' ').title()}</h4>", unsafe_allow_html=True)
                st.write(f"<h6 style='text-align: {alignment};'>{df[column].iloc[0]}</h6>", unsafe_allow_html=True)