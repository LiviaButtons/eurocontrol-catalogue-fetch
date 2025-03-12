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

# Place data into DataFrames to join/compare/manipulate more easily
web_df = pd.read_json(web_catalogue_file, orient='split')
pdf_df = pd.read_json(pdf_catalogue_file, orient='split')

# Step 1: fetch all possible categories from web & PDF based on column names
all_categories = []
web_categories = web_df.Activities
pdf_categories = pdf_df.Category

# Loop through them to add each activity to the global activity/category view once
for web_category in web_categories:
    # Note that there's 1-2 products that don't have an activity
    if web_category:
        # If there's multiple activities, loop through them and add any that aren't in the total list yet
        if len(web_category) > 1:
            for indiv_web_category in web_category:
                if not indiv_web_category in all_categories:
                    all_categories.append(indiv_web_category)
        # Else just add the individual one
        elif not web_category[0] in all_categories:
            all_categories.append(web_category[0])

# PDF categories are easier because there's only ever one
for pdf_category in pdf_categories:
    if not pdf_category in all_categories:
        all_categories.append(pdf_category)

#print(web_categories)
#print(pdf_categories)
print(all_categories)

# Step 2: match web catagories to PDF categories
# Step 3: group elements by category if there's a match and add them to individual sheets on the excel.
# Step 3.1: retain the rest of the info for each product

# Merging with outer join based on URL match
complete_df = web_df.merge(pdf_df, on='Link', how='outer')
complete_df.to_excel('complete-catalogue.xlsx', sheet_name='Sheet 1', index=False)