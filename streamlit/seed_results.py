import streamlit as st
import plotly.express as px
conn = st.connection("postgresql", type="sql")

def get_seed_results():
    query = f"""select "SEED" as "Seed",
                       "PAKE RANK" as "Performance Against Computer Expectations (PAKE)",
                       "PASE RANK" as "Performance Against Seed Expectations (PASE)"
                from seed_results
                """ 
    
    df = conn.query(query)

    return df

def create_scatter_plot(seed_results):
    fig = px.scatter(seed_results, x='Performance Against Computer Expectations (PAKE)', y='Performance Against Seed Expectations (PASE)', text='Seed', title='Seed Rank: PAKE vs. PASE')
    fig.update_xaxes(showgrid=False, tickmode='linear', tick0=1, dtick=1)
    fig.update_yaxes(showgrid=False, tickmode='linear', tick0=1, dtick=1)
    fig.update_traces(marker=dict(symbol='circle', size=20, color='orange'), textfont=dict(color='black'))
    fig.update_layout(xaxis=dict(title=dict(text='Rank: Performance Against Computer Expectations (PAKE)', font=dict(color='black')), tickfont=dict(color='black')), 
                  yaxis=dict(title=dict(text='Rank: Performance Against Seed Expectations (PASE)', font=dict(color='black')), tickfont=dict(color='black')),
                  font=dict(color='black'))
    return fig