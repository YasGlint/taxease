## Transforms data into a format that matches the data warehouse schema
import pandas as pd


# Load the CSV into Excel-compatible DataFrame
input_data = 'output/extracted_FIRS_statistics.csv'
output_csv = 'output/FIRS_statistics.csv'

# Read the CSV
df = pd.read_csv(input_data)


# Clean `Tax Type` with refined rules
def clean_tax_type_excel(tax_type):
    tax_type = tax_type.strip().replace('"', '').replace('\n', ' ')
    if len(tax_type) > 2 and tax_type[1] == ' ':
        tax_type = tax_type[2:].strip()

    # Remove trailing uppercase if separated by a space
    words = tax_type.split()
    if words[-1].isupper() and len(words[-1]) == 1:
        words.pop()
    return ' '.join(words)


# Function to convert to Camel Case
def to_camel_case(text):
    if text.isupper():  # Preserve all-uppercase text
        return text

    # Split text into words, capitalize each, then join
    words = text.lower().split()
    camel_case_text = ''.join(word.capitalize() for word in words)
    return camel_case_text


# Apply cleaning and Camel Case function to `Tax Type`
df['Tax Type'] = df['Tax Type'].apply(clean_tax_type_excel).apply(to_camel_case)


# Export
# df.to_excel(output_excel, index=False)
df.to_csv(output_csv, index=False)
print("Data exported to {output_csv}")