DROP DATABASE IF EXISTS records_db;

-- Create the database
CREATE DATABASE records_db;

-- Connect to the database
\c records_db;

-- Create the `tax_categories` dimension table first
CREATE TABLE tax_categories (
    tax_category_id SERIAL PRIMARY KEY,
    tax_category_name VARCHAR(255) NOT NULL
);

-- Create the `dates` dimension table with `year` column
CREATE TABLE dates (
    date_id SERIAL PRIMARY KEY,
    year INT NOT NULL
);

-- Create the `tax_transactions` fact table
CREATE TABLE tax_transactions (
    transaction_id SERIAL PRIMARY KEY,
    tax_category_id INT NOT NULL,
    date_id INT NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    annual_target NUMERIC(15, 2) NOT NULL,
    FOREIGN KEY (tax_category_id) REFERENCES tax_categories(tax_category_id),
    FOREIGN KEY (date_id) REFERENCES dates(date_id)
);
