import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import data

# (metric_name, is_lower_favorable)
metrics = [
    ('Safety', False),
    'Natural Disasters',
    # ('Natural Disasters', False),
    # ('Natural Disasters', True),
    ('Weather', False),
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

def create_section_weights(metric, columns, is_favorable=True):
    st.sidebar.checkbox('Is Favorable', value=not is_favorable, key='{0}_is_favorable'.format(metric))

    show_category_weighting = False
    if len(columns) > 1:
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

for index, metric_config in enumerate(metrics):
    if not isinstance(metric_config, tuple):
        metrics[index] = (metric_config, True)
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

    metric_score[metric] = 1 if is_lower_favorable else 0

    metric_score[metric] = data.calculate_metric_score(
        data=metric_data['data'],
        metric_score=metric_score[metric],
        subweights=metrics_data[metric]['sub_weights'],
        is_lower_favorable=is_lower_favorable
    )

    if ranking_df is False:
        ranking_df = metric_score
        ranking_df.insert(1, 'Score', 0.0)
    else:
        ranking_df = pd.merge(ranking_df, metric_score, on="State")

    ranking_df['Score'] = ranking_df['Score'] + weight * ranking_df[metric]
    # end cleanup


st.title('Rankings')
st.write('See which states are favorable based on what\'s important to you.')

overview = ranking_df[['State','Score']]

map_component = components.declare_component("home_map", path="components/map")
home_map = map_component(key="map", data=overview.to_numpy().tolist())

tab_component = components.declare_component("tabs", path="components/tabs/build")
tabs = list(map(lambda metric: metric[0] if isinstance(metric, tuple) else metric, metrics))
tabs.insert(0, "Overview")
active_tab = tab_component(key="tabs", tabs=tabs)


if (active_tab == "Overview"):
    ranking_df = ranking_df.sort_values(by=['Score'], ascending=False)
    st.write(ranking_df)
else:
    for metric_name, is_lower_favorable in metrics:
        if (metric_name == active_tab):
            st.write(metrics_data[metric_name].get('data'))
