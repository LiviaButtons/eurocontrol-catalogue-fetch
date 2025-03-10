# Previously exported all the data as JSON, so:
import json
# Panda for dataframe stuff
import pandas as pd

web_catalogue_file = 'web-catalogue.json'
pdf_catalogue_file = 'pdf-catalogue.json'

with open(web_catalogue_file, 'r') as openfile:
    web_catalogue_object = json.load(openfile)

with open(pdf_catalogue_file, 'r') as secondfile:
    pdf_catalogue_object = json.load(secondfile)

# Place data into DataFrames to join/compare/manipulate more easilye
web_df = pd.read_json(web_catalogue_file, orient='split')
pdf_df = pd.read_json(pdf_catalogue_file, orient='split')

# Merging with outer join based on URL match
complete_df = web_df.merge(pdf_df, on='Link', how='outer')
complete_df.to_excel('complete-catalogue.xlsx', sheet_name='Sheet 1', index=False)