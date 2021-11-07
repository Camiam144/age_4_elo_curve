""" The main streamlit app script """
import sqlite3 as sql

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache
def get_data() -> pd.DataFrame:
    db_name = 'aoe4elo.db'
    with sql.connect(db_name) as conn:
        data = pd.read_sql('SELECT * FROM elo', conn, parse_dates=['load_time'])

    return data


st.title("AoE 4 1v1 ELO Curve")
data = get_data()

st.subheader("raw data")
st.write(data.head())

region_dict = {
    "Europe" : 0,
    "Middle East" : 1,
    "Asia" : 2,
    "North America" : 3,
    "South America" : 4,
    "Oceania" : 5,
    "Africa" : 6,
    "Global" : 7,
}

region = st.selectbox(label="Select Region", options=region_dict.keys(), index=7)
region_code = region_dict[region]
if region_code != 7:
    filtered_data = data[data['region'] == region_code]
else:
    filtered_data = data

total_players_in_region = filtered_data.shape[0]
st.text(f"Total players in region: {total_players_in_region}")
total_games_played_in_region = filtered_data[['wins', 'losses']].sum().sum()
st.text(f"Total games played in region: {total_games_played_in_region}")

st.subheader("Elo Histogram")
hist_values, bin_edges = np.histogram(filtered_data['elo'].to_numpy(), bins=40)
fig = px.histogram(filtered_data, x="elo")
st.plotly_chart(fig)