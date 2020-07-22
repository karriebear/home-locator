import streamlit as st
import pandas as pd
import urllib.parse

def strip_number(n):
    return float(n.strip('$%'))

@st.cache(allow_output_mutation=True)
def load_data(file, sheet):
    data = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
            file,
            urllib.parse.quote(sheet),
        ),
        thousands=',',
        converters={
            'Tax (%)':strip_number,
            'Tax ($)':strip_number,
        }
    )
    data = data.fillna(0)
    columns = data.columns[1:]
    metric_data = {
        'data': data,
        'columns': columns,
        'sub_weights': {},
        'weight': 0
    }
    return metric_data


def calculate_metric_score(data, metric_score, subweights, is_lower_favorable):
    for col in subweights:
        percent_metric = data[col]/data[col].max()
        applied_weights = percent_metric * subweights[col]
        if is_lower_favorable:
            metric_score -= applied_weights
        else:
            metric_score += applied_weights

    return metric_score
