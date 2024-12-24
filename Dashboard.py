import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from psycopg2 import OperationalError
import matplotlib.pyplot as plt
from datetime import datetime


engine_dataset = create_engine("postgresql://postgres:spyder@localhost:5432/datasets_db")


with engine.connect() as connection:
    # Create the 'taxpayers' table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS taxpayers (
            taxpayer_id SERIAL PRIMARY KEY,
            taxpayer_name VARCHAR(255),
            location VARCHAR(255)
        )
    """))
    connection.commit()
    
    # Create the 'tax_categories' table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS tax_categories (
            tax_category_id SERIAL PRIMARY KEY,
            tax_category_name VARCHAR(255)
        );
    """))
    connection.commit()

    # Create the 'dates' table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS dates (
            date_id SERIAL PRIMARY KEY,
            date DATE,
            year INT,
            month INT,
            quarter INT,
            day_of_week INT
        );
    """))
    connection.commit()

    # Create the 'tax_transactions' table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS tax_transactions (
            transaction_id SERIAL PRIMARY KEY,
            taxpayer_id INT,
            tax_category_id INT,
            date_id INT,
            amount DECIMAL,
            FOREIGN KEY (taxpayer_id) REFERENCES taxpayers(taxpayer_id),
            FOREIGN KEY (tax_category_id) REFERENCES tax_categories(tax_category_id),
            FOREIGN KEY (date_id) REFERENCES dates(date_id)
        );
    """))
    connection.commit()

# Configuration
st.set_page_config(
    page_title="TaxEase Dashboard", 
    layout="wide",
)
st.title("TaxEase Dashboard")
st.write("Welcome to the TaxEase Dashboard.")

st.sidebar.header("TaxEase")
# st.sidebar.success("🏠 Dashboard")

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


## Attempt to read datasets
data_is_present = False
try:
    dataset1 = ([x[0] for x in list_datasets(engine_dataset)])
    data_is_present = True
except:
    pass





col = st.columns((3, 4), gap='medium')

with col[0]:
    if data_is_present:
        dataset_to_read = st.selectbox(f'Reading dataset', dataset1)
        df = read_dataset(dataset_to_read, engine_dataset)
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
    else:
        st.write("No datasets")


with col[1]:
    if data_is_present:
        col = st.columns((4, 4))
        with col[0]:
            st.metric("Average value", round(df["value"].mean(), 2))
        with col[1]:
            st.metric("Sum of values", round(df["value"].sum(), 2))

        # Bar plot
        st.subheader('Bar Chart')
        st.bar_chart(df['value'])


### Line plot
if data_is_present:
    st.subheader('Line Chart')
    st.line_chart(df['value'])