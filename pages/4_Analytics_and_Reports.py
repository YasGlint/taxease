import pandas as pd
import streamlit as st
import altair as alt

from Dashboard import list_datasets, engine_dataset, read_dataset



## Attempt to read datasets
try:
    dataset1 = ([x[0] for x in list_datasets(engine_dataset)])
    data_exists = dataset1
except:
    pass

st.set_page_config(
    page_title="Analytics and Reports", 
    layout="wide",
)
st.sidebar.header("TaxEase")
st.title("Analytics and Reports")
st.sidebar.success("📈 Analytics")


if not data_exists:
    st.write("No datasets")
else:
    dataset_to_read = st.selectbox(f'Reading dataset', dataset1)
    df = read_dataset(dataset_to_read, engine_dataset)

    st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

    faceted = alt.Chart(df).mark_line().encode(
        x='Year:O',
        y='Annual Target:Q',
        color='Tax Type:N'
    ).facet(
        column='Tax Type:N'
    )
    st.altair_chart(faceted)


    stacked = alt.Chart(df).transform_fold(
        ['Annual Target', 'Total Actual'],
        as_=['Type', 'Value']
    ).mark_bar().encode(
        x='Tax Type:N',
        y='Value:Q',
        color='Type:N',
        tooltip=['Tax Type:N', 'Type:N', 'Value:Q']
    )

    st.altair_chart(stacked, use_container_width=True)