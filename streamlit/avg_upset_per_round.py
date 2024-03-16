import streamlit as st
import plotly.express as px
conn = st.connection("postgresql", type="sql")


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