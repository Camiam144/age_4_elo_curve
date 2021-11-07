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

# st.subheader("raw data")
# st.write(data.head())

region_dict = {
    "Global" : 7,
    "Europe" : 0,
    "North America" : 3,
    "Asia" : 2,
    "South America" : 4,
    "Oceania" : 5,
    "Africa" : 6,
    "Middle East" : 1,
}

region = st.selectbox(label="Select Region", options=region_dict.keys(), index=0)
region_code = region_dict[region]
if region_code != 7:
    filtered_data = data[data['region'] == region_code]
else:
    filtered_data = data

total_players_in_region = filtered_data.shape[0]
st.caption(f"Total players in region: {total_players_in_region}")
total_games_played_in_region = filtered_data[['wins', 'losses']].sum().sum()
st.caption(f"Total games played in region: {total_games_played_in_region}")

username = st.multiselect("Search for a player...", options=filtered_data['userName'])
row = filtered_data[filtered_data['userName'].isin(username)]
st.table(row[['rlUserId', 'userName', 'elo', 'rank', 'wins', 'losses', 'winPercent', 'winStreak']])

st.subheader("Elo Histogram")
# Work out the start and end of the bins:
bins_start = (filtered_data['elo'].min()//10) * 10
bins_end = (filtered_data['elo'].max()//10 + 1) * 10
counts, bins = np.histogram(filtered_data['elo'].to_numpy(), bins=range(bins_start, bins_end, 10))
bins = 0.5 * (bins[:-1] + bins[1:])

# Whip up a quick dataframe with everything we need:

df_plotting = pd.DataFrame(data={'counts': counts, 'bins': bins})
df_plotting['bin_label'] = df_plotting['bins'].apply(lambda x: str(int(x - 5)) + " - " + str(int(x + 4)))
df_plotting['cum_sum'] = df_plotting['counts'].cumsum()
df_plotting['cum_frac'] = df_plotting['cum_sum']/(df_plotting['counts'].sum())
df_plotting['cum_percent'] = df_plotting['cum_frac']*100

fig = px.bar(df_plotting, x='bins', y='counts', custom_data=['bin_label', 'cum_percent'])
fig.update_traces(hovertemplate="""Players: %{y} <br>Elo: %{customdata[0]} <br>Percentile = %{customdata[1]:.2f}%""")
fig.update_layout(bargap=0.05)

if row.shape[0] > 0:
    line_x_values = row['elo'].to_numpy()
    for val in line_x_values:
        fig.add_vline(x=val, line_dash='dash', line_color='purple')

st.plotly_chart(fig)
