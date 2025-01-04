import pandas as pd
import streamlit as st

from sql.sql_ops import \
    engine, engine_dataset,\
    list_datasets, populate_records_db, read_and_transform_dataset, read_dataset, upload_dataset


# Streamlit UI
st.set_page_config(
    layout="wide",
    page_title="Data Sources"
)
st.title("Data Sources")
st.sidebar.header("TaxEase")
st.sidebar.success("📊 Datasets")

col1, col2 = st.columns(2)


with col1:
    st.write("Staging area for preprocessing datasets before recording")
    st.header('Add datasets')
    dataset = st.file_uploader('Please upload dataset')
    if dataset is not None:
        dataset_to_upload = pd.read_csv(dataset)
        dataset_name = st.text_input('Please enter name for dataset').strip()

        if st.button('Save dataset to database'):

            # Add to datasets_db
            upload_dataset('%s' % (dataset_name), dataset_to_upload,engine_dataset)

            # Populate records_db
            df = read_and_transform_dataset(engine_dataset, dataset_name)
            populate_records_db(engine, df)

        
with col2:
    st.write()
    try:
        read_title = st.header('Saved datasets')

        # List datasets
        dataset_to_read = st.selectbox('Select dataset to read',([x[0] for x in list_datasets(engine_dataset)]))

        # # Drop the selected dataset
        # if st.button(f"Drop '{dataset_to_read}'"):
        #     drop_dataset(engine, dataset_to_read)
        #     st.experimental_rerun()

        # Read
        st.write(f'Previewing {dataset_to_read}')
        df = read_dataset(engine_dataset, dataset_to_read)
        preview = df.head(5)
        st.write(preview)


    except:
        read_title.header('No datasets available.')
        st.write('Upload data to continue')