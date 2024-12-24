import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from psycopg2 import OperationalError
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt


engine = create_engine("postgresql://postgres:spyder@localhost:5432/records_db")
engine_dataset = create_engine("postgresql://postgres:spyder@localhost:5432/datasets_db")

st.set_page_config(page_title="TaxEase Dashboard", layout="wide")
st.title("TaxEase Dashboard")
st.write("Welcome to the TaxEase Dashboard.")
st.write("")


#### DATASETS DB
# Read
def read_dataset(name, engine):
    try:
        dataset = pd.read_sql_table(name, engine)
    except:
        dataset = pd.DataFrame([])
    return dataset

# Query
def list_datasets(engine):
    with engine.connect() as connection:
        datasets = connection.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        )
        return datasets.fetchall()




column_1, column_2 = st.columns(2)

with column_1:
    try:
        read_title = st.empty()
        # List datasets_db
        df1 = ([x[0] for x in list_datasets(engine_dataset)])
        dataset_to_read = st.selectbox(f'Reading dataset', df1)

        # Read datasets_db
        df = read_dataset(dataset_to_read,engine_dataset)
        st.write(df)
    except:
        read_title.header('No datasets')


with column_2:
    try:
        df = read_dataset(dataset_to_read,engine_dataset)
        # Bar plot
        st.subheader('Bar Chart')
        st.bar_chart(df['value'])
    except:
        pass

try:
    df = read_dataset(dataset_to_read,engine_dataset)
    # Line plot
    st.subheader('Line Chart')
    st.line_chart(df['value'])
except:
    pass