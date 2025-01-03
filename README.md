# taxease

Our current implementation is a starting point with a UI layer for interaction using Streamlit and backend databases with PostgreSQL. 

# 1. Data Warehouse Implementation:
Our Implementation:

  i. We've created relational tables (taxpayers, tax_categories, dates, tax_transactions) that represent a star schema.
  
  ii. Analytics: Basic analytical capability added by visualizing datasets (line_chart in Streamlit), but it's limited compared to typical data warehouse analytics tools.

  While it is a good start, it lacks:
  
  i. Advanced analytics and OLAP capabilities (e.g., aggregations, rollups, or precomputed summaries).
  
  ii. A larger focus on integrating data from multiple sources, which is typical in a data warehouse.


# 2. ETL Pipeline:

Our Implementation:

  i. Extract: The file_uploader in Streamlit allows importing external datasets in CSV format, which fulfills the extract step in a basic manner.
  
  ii. Transform:

  In progress.
  
  iii. Load: The write_dataset function stores datasets into the datasets_db, and taxpayer or transaction records are saved directly into records_db. This fulfills the loading step.

  Lacking:
  
  i. Transformation steps (data cleaning, enrichment, or processing) are not explicitly defined.
  
  ii. Automated ETL Pipeline: Using tools like Apache Airflow or Dagster to schedule ETL tasks.



# How to run:
1. Install all requirements
2. Create a PostgreSQL user using the credentials at /.streamlit/secrets.toml
3. Create 2 PostgreSQL databases: 'datasets_db' and 'records_db' using the sql templates in /sql
4. Execute 'Streamlit run Dashboard.py' and navigate to the link.

Data was extracted from https://www.firs.gov.ng/tax-resources-statistics by copy-paste into the /ETL/source folder, into text files each from years 2015-2023.

The files in the entire /ETL/source can be extracted into a single file (/ETL/extract.py) and transformed to fit the schema (/ETL/transform.py). The output is saved to /ETL/output/FIRS_statistics.csv and can be loaded into the warehouse.



# TODO:  
  i. (In process) Perform data cleaning and transformation before loading.
  
  ii. Expand Analytics: Integrate an OLAP tool or library to perform advanced aggregations.
  
  iii. (In process) Add more visualizations, such as bar charts, heatmaps, or dashboards.
  
  iv. Integrate Data Sources:
  Include APIs, third-party databases, or other file formats in the extract step.
  Merge datasets from multiple sources into a unified data model.
  
  v. Data Quality: Implement data validation during the Transform step to ensure the quality and consistency of uploaded datasets.
  
  vi. Optimize Queries:
  Use indexes and query optimization for the PostgreSQL database to handle large datasets efficiently.
