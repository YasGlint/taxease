import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


engine_dataset = create_engine("postgresql://postgres:spyder@localhost:5432/datasets_db")


#### DATASETS DB
# Write
def write_dataset(name, dataset, engine):
    dataset.to_sql('%s' % (name),engine,index=False,if_exists='replace',chunksize=1000)

# Read
def read_dataset(name, engine):
    try:
        dataset = pd.read_sql_table(name, engine)
    except:
        dataset = pd.DataFrame([])
    return dataset

# Query
def list_datasets(engine):
    with engine.connect() as connection:
        datasets = connection.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        )
        return datasets.fetchall()


# Streamlit UI
st.set_page_config(
    page_title="Datasets Management", 
    layout="wide",
    page_icon="📈"
)
st.title("Datasets Management")
st.sidebar.header("TaxEase")
st.sidebar.success("📊  Datasets")
# column_1, column_2 = st.columns(2)

# with column_1:
st.header('Add datasets')
dataset = st.file_uploader('Please upload dataset')
if dataset is not None:
    dataset = pd.read_csv(dataset)
    dataset_name = st.text_input('Please enter name for dataset')
    if st.button('Save dataset to database'):
        # Write to datasets_db
        write_dataset('%s' % (dataset_name),dataset,engine_dataset)
        st.info('**%s** saved to database' % (dataset_name))

        
# with column_2:
st.write()
try:
    read_title = st.empty()
    # List datasets_db
    dataset_to_read = st.selectbox('Select dataset to read',([x[0] for x in list_datasets(engine_dataset)]))
    read_title.header('Saved datasets')

    if st.button('Read dataframes'):
        # Read datasets_db
        df = read_dataset(dataset_to_read,engine_dataset)
        st.write(df)
    
    # Line plot
    if st.button('Visualize'):
        df = read_dataset(dataset_to_read, engine_dataset)

        # Line
        st.subheader('Line Chart')
        st.line_chart(df['value'])

        # Bar
        st.subheader('Bar Chart')
        st.bar_chart(df['value'])

except:
    read_title.header('No datasets.')
    st.write('Upload data to continue')