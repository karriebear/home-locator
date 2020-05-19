import streamlit as st
import pandas as pd
import urllib.parse

metrics = [
    'Safety',
    'Natural Disasters',
    'Weather',
    'Income Tax',
    'Capital Gains Tax',
    'Sin Tax',
    'Wireless Tax',
    'Sales Tax',
    'Fuel Tax',
    'Property Tax',
]

metrics_data = {}
ranking_df = False

@st.cache
def load_data(file, sheet):
    global ranking_df
    data = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
            file,
            urllib.parse.quote(sheet)
        )
    )
    if ranking_df is False:
        ranking_df = data['State']
    # metrics_data[sheet][DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def create_section_weights(columns):
    for col in columns:
        st.sidebar.text_input(col)

def create_rankings():
    if ranking_df is not False:
        st.write(ranking_df)
    # metrics_data[metric][]/metrics_data[metric][]

for metric in metrics:
    data = load_data('1ZBhUjnMxAQW1fgQAEipzJ7jbaJ5768bGSkqyuOgHn2o', metric)
    metrics_data[metric] = data
    st.sidebar.subheader(metric)
    columns = data.columns
    if len(columns) > 2:
        create_section_weights(columns[1:])

    st.subheader(metric)
    st.write(metrics_data[metric])
    create_rankings()
