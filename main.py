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

@st.cache
def load_data(file, sheet):
    data = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
            file,
            urllib.parse.quote(sheet)
        )
    )
    # metrics_data[sheet][DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


for metric in metrics:
    data = load_data('1ZBhUjnMxAQW1fgQAEipzJ7jbaJ5768bGSkqyuOgHn2o', metric)
    metrics_data[metric] = data
    st.sidebar.subheader(metric)
    for col in data.head():
        if (col is not "State"):
            st.sidebar.text(col)
    st.subheader(metric)
    st.write(metrics_data[metric])
