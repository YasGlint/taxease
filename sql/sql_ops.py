import pandas as pd
from sqlalchemy import text
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy import text
import streamlit as st
from sqlalchemy import create_engine, text



engine = create_engine("postgresql://postgres:spyder@localhost:5432/records_db")
engine_dataset = create_engine("postgresql://postgres:spyder@localhost:5432/datasets_db")


# Datasets (datasets_db)
###############################

# List all datasets
def list_datasets(engine):
    with engine.connect() as connection:
        datasets = connection.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        )
        return datasets.fetchall()
    

# Read a selected dataset
def read_dataset(engine, ds):
    try:
        dataset = pd.read_sql_table(ds, engine)
    except:
        dataset = pd.DataFrame([])
    return dataset


# Load the dataset into datasets_db
def upload_dataset(dataset_name, dataset, engine):
    dataset.to_sql('%s' % (dataset_name),engine,index=False,if_exists='replace',chunksize=1000)
    st.success(f"Dataset '{dataset}' uploaded.")
    st.info('**%s** saved to database' % (dataset))


# # Drop a DS
# def drop_dataset(engine, table_name):
#     with engine.connect() as connection:
#         try:
#             # Quote the table name to handle case sensitivity
#             connection.execute(text(f'DROP TABLE public."{table_name}"'))
#             st.success(f"Dataset '{table_name}' has been dropped.")
#         except Exception as e:
#             st.error(f"Error dropping table '{table_name}': {str(e)}")




def read_and_transform_dataset(engine, table_name):
    # Read dataset
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)

    # Clean and preprocess the data
    df['Tax Type'] = df['Tax Type'].str.strip()
    df['Total Actual'] = pd.to_numeric(df['Total Actual'].str.replace(",", ""), errors='coerce')
    df['Annual Target'] = pd.to_numeric(df['Annual Target'].str.replace(",", ""), errors='coerce')
    return df


def populate_records_db(engine, df):
    with engine.connect() as conn:
        # Populate tax_categories
        unique_tax_types = df['Tax Type'].unique()
        tax_categories_df = pd.DataFrame({'tax_category_name': unique_tax_types})
        tax_categories_df.to_sql('tax_categories', engine, index=False, if_exists='append', method='multi')

        # Populate dates
        unique_years = df['Year'].unique()
        dates_df = pd.DataFrame({'year': unique_years})
        dates_df.to_sql('dates', engine, index=False, if_exists='append', method='multi')

        # Populate tax_transactions
        tax_categories = pd.read_sql("SELECT * FROM tax_categories", conn)
        dates = pd.read_sql("SELECT * FROM dates", conn)

        # Merge for foreign key resolution
        df = df.merge(tax_categories, left_on='Tax Type', right_on='tax_category_name', how='left')
        df = df.merge(dates, left_on='Year', right_on='year', how='left')

        transactions_df = df[['tax_category_id', 'date_id', 'Total Actual', 'Annual Target']].rename(
            columns={'Total Actual': 'amount', 'Annual Target': 'annual_target'}
        )
        transactions_df.to_sql('tax_transactions', engine, index=False, if_exists='append', method='multi')



# ETL: populates the records_db using the columns from the datasets_db
def etl_to_records_db(df, engine):
    
    # Extract tax categories
    df['Tax Type'] = df['Tax Type'].str.strip()
    df.replace(',', '', regex=True, inplace=True)
    df.fillna(0, inplace=True)

    unique_tax_types = df['Tax Type'].unique()
    tax_categories_df = pd.DataFrame({'tax_category_name': unique_tax_types})


    # Extract quarters $ transactions
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


    # Total actual
    df["Total Actual"] = df["Total Actual"].str.replace(",", "")
    df["Total Actual"] = pd.to_numeric(df["Total Actual"], errors="coerce")

    total_actual = df['Total Actual'].unique()
    amount_df = pd.DataFrame({'amount': total_actual})


    # Annual targets
    df["Annual Target"] = df["Annual Target"].str.replace(",", "")
    df["Annual Target"] = pd.to_numeric(df["Annual Target"], errors="coerce")


    # Insert data into records_db
    with engine.connect() as conn:
        
        # Insert tax_categories
        tax_categories_df.to_sql('tax_categories', engine, index=False, if_exists='append')

        # Insert amount to tax_transactions
        amount_df.to_sql('tax_transactions', engine, index=False, if_exists='append')




# Records (records_db)
###############################

# Add a transactional records 
def write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO tax_transactions (taxpayer_id, tax_category_id, date_id, amount) VALUES (:taxpayer_id, :tax_category_id, :date_id, :amount)"),
            {"taxpayer_id": taxpayer_id, "tax_category_id": tax_category_id, "date_id": date_id, "amount": amount}
        )

        conn.commit()
        conn.close()
    st.success(f"Tax transaction for Taxpayer ID **{taxpayer_id}** saved.")



# Tax payers (records_db)
# Add a taxpayer record
def write_record_taxpayer(taxpayer_name, location):
    with engine.connect() as conn:
        conn.execute(
            text("""
            INSERT INTO taxpayers (taxpayer_name, location) 
            VALUES (:taxpayer_name, :location)
            """),
            {"taxpayer_name": taxpayer_name, "location": location}
        )
        conn.commit()
        conn.close()
    st.success(f"Taxpayer '{taxpayer_name}' from '{location}' has been added.")

