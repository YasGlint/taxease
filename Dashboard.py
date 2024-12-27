import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


engine = create_engine("postgresql://postgres:spyder@localhost:5432/records_db")
engine_dataset = create_engine("postgresql://postgres:spyder@localhost:5432/datasets_db")


with engine.connect() as connection:
    # Create the 'tax_transactions' table (Facts table)
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS tax_transactions (
            transaction_id SERIAL PRIMARY KEY,
            taxpayer_id INT,
            tax_category_id INT,
            date_id INT,
            amount DECIMAL,
            annual_target DECIMAL,
            FOREIGN KEY (taxpayer_id) REFERENCES taxpayers(taxpayer_id),
            FOREIGN KEY (tax_category_id) REFERENCES tax_categories(tax_category_id),
            FOREIGN KEY (date_id) REFERENCES dates(date_id)
        )
    """))

    # Create the 'taxpayers' table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS taxpayers(
            taxpayer_id SERIAL PRIMARY KEY,
            taxpayer_name VARCHAR(255),
            location VARCHAR(255)
        )
    """))
    
    # Create the 'tax_categories' table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS tax_categories (
            tax_category_id SERIAL PRIMARY KEY,
            tax_category_name VARCHAR(255)
        );
    """))

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
try:
    dataset1 = ([x[0] for x in list_datasets(engine_dataset)])
    data_exists = dataset1
except:
    pass


col = st.columns((3, 4), gap='medium')

with col[0]:
    if data_exists:
        dataset_to_read = st.selectbox(f'Reading dataset', dataset1)
        df = read_dataset(dataset_to_read, engine_dataset)
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
    else:
        st.write("No datasets")


with col[1]:
    if data_exists:
        col = st.columns((4, 4))
        with col[0]:
            average_annual_target = round(df["Annual Target"].mean(), 2)
            st.metric("Average Annual Target", average_annual_target)
            
        with col[1]:
            sum_total_actual = round(df["Total Actual"].sum(), 2)
            st.metric("Total amount", sum_total_actual)

        # Bar plot
        st.subheader('Bar Chart')
        st.bar_chart(df['Total Actual'])


### Line plot
if data_exists:
    st.subheader('Line Chart')
    st.line_chart(df['Tax Type'])