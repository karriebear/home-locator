import streamlit as st
from streamlit_google_geochart import google_geochart
import streamlit.components.v1 as components
from metrics import metrics
from state import state

def render_results(ranking_df, metrics_data):
    st.title('Rankings')
    st.write('See which states are favorable based on what\'s important to you.')
    st.write(state.poi)
    overview = ranking_df[['State','Score']]

    google_geochart(
        key="map",
        data=overview.to_records(index=False).tolist(),
        headers=['State','Score'],
        google_maps_api_key="AIzaSyAqFvKJYNukFmJl_erO9xFg_1M0T9jbehc",
        options={
            'region': 'US',
            'displayMode': 'regions',
            'resolution': 'provinces'
        }
    )

    tab_component = components.declare_component("tabs", path="components/tabs/build")
    tabs = list(map(lambda metric: metric[0] if isinstance(metric, tuple) else metric, metrics))
    tabs.insert(0, "Overview")

    active_tab = tab_component(key="tabs", tabs=tabs)

    overall = st.beta_container()
    ranking_df = ranking_df.sort_values(by=['Score'], ascending=False)

    if (active_tab == "Overview"):
        ranking_df = ranking_df.sort_values(by=['Score'], ascending=False)
        st.write(ranking_df)
    else:
        for metric_name, is_lower_favorable in metrics:
            if (metric_name == active_tab):
                st.write(metrics_data[metric_name].get('data'))
