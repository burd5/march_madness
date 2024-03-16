import streamlit as st
import pandas as pd

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
    
    df = conn.query(query)
    df_transposed = df.T
    df_transposed.reset_index(inplace=True)
    df_transposed.columns = ['Round', 'Upsets']
    return df_transposed

