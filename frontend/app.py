import streamlit as st
st.set_page_config(layout="wide")
import plotly.express as px
import pandas as pd
from upset_bar_graph import create_bar_graph, seed_upsets
from avg_upset_per_round import get_upset_count, create_line_graph
from seed_results import get_seed_results, create_scatter_plot
from head_to_head import team_info, return_table
from consts import rounds, teams, years

def upsets():
    st.markdown("""<style>body {background-color: #FFFFFF; /* White background */}</style>""",unsafe_allow_html=True)
    st.columns(3)[1].markdown("<h1>March Madness Upsets</h1>", unsafe_allow_html=True)
    with st.sidebar:
        selected_round = st.selectbox('Select a Round', rounds)
        start_year, end_year = st.sidebar.slider('Select a Range of Years', min_value=2008, max_value=2023, value=(2008, 2023))

    upsets_data = seed_upsets(selected_round, start_year, end_year)
    upsets_bar_graph = create_bar_graph(upsets_data, title=[selected_round, start_year, end_year])
    upset_count = get_upset_count(start_year, end_year)
    upset_count_line_graph = create_line_graph(upset_count, start_year, end_year)
    seed_results = get_seed_results()
    seed_upset_rank_scatter = create_scatter_plot(seed_results)

    st.plotly_chart(upsets_bar_graph, use_container_width=True)
    st.markdown("<p style='text-align: left;'>An upset is defined as a team losing to a seed who is two or more rankings higher. Despite the fact that 10 over 7 should be the most likely, 11 seeds are responsible for the most upsets in the first AND second rounds over the past 15 years.</p>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.write(upset_count_line_graph)
        st.markdown("<p style='text-align: center;'>This graph displays the average number of upsets per round over the selected time period. The average remains relatively stable, which warrants caution for fans who may want to favor a lot of upset picks in the first two rounds.</p>", unsafe_allow_html=True)
    with col4:
        st.write(seed_upset_rank_scatter)
        st.markdown("<p style='text-align: center;'>This graph displays how a seed ranks against computer and general seed expectations. The 11 and 15 seeds overperform on both PAKE and PASE measures, making them a strong pick for potential upsets.</p>", unsafe_allow_html=True)

def head_to_head():
    st.markdown("""<style>body {background-color: #FFFFFF; /* White background */}</style>""",unsafe_allow_html=True)
    st.columns(3)[1].markdown("<h1 style='text-align: center;'>Head to Head</h1>", unsafe_allow_html=True)
    with st.sidebar:
        year = st.selectbox('Year', years)
        first_team = st.selectbox('Team 1', teams)
        second_team = st.selectbox('Team 2', teams)

    first_team_information = team_info(first_team, year)
    second_team_information = team_info(second_team, year)

    col1, col2, col3 = st.columns(3)
    with col1:
        return_table(first_team_information, 1, first_team, year)
    with col2:
        for _ in range(25):
            st.markdown("<h1 style='text-align: center;'>🏀</h1>", unsafe_allow_html=True)

    with col3:
        return_table(second_team_information, 2, second_team, year)



page_names_to_funcs = {
    "Upsets": upsets,
    "Head to Head": head_to_head,
}

# st.markdown("""<style>[data-testid=stSidebar] {background-color: #4682B4;}</style>""", unsafe_allow_html=True)
demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()