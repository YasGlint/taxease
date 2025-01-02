import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from Dashboard import engine
import altair as alt


engine_dataset = create_engine("postgresql://postgres:spyder@localhost:5432/datasets_db")

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


# Function to drop a table
def drop_dataset(engine, table_name):
    with engine.connect() as connection:
        connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
        connection.commit()


# Query
def list_datasets(engine):
    with engine.connect() as connection:
        datasets = connection.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        )
        return datasets.fetchall()


# ETL
def etl_to_records_db(df, engine):
    # Transformations
    df['Tax Type'] = df['Tax Type'].str.strip()  # Clean names
    df.replace(',', '', regex=True, inplace=True)  # Remove commas
    df.fillna(0, inplace=True)  # Fill missing values

    # Extract tax categories
    unique_tax_types = df['Tax Type'].unique()
    tax_categories_df = pd.DataFrame({'tax_category_name': unique_tax_types})

    # Extract dates
    quarter_columns = ['Q1 Target', 'Q2 Target', 'Q3 Target', 'Q4 Target']
    transactions = []

    for _, row in df.iterrows():
        for i, quarter in enumerate(quarter_columns, start=1):
            transactions.append({
                'year': row['Year'],
                'quarter': f"Q{i}",
                'tax_category_name': row['Tax Type'],
                'amount': row[quarter],
                'annual_target': row['Annual Target']
            })
    transactions_df = pd.DataFrame(transactions)


    df["Total Actual"] = df["Total Actual"].str.replace(",", "")  # Remove commas
    df["Total Actual"] = pd.to_numeric(df["Total Actual"], errors="coerce")  # Convert to numeric

    total_actual = df['Total Actual'].unique()
    amount_df = pd.DataFrame({'amount': total_actual})


    # Annual targets
    # Clean and convert the 'Annual Target' column
    df["Annual Target"] = df["Annual Target"].str.replace(",", "")  # Remove commas
    df["Annual Target"] = pd.to_numeric(df["Annual Target"], errors="coerce")  # Convert to numeric


    # Insert data into records_db
    with engine.connect() as conn:
        # Insert tax categories
        tax_categories_df.to_sql('tax_categories', engine, index=False, if_exists='append')

        # Insert amount
        amount_df.to_sql('tax_transactions', engine, index=False, if_exists='append')

        # # Insert dates
        # dates = [{'year': row['year'], 'quarter': row['quarter']} for row in transactions_df.to_dict('records')]

        # dates_df = pd.DataFrame(dates).drop_duplicates()
        # dates_df.to_sql('dates', engine, index=False, if_exists='append')

        # # Insert fact table data
        # transactions_df.to_sql('tax_transactions', engine, index=False, if_exists='append')


# Streamlit UI
st.title("Data Sources")
st.sidebar.header("TaxEase")
st.sidebar.success("📊  Datasets")
# column_1, column_2 = st.columns(2)

# with column_1:
st.header('Add datasets')
dataset = st.file_uploader('Please upload dataset')
if dataset is not None:
    dataset = pd.read_csv(dataset)
    dataset_name = st.text_input('Please enter name for dataset')

    if st.button('Save dataset to database'):
        # Write to datasets_db
        etl_to_records_db(dataset, engine)
        write_dataset('%s' % (dataset_name),dataset,engine_dataset)
        st.info('**%s** saved to database' % (dataset_name))

        
# with column_2:
st.write()
try:
    read_title = st.empty()
    # List datasets_db
    dataset_to_read = st.selectbox('Select dataset to read',([x[0] for x in list_datasets(engine_dataset)]))
    read_title.header('Saved datasets')

    # Drop the selected dataset
    if dataset_to_read:
        if st.button(f"Drop '{dataset_to_read}'"):
            drop_dataset(engine_dataset, dataset_to_read)
            st.success(f"Dataset '{dataset_to_read}' has been dropped.")
            st.experimental_rerun()

        # Read
        st.write('Preview')
        df = read_dataset(dataset_to_read,engine_dataset)
        preview = df.head()
        st.write(preview)


except:
    read_title.header('No datasets available.')
    st.write('Upload data to continue')