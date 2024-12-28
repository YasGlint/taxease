import pandas as pd
import streamlit as st
from sqlalchemy import text
from Dashboard import engine

############# Function
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
st.title('Tax Transactions')
st.sidebar.header("TaxEase")
st.sidebar.success("💰 Tax Transactions")


# Add new tax transaction
st.header('Add new Tax Transaction')
taxpayer_id = st.number_input('Enter taxpayer ID', min_value=1)
tax_category_id = st.number_input('Enter tax category ID', min_value=1)
date_id = st.number_input('Enter date ID', min_value=1)
amount = st.number_input('Enter transaction amount', min_value=0.01, format="%.2f")

if st.button('Save Transaction'):
    write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine)
    st.success(f"Tax transaction for Taxpayer ID **{taxpayer_id}** saved.")



read_conn = engine.connect()

df = pd.read_sql("SELECT * FROM tax_transactions", read_conn)
st.header("Stored Tax Transactions")
st.write(df)

if st.button('Reload'):
    df = read_conn.query('SELECT * FROM tax_transactions;')
