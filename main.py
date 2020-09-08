import streamlit as st
import pandas as pd
import urllib.parse
from metrics import metrics
import data

metrics_data = {}

ranking_df = False

def create_section_weights(metric, columns, is_favorable=True):
    sidebar = st.sidebar
    # sidebar.checkbox('Is Favorable', value=not is_favorable, key='{0}_is_favorable'.format(metric))
    weighting_container = sidebar.collapsible_container("Factors", collapsed=True) if len(columns) > 1 else sidebar.container()
    default_value = 1/len(columns)

    for col in columns:
        metrics_data[metric]['sub_weights'][col] = weighting_container.slider(
            col,
            value=metrics_data[metric]['sub_weights'][col] if col in metrics_data[metric]['sub_weights'] else default_value,
            key='{0}_{1}'.format(metric,col),
            min_value=0.0,
            max_value=1.0
        )
        if col not in metrics_data[metric]['sub_weights']:
            metrics_data[metric]['sub_weights'][col] = default_value

for index, metric_config in enumerate(metrics):
    if not isinstance(metric_config, tuple):
        metrics[index] = (metric_config, True)
        print(metrics)
    (metric, is_lower_favorable) = metrics[index]

    metric_data = data.load_data('1ZBhUjnMxAQW1fgQAEipzJ7jbaJ5768bGSkqyuOgHn2o', metric)
    metrics_data[metric] = metric_data
    columns = metric_data['columns']

    st.sidebar.subheader(metric)
    weight = st.sidebar.slider(
        'Weight',
        value=1/len(metrics),
        key=metric,
        min_value=0.0,
        max_value=1.0
    )

    metric_score = metric_data['data'][['State']].copy()

    create_section_weights(metric, columns, is_lower_favorable)

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

    ranking_df['Score'] = ranking_df['Score'] + weight * ranking_df[metric]
    # end cleanup

st.title('Rankings')
st.write('See which states are favorable based on what\'s important to you.')

overall = st.container()
ranking_df = ranking_df.sort_values(by=['Score'], ascending=False)
overall.write(ranking_df)

for metric_name, is_lower_favorable in metrics:
    container = st.collapsible_container(metric_name)
    container.write(metrics_data[metric_name].get('data'))
