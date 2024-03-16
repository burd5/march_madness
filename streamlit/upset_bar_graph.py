import streamlit as st
import plotly.express as px
conn = st.connection("postgresql", type="sql")

rounds = {'Round of 64': 64, 'Round of 32': 32, 'Sweet 16': 16, 'Elite 8': 8, 'Final 4': 4}

def seed_upsets(round, start_year, end_year):
    query = f"""select "SEED WON" as "Winner", 
                               "SEED LOST" as "Loser", 
                               "SEED WON" || ' vs ' || "SEED LOST" as "Matchup", 
                                COUNT(*) as "Count"
                        from upset_seed_info 
                        where "SEED WON" > "SEED LOST" AND
                                            "YEAR" BETWEEN {start_year} AND {end_year}
                        """ 
    if round != 'All Rounds':
       query += f""" AND "CURRENT ROUND" = {rounds[round]}"""

    query += """ group by "SEED WON", "SEED LOST" order by 4 desc """
    
    df = conn.query(query)

    return df

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