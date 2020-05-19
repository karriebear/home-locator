import streamlit as st
import pandas as pd
import urllib.parse

metrics = [
    'Safety',
    'Natural Disasters',
    'Weather',
    'Income Tax',
    # 'Capital Gains Tax',
    'Sin Tax',
    'Wireless Tax',
    'Sales Tax',
    'Fuel Tax',
    'Property Tax',
]

metrics_data = {}

ranking_df = False

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

def create_section_weights(metric, columns):
    show_category_weighting = st.sidebar.checkbox('Show category weighting', key=metric)
    default_value = 1/len(columns)

    for col in columns:
        if show_category_weighting:
            metrics_data[metric]['sub_weights'][col] = st.sidebar.slider(
                col,
                value=metrics_data[metric]['sub_weights'][col] if col in metrics_data[metric]['sub_weights'] else default_value,
                key='{0}_{1}'.format(metric,col),
                min_value=0.0,
                max_value=1.0
            )
        elif col in metrics_data[metric]['sub_weights']:
            continue
        else:
            metrics_data[metric]['sub_weights'][col] = default_value

for metric in metrics:
    metric_data = load_data('1ZBhUjnMxAQW1fgQAEipzJ7jbaJ5768bGSkqyuOgHn2o', metric)
    metrics_data[metric] = metric_data
    columns = metric_data['columns']

    st.sidebar.subheader(metric)
    weight = st.sidebar.slider('Weight', value=1/len(metrics), key=metric, min_value=-1.0, max_value=1.0)

    metric_score = metric_data['data'][['State']].copy()

    if len(columns) > 1:
        create_section_weights(metric, columns)

    # cleanup/move to method -> calculate scores
    if len(metric_data['sub_weights'].keys()) > 0:
        metric_score[metric] = 0
        for col in metrics_data[metric]['sub_weights']:
            percent_metric = metric_data['data'][col]/metric_data['data'][col].max()
            applied_weights = percent_metric * metric_data['sub_weights'][col]
            metric_score[metric] = metric_score[metric] + applied_weights
    else:
        metric_score[metric] = metric_data['data'].iloc[:,1]/metric_data['data'].iloc[:,1].max()

    if ranking_df is False:
        ranking_df = metric_score
        ranking_df.insert(1, 'Score', 0.0)
    else:
        ranking_df = pd.merge(ranking_df, metric_score, on="State")

    ranking_df['Score'] = ranking_df['Score'] + weight * ranking_df[metric]
    # end cleanup

st.title('Rankings')
st.write('See which states are favorable based on what\'s important to you. The lower the score, the more favorable the state. Favorable attributes with a high value require a negative weight (i.e. warm weather). ')

ranking_df = ranking_df.sort_values(by=['Score'])
st.write(ranking_df)

for metric in metrics:
    st.subheader(metric)
    st.write(metrics_data[metric].get('data'))
