import pandas as pd
import streamlit as st
import altair as alt

from sql.sql_ops import engine


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
tab1, tab2, tab3, tab4 = st.tabs(['Dataframes', 'Charts', 'Faceted timeline', 'Trends & Reports'])

# Dataframes tab
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
with tab2:
    df_tab1, df_tab2, df_tab3 = st.tabs(['Area', 'Line', 'Scatter'])

    with df_tab1:
        st.area_chart(df_tax_transactions)

    with df_tab2:
        st.line_chart(df_tax_transactions)

    with df_tab3:
        st.scatter_chart(df_tax_transactions)
    

# Faceted timeline
with tab3:
    st.write('In the works...')
    # faceted = alt.Chart(df_tax_transactions).mark_line().encode(
    #     x='amount:O',
    #     y='annual_target:Q',
    #     color='amount:N'
    # ).facet(
    #     column='amount:N'
    # )
    # st.altair_chart(faceted)


with tab4:
    tab1, tab2 = st.tabs(['Insights', 'Visualizations'])
    with tab1:
        # Summary statistics for targets and actuals
        st.header("Summary statistics for Annual targets and actuals amounts collected")
        st.dataframe(df_tax_transactions[['annual_target', 'amount']].describe(), use_container_width=True)

        # Top-performing tax types
        st.header("Top-performing tax types")
        top_tax_types = df_tax_transactions.groupby('tax_category_id')['amount'].sum().sort_values(ascending=False)
        st.dataframe(top_tax_types, use_container_width=True)

        # Annual trends
        st.header("Annual Trends:")
        annual_trends = df_tax_transactions.groupby('date_id')[['annual_target', 'amount']].sum()
        st.dataframe(annual_trends, use_container_width=True)

    with tab2:
        # Annual Achievement Rate Distribution
        st.header("Annual Achievement Rates by Tax Type")
        line = alt.Chart(df_tax_transactions.reset_index()).mark_line().encode(
            x='date_id:O',
            y='annual_target:Q'
        )
        st.altair_chart(line, use_container_width=True)

        # Top Tax Types (Total Actual)
        st.header("Annual Achievement Rates by Tax Type")

        st.line_chart(top_tax_types[:10])