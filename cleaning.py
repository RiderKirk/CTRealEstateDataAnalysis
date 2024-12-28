import numpy as np
import pandas as pd

data = pd.read_csv('Data/Real_Estate_Sales_2001-2022_GL.csv', low_memory=False)
print("INPUT DATA INFO")
print(data.info())
print()
print("EXAMPLE INPUT DATA")
print(data)
print()
d1 = data.drop(columns=['Serial Number', 'Assessor Remarks', 'OPM remarks', 'Non Use Code']) # remove some unnecessary columns
# many rows have null entires for property type/residential type
# Consolidate property type information
type_df = d1
type_df['Residential Type'] = type_df['Residential Type'].fillna('') # for now I will replace the null values with empty strings so that I can more easily manipulate the strings
type_df['Property Type'] = type_df['Property Type'].fillna('')
type_df['Type'] = (type_df['Property Type'] + ' ' + type_df['Residential Type'])
type_df['Type'] = type_df['Type'].str.strip()
type_df['Type'] = type_df['Type'].replace(r'(\w+ Family) \1', r'Residential \1', regex=True).replace('Condo Condo', 'Condo')
type_df = type_df.drop(columns=['Residential Type', 'Property Type'])
type_df['Type'] = type_df['Type'].replace('', np.nan) # change the empty strings back to null values
# note that many locations are null
# I will just look at the ones that have locations
location_df = type_df[type_df['Location'].notna()].copy()
location_df['Latitude'] = location_df['Location'].str.extract(r'POINT \(([^ ]+) ([^ ]+)\)')[1]
location_df['Longitude'] = location_df['Location'].str.extract(r'POINT \(([^ ]+) ([^ ]+)\)')[0]
location_df = location_df.drop(columns=['Location'])
location_df['Latitude'] = location_df['Latitude'].astype(float)
location_df['Longitude'] = location_df['Longitude'].astype(float)
# there are also some rows without addresses
location_df = location_df[location_df['Address'].notna()]
cleaned_df = location_df.dropna(subset=['Type'])
cleaned_df.to_csv('Data/cleaned_data.csv', index=False)
print("CLEANED DATA INFO")
print(cleaned_df.info())
print()
print("EXAMPLE CLEANED DATA")
print(cleaned_df)
