import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def load_data(filepath):
    try:
        data = pd.read_csv(filepath, low_memory=False)
        logging.info("Data loaded successfully.")
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        exit()

def clean_property_type(df):
    df['Residential Type'] = df['Residential Type'].fillna('')
    df['Property Type'] = df['Property Type'].fillna('')
    df['Type'] = (df['Property Type'] + ' ' + df['Residential Type']).str.strip()
    df['Type'] = df['Type'].replace(r'(\w+ Family) \1', r'Residential \1', regex=True).replace('Condo Condo', 'Condo')
    df['Type'] = df['Type'].replace('', np.nan)
    df['Type'] = df['Type'].astype('category')
    return df.drop(columns=['Residential Type', 'Property Type'])

def extract_location(df):
    df[['Longitude', 'Latitude']] = df['Location'].str.extract(r'POINT \(([^ ]+) ([^ ]+)\)').astype(float)
    return df.drop(columns=['Location'])

def clean_data(filepath, output_filepath):
    data = load_data(filepath)
    logging.info(data.info())

    # Drop unnecessary columns
    data = data.drop(columns=['Serial Number', 'Assessor Remarks', 'OPM remarks', 'Non Use Code'])

    # Clean property type information
    data = clean_property_type(data)

    # Filter rows with valid locations
    data = data[data['Location'].notna()]
    data = extract_location(data)

    # Filter rows with valid addresses and types
    data = data[data['Address'].notna()]
    cleaned_data = data.dropna(subset=['Type'])

    cleaned_data.to_csv(output_filepath, index=False)
    logging.info("Cleaned data saved to file.")
    logging.info(cleaned_data.info())

if __name__ == "__main__":
    input_file = 'Data/Real_Estate_Sales_2001-2022_GL.csv'
    output_file = 'Data/cleaned_data.csv'
    clean_data(input_file, output_file)

