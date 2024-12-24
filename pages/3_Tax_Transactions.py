import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
from datetime import datetime
from Dashboard import engine



############# Functions
# Write transactional records 
def write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO tax_transactions (taxpayer_id, tax_category_id, date_id, amount) VALUES (:taxpayer_id, :tax_category_id, :date_id, :amount)"),
            {"taxpayer_id": taxpayer_id, "tax_category_id": tax_category_id, "date_id": date_id, "amount": amount}
        )

        conn.commit()
        conn.close()
    st.success("Transaction recorded.")


############# Streamlit UI
st.set_page_config(
    page_title="Tax Transactions", 
    layout="wide",
)
st.title('Tax Transactions')
st.sidebar.header("TaxEase")
st.sidebar.success("💰  Tax Transactions")


# Add new tax transaction
st.header('Add new Tax Transaction')
taxpayer_id = st.number_input('Enter taxpayer ID', min_value=1)
tax_category_id = st.number_input('Enter tax category ID', min_value=1)
date_id = st.number_input('Enter date ID', min_value=1)
amount = st.number_input('Enter transaction amount', min_value=0.01, format="%.2f")

if st.button('Save Transaction'):
    write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine)
    st.success(f"Tax transaction for Taxpayer ID **{taxpayer_id}** saved.")



### Read tax transactions
###################
read_conn = st.connection("postgresql", type="sql")
df = read_conn.query('SELECT * FROM tax_transactions;', ttl="10m")

st.header("Stored Tax Transactions")
st.write(df)

if st.button('Reload'):
    df = read_conn.query('SELECT * FROM tax_transactions;')