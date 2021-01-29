import streamlit as st
import pandas as pd
import urllib.parse

from metrics import metrics
import secrets_beta
import data
from state import state
from sidebar import create_section, create_section_weights
from results import render_results
from add_custom_data import render_data_upload

metrics_data = {}

ranking_df = False

page = st.sidebar.radio("Select Page", ["Results", "Add data"], index=0)

for index, metric_config in enumerate(metrics):
    if not isinstance(metric_config, tuple):
        metrics[index] = (metric_config, True)
        print(metrics)
    (metric, is_lower_favorable) = metrics[index]

    metric_data = data.load_data(st.secrets["GOOGLE_API_KEY"], metric)
    metrics_data[metric] = metric_data
    columns = metric_data['columns']

    create_section(metric, metrics_data)

    metric_score = metric_data['data'][['State']].copy()

    create_section_weights(metric, columns, metrics_data, is_lower_favorable)

    # this math doesn't work out properly :( true + false should equal to one but does not
    # cleanup/move to method -> calculate scores
    metric_score[metric] = 1 if is_lower_favorable else 0
    for col in metrics_data[metric]['sub_weights']:
        percent_metric = metric_data['data'][col]/metric_data['data'][col].max()
        applied_weights = percent_metric * metric_data['sub_weights'][col]
        if is_lower_favorable:
            metric_score[metric] -= applied_weights
        else:
            metric_score[metric] += applied_weights

    if ranking_df is False:
        ranking_df = metric_score
        ranking_df.insert(1, 'Score', 0.0)
    else:
        ranking_df = pd.merge(ranking_df, metric_score, on="State")

    ranking_df['Score'] = ranking_df['Score'] + metrics_data[metric]['weight'] * ranking_df[metric]
    # end cleanup

if page == "Results":
    render_results(ranking_df, metrics_data)
else:
    render_data_upload()
