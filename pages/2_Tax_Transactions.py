import pandas as pd
import streamlit as st

from sql.sql_ops import \
    engine, write_tax_transaction



############# Streamlit UI
st.title('Tax Transactions')
st.sidebar.header("TaxEase")
st.sidebar.success("💰 Tax Transactions")

# tab1, tab2 = st.tabs(['Add new Tax Transaction', 'Existing Tax Transactions'])

col1, col2 = st.columns(2)


with col1:
    # Add new tax transaction
    st.header('Add new Tax Transaction')
    taxpayer_id = st.number_input('Enter taxpayer ID', min_value=1)
    tax_category_id = st.number_input('Enter tax category ID', min_value=1)
    date_id = st.number_input('Enter date ID', min_value=1)
    amount = st.number_input('Enter transaction amount', min_value=0.01, format="%.2f")

    if st.button('Save Transaction'):
        write_tax_transaction(taxpayer_id, tax_category_id, date_id, amount, engine)


with col2:
    st.header("Stored Tax Transactions")

    read_conn = engine.connect()
    df = pd.read_sql("SELECT * FROM tax_transactions", read_conn)
    st.dataframe(df)