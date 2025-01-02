import pandas as pd
import streamlit as st
from sqlalchemy import text
from Dashboard import engine


############# Streamlit UI
# Configuration
st.set_page_config(
    layout="wide",
)
st.title("Logs")
st.sidebar.header("TaxEase")
st.sidebar.success("Logs")