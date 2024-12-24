import streamlit as st

st.title("Taxpayer Management")
st.write("Here, you can manage taxpayer records.")

# Add new taxpayer
st.header("Add Taxpayer")
taxpayer_name = st.text_input("Enter taxpayer name")
location = st.text_input("Enter location")
if st.button("Save Taxpayer"):
    st.success(f"Taxpayer '{taxpayer_name}' from '{location}' has been added.")

