import pandas as pd
import streamlit as st
import altair as alt

from sql.sql_ops import engine
from sql.helper import *

read_conn = engine.connect()

df_tax_transactions = pd.read_sql(f"SELECT * FROM tax_transactions", read_conn)
df_tax_categories = pd.read_sql(f"SELECT * FROM tax_categories", read_conn)
df_dates = pd.read_sql(f"SELECT * FROM dates", read_conn)



# Streamlit UI
st.set_page_config(
    page_title="Analytics and Reports", 
    layout="wide",
)
st.sidebar.header("TaxEase")
st.title("Analytics and Reports")
st.sidebar.success("📈 Analytics")



# Tabs
tab1, tab2, tab3, tab4 = st.tabs(['Dataframes', 'Charts', 'Trends & Reports', 'Insights'])

# Dataframes tab
###############################
with tab1:
    st.header('Tax Transactions')
    st.dataframe(df_tax_transactions, use_container_width=True)

    df_col1, df_col2 = st.columns(2)

    with df_col1:
        st.header('Tax Categories')
        st.dataframe(df_tax_categories['tax_category_name'], width=600)

    with df_col2:
        st.header('Dates (Years)')
        st.dataframe(df_dates['year'], width=300)


# Charts tab
###############################
with tab2:
    df_tab1, df_tab2, df_tab3 = st.tabs(['Area', 'Line', 'Scatter'])

    with df_tab1:
        st.area_chart(df_tax_transactions)

    with df_tab2:
        st.line_chart(df_tax_transactions)

    with df_tab3:
        st.scatter_chart(df_tax_transactions)


# Trends & Reports
###############################
with tab3:
    st.header("Summary statistics for annual targets and actual amounts collected")

    col1, col2 = st.columns(2)
    with col1:
        # Summary table
        st.dataframe(df_tax_transactions[['annual_target', 'amount']].describe(), use_container_width=True)
    with col2:
        pass

    
    col1, col2 = st.columns(2)
    with col1:
        # Top-performing tax types
        st.header("Highest-grossing taxes")
        top_taxes = df_tax_transactions.groupby('tax_category_id')['amount'].sum().sort_values(ascending=False)
        st.dataframe(top_taxes, use_container_width=True)

    with col2:
        # Annual trends
        st.header("Annual tax trends:")
        annual_trends = df_tax_transactions.groupby('date_id')[['annual_target', 'amount']].sum()
        st.dataframe(annual_trends, use_container_width=True)

# Insights
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        means = df_tax_transactions[['annual_target', 'amount']].mean().round(1)
        maxes =  df_tax_transactions[['annual_target', 'amount']].max().round(1)
        minimums = df_tax_transactions[['annual_target', 'amount']].min().round(1)
        counts = df_tax_transactions.count().round(1)
            
        # Summary text
        st.subheader("Averages")
        st.text(f"Total instances (rows): {counts[0]}")

        st.text(f"Average Annual Target: {means[0]}")
        st.text(f"Average Amount collected: {means[1]}")

        st.write("")
        st.subheader("Highs")
        st.text(f"Highest Annual Target: {maxes[0]}")
        st.text(f"Highest Amount collected: {maxes[1]}")
        
        st.write("")
        st.subheader("Lows")
        st.text(f"Lowest Annual Target: {maxes[0]}")
        st.text(f"Lowest Amount collected: {maxes[1]}")
    
    with col2:
        st.subheader("Deductions")
        
        max_tax_collected = maxes[1]
        max_target = maxes[0]

        min_tax_collected = minimums[1]
        min_target = minimums[0]
        
        st.subheader('1. Tax Goals')
        st.write(
            checkIfTaxGoalsAreMet(max_tax_collected, max_target)
        )

        st.subheader('2. Income state')
        st.write(
            checkIfTaxGoalsAreMet(max_tax_collected, max_target)
        )


# # Faceted timeline
# ###############################
# with tab4:
#     st.write('In the works...')
#     faceted = alt.Chart(df_tax_transactions).mark_line().encode(
#         x='amount:O',
#         y='annual_target:Q',
#         color='amount:N'
#     ).facet(
#         column='annual_target:N'
#     )
#     st.altair_chart(faceted)