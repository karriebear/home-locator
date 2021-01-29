import streamlit as st
from metrics import metrics

def create_section(metric, metrics_data):
    header, value = st.sidebar.beta_columns([3, 1])
    header.subheader(metric)

    metrics_data[metric]['weight'] = st.sidebar.slider(
        'Weight',
        value=1/len(metrics),
        key=metric,
        min_value=0.0,
        max_value=1.0
    )
    value.write("\n")
    value.text("{:.0%}".format(round(metrics_data[metric]['weight'], 2)))

def create_section_weights(metric, columns, metrics_data, is_favorable=True):
    sidebar = st.sidebar
    # sidebar.checkbox('Is Favorable', value=not is_favorable, key='{0}_is_favorable'.format(metric))
    if len(columns) > 1:
        weighting_container = sidebar.beta_expander("Factors", expanded=False)

        default_value = 1/len(columns)

        for col in columns:
            value = default_value
            if col in metrics_data[metric]['sub_weights']:
                value = metrics_data[metric]['sub_weights'][col]

            metrics_data[metric]['sub_weights'][col] = weighting_container.slider(
                col,
                value=value,
                key='{0}_{1}'.format(metric,col),
                min_value=0.0,
                max_value=1.0
            )
            if col not in metrics_data[metric]['sub_weights']:
                metrics_data[metric]['sub_weights'][col] = default_value
