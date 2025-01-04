import pandas as pd
import streamlit as st

# Configuration
st.set_page_config(
    page_title="TaxEase Dashboard", 
    layout="wide",
)
st.title("TaxEase Dashboard")
st.write("Welcome to the TaxEase Dashboard.")

st.sidebar.header("TaxEase")
st.write("")


# ## Attempt to read datasets
# try:
#     dataset1 = ([x[0] for x in list_datasets(engine_dataset)])
#     data_exists = dataset1
# except:
#     pass


# col = st.columns((3, 4), gap='medium')

# with col[0]:
#     if data_exists:
#         dataset_to_read = st.selectbox(f'Select', dataset1)
#         df = read_dataset(dataset_to_read, engine_dataset)
#         st.dataframe(df, use_container_width=True)
#     else:
#         st.write("No datasets")


# with col[1]:
#     if data_exists:
#         col = st.columns((4, 4))
#         with col[0]:
#             average_annual_target = round(df["Annual Target"].mean(), 2)
#             average_annual_target = f'{average_annual_target} M'
#             st.metric("Average Annual Target", average_annual_target)

#         with col[1]:
#             total_amount = round(df["Total Actual"].mean(), 2)
#             total_amount = f'{total_amount} M'
#             st.metric("Total Amount", total_amount)

#         pie = alt.Chart(df).mark_arc(innerRadius=50).encode(
#             theta='Annual Target:Q',
#             color='Tax Type:N',
#             tooltip=['Tax Type:N', 'Annual Target:Q']
#         )
#         st.altair_chart(pie)
