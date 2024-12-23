import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from psycopg2 import OperationalError
import matplotlib.pyplot as plt
from datetime import datetime


engine = create_engine("postgresql://postgres:spyder@localhost:5432/records_db")
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


#### RECORDS DB
# Query records from records_db
def read_taxpayer_data(engine):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM taxpayers")
        )
        return pd.read_sql_query(result.first()[0], engine)
    
def read_tax_transaction_data(engine):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM tax_transactions")
        )
    return pd.read_sql_query(result.first()[0], engine)

def read_specific_taxpayer(taxpayer_name, engine):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM taxpayers WHERE taxpayer_name = '{taxpayer_name}';")
        )
    return pd.read_sql_query(result.first()[0], engine)


# Insert records into records_db
def write_record_taxpayer(taxpayer_name, location, engine):
    with engine.connect() as connection:
        connection.execute(
            text("INSERT INTO taxpayers (taxpayer_name, location) VALUES (:taxpayer_name, :location)"),
            {"taxpayer_name": taxpayer_name, "location": location}
        )

def write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine):
    with engine.connect() as connection:
        connection.execute(
            text("INSERT INTO tax_transactions (taxpayer_id, tax_category_id, date_id, amount) VALUES (:taxpayer_id, :tax_category_id, :date_id, :amount)"),
            {"taxpayer_id": taxpayer_id, "tax_category_id": tax_category_id, "date_id": date_id, "amount": amount}
        )


#### DATASETS DB
# Write
def write_dataset(name, dataset, engine):
    dataset.to_sql('%s' % (name),engine,index=False,if_exists='replace',chunksize=1000)

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



# Streamlit UI
st.title('TaxEase Dashboard')

column_1, column_2 = st.columns(2)

with column_1:
    # Save Taxpayer Records
    st.header('Save Taxpayer')
    taxpayer_name = st.text_input('Enter tax payer\'s name')
    location = st.text_input('Enter tax payer\'s location')
    
    if st.button('Save Taxpayer'):
        write_record_taxpayer(taxpayer_name, location, engine)
        st.success(f"Taxpayer **{taxpayer_name}** from **{location}** saved to database.")
        
    ### Read tax payer data
    if st.button('Read Taxpayer'):
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * FROM taxpayers")
            )
            st.write(pd.read_sql_query(result, engine))
    
    # Save Tax Transaction
    st.header('Save Tax Transaction')
    taxpayer_id = st.number_input('Enter taxpayer ID', min_value=1)
    tax_category_id = st.number_input('Enter tax category ID', min_value=1)
    date_id = st.number_input('Enter date ID', min_value=1)
    amount = st.number_input('Enter transaction amount', min_value=0.01, format="%.2f")
    
    if st.button('Save Transaction'):
        write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine)
        st.success(f"Tax transaction for Taxpayer ID **{taxpayer_id}** saved.")

        
with column_2:
    st.header('Save datasets')
    dataset = st.file_uploader('Please upload dataset')
    if dataset is not None:
        dataset = pd.read_csv(dataset)
        dataset_name = st.text_input('Please enter name for dataset')
        if st.button('Save dataset to database'):
            # Write to datasets_db
            write_dataset('%s' % (dataset_name),dataset,engine_dataset)
            st.info('**%s** saved to database' % (dataset_name))

    try:
        read_title = st.empty()
        # List datasets_db
        dataset_to_read = st.selectbox('Select dataset to read',([x[0] for x in list_datasets(engine_dataset)]))
        read_title.header('Read datasets')
        if st.button('Read dataset'):
            # Read datasets_db
            df = read_dataset(dataset_to_read,engine_dataset)
            st.subheader('Chart')
            st.line_chart(df['value'])
            st.subheader('Dataframe')
            st.write(df)
            
            # # Buttons for different plots
            # if st.button("Show Line Chart"):
            #     plots_.plot_line_chart(df)

            # if st.button("Show Bar Chart"):
            #     plots_.plot_bar_chart(df)

            # if st.button("Show Scatter Plot"):
            #     plots_.plot_scatter_chart(df)
    except:
        pass