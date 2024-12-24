import pandas as pd
import streamlit as st
from sqlalchemy import text
from Dashboard import engine


############# Functions
# Write taxpayer records
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


############# Streamlit UI
st.set_page_config(
    page_title="Taxpayer Management", 
    layout="wide",
)
st.title("Taxpayer Management")
st.sidebar.header("TaxEase")
st.sidebar.success("🧑🏻  Tax Payers")
st.write("Manage taxpayer records.")

    
# Add new taxpayer
#####################
st.header("Add Taxpayer")
taxpayer_name = st.text_input("Enter taxpayer name")
location = st.text_input("Enter location")

if st.button("Save Taxpayer"):
    write_record_taxpayer(taxpayer_name, location)


### Read tax payers
###################
read_conn = st.connection("postgresql", type="sql")
df = read_conn.query('SELECT * FROM taxpayers;', ttl="10m")

st.header("Stored Taxpayers")
st.write(df)

if st.button('Reload'):
    df = read_conn.query('SELECT * FROM taxpayers;')
