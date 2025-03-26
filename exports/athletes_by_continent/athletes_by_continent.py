import pandas as pd
import country_converter as coco
import json

# Custom mapping
c_map = {'ROC': 'Europe'}

# Read the data
df = pd.read_csv(
    'athletes.csv',
    usecols= ['Country'],
    encoding='ISO-8859-1'
)

# Filter out Refugee Olympic Team
df = df[df['Country'] != "Refugee Olympic Team"]

# Get unique countries and create mapping dictionary
unique_countries = df['Country'].unique()
country_to_continent = {}

# Process each unique country once
for country in unique_countries:
    if country in c_map:
        country_to_continent[country] = c_map[country]
    else:
        try:
            country_to_continent[country] = coco.convert(names=country, to='continent')
        except:
            print(f"Could not map country: {country}")
            country_to_continent[country] = 'Unknown'

df['Continent'] = df['Country'].map(country_to_continent)
df.to_csv('athletes_with_continents.csv', index=False)

# Save mapping for future use
with open('country_mapping.json', 'w') as f:
    json.dump(country_to_continent, f)