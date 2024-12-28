## Extracts data from source folder into CSV files

import re
import csv
import os


def parse_data_from_year_file(file_path, year):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    data_pattern = re.compile(r'([A-Za-z\s/]+(?:Tax|Duty|Levy|Fund|Pool|VAT|Income|Profit)?)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)')

    rows = []
    
    for data_match in data_pattern.finditer(text):
        rows.append([year] + [data_match.group(i) for i in range(1, 8)])

    return rows

# Function to process multiple year files and combine the data
def process_year_files(year_files):
    all_data = []
    for year, file_path in year_files.items():
        data = parse_data_from_year_file(file_path, year)
        all_data.extend(data)
    return all_data


# Function to save combined data to CSV
def save_to_csv(data, output_file):
    headers = ['Year', 'Tax Type', 'Annual Target', 'Q1 Target', 'Q2 Target', 'Q3 Target', 'Q4 Target', 'Total Actual']
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)



data_dir = 'source/'

year_files = {
    file.split('.')[0]: os.path.join(data_dir, file)
    for file in os.listdir(data_dir)
    if file.endswith('.txt') and file.split('.')[0].isdigit()
}

# year_files = {str(year): f'data/{year}.txt' for year in range(2015, 2023)}

print(year_files)


csv_output = 'output/extracted_FIRS_statistics.csv'

data = process_year_files(year_files)

save_to_csv(data, csv_output)
print("Exported to CSV.")
