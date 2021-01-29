import streamlit as st
import pandas as pd
from state import state
from data import add_poi

table_attr = {}
displayed_fields = []

def render_column_names():
    column_names = st.text_input("Enter comma separated header names")
    if len(column_names) > 0:
        table_attr["names"] = column_names.split(",")

def render_fields(column_names):
    if len(column_names) > 0:
        state.displayed_fields = st.multiselect(
            "Columns to include",
            options=column_names,
            default=column_names
        )

def render_data_upload():
    data = None
    result = None
    datasource = st.file_uploader("Upload data source")
    has_header = st.checkbox("Data has header?")
    if has_header is False:
        table_attr["header"] = None

    if datasource is None:
        if has_header is False:
            render_column_names()
    else:
        data = pd.read_csv(datasource, **table_attr)
        if has_header:
            table_attr["names"] = list(data.columns)
        else:
            render_column_names()
            if "names" in table_attr:
                missing_cols = len(data.columns) - len(table_attr["names"])
                if missing_cols > 0:
                    table_attr["names"] = table_attr["names"] + list(range(0, missing_cols))
                data.columns = table_attr["names"]

    if "names" in table_attr:
        render_fields(table_attr["names"])
    elif data is not None:
        render_fields(list(range(0, len(data.columns))))

    if len(state.displayed_fields):
        try:
            result = data[state.displayed_fields]
        except:
            result = data
    else:
        result = data

    if result is not None:
        st.write(result)
        st.button("Add POI", on_click=lambda: add_poi(result))
