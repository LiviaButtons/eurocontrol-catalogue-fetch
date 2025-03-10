# Beautiful Soup
from bs4 import BeautifulSoup
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

print(web_catalogue_object)

# Place data into DataFrames to join/compare/manipulate more easily
web_df = pd.DataFrame.from_dict(pd.json_normalize(web_catalogue_object), orient='columns')
pdf_df = pd.DataFrame.from_dict(pd.json_normalize(pdf_catalogue_object), orient='columns')

# Merging with outer join based on URL match
#complete_df = web_df.merge(pdf_df, how='right')

#complete_df.to_excel("complete-catalogue.xlsx", sheet_name="From website", index=False)