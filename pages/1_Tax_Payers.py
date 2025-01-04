import pandas as pd
import streamlit as st
from sqlalchemy import text

from sql.sql_ops import engine, write_record_taxpayer
import datetime



############# Streamlit UI
# Configuration
st.set_page_config(
    layout="wide",
)
st.title("Tax Payers")
st.sidebar.header("TaxEase")
st.sidebar.success("🧑🏻 Tax Payers")

date = datetime.date(2025, 1, 3)
formatted_date = date.strftime("%a %-d %b , %Y")
st.write(formatted_date)


df_col1, df_col2 = st.columns(2)

with df_col1:
    # Add new taxpayer
    st.header("Add Taxpayer")
    taxpayer_name = st.text_input("Enter taxpayer name")
    location = st.text_input("Enter location")

    if st.button("Save Taxpayer"):
        write_record_taxpayer(taxpayer_name, location)


with df_col2:
    read_conn = engine.connect()

    try:
        df = pd.read_sql("SELECT * FROM taxpayers", read_conn)
        st.write(df)
        
        if st.button('Reload'):
            df = read_conn.query('SELECT * FROM taxpayers;')

    except:
        st.header("Stored Taxpayers")
        st.write("No tax payer data")