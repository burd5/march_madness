import streamlit as st
st.set_page_config(layout="wide")
from utils import seed_upsets, get_upset_count
import plotly.express as px
import pandas as pd
from upset_bar_graph import create_bar_graph, seed_upsets
from avg_upset_per_round import get_upset_count, create_line_graph
from seed_results import get_seed_results, create_scatter_plot
from consts import rounds

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
col3, col4 = st.columns(2)
with col3:
    st.write(upset_count_line_graph)
with col4:
    st.write(seed_upset_rank_scatter)
