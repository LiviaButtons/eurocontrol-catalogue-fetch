# Module that makes HTTP requests to URL and returns response 
import requests
# Module that provides methods and phrases for guiding, searching and changing parse tree
from bs4 import BeautifulSoup
# URL parse to fetch product type
from urllib.parse import urlparse
# Pandas and openpyxl for dataframes and excel manipulation
import pandas as pd
# Random & time to add delays
from random import randint
from time import sleep

# Start from product catalogue page with pagination parameter
baseurl = 'https://www.eurocontrol.int'
prodsurl = '/what-we-offer?page='

# Number of pages (could also be made dynamic)
pages = 25

# Declaring variables for later (web activity = pdf category)
plinks, ptype, pnames, pacts = [], [], [], []
col1, col2, col3, col4 = 'Link', 'Type', 'Page title', 'Activities'

# Loop through all pages to fetch URLs of each product/tool
for page in range(0, pages):
    # GET request
    r = requests.get(baseurl + prodsurl + str(page))

    # Parse HTML from response - zero in on the cards with the content I want, avoid getting menu links etc
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find('div', class_='card-deck')

    # Find the URL for each product/tool (excluding external links)
    for a in content.find_all('a'):
        link = a.get('href')
        if link.startswith('/'):
            plinks.append(baseurl + link)
            # Find product type in URL
            parsedlink = urlparse(link).path
            subtype = parsedlink.rpartition('/')[0].replace('/', '')
            ptype.append(subtype)
            
products_df = pd.DataFrame({col1: plinks, col2: ptype})
products_df.to_excel('web-catalogue.xlsx', sheet_name='From website', index=False)

# Fetch page info for each product/tool based on previously found URL
for plink in plinks:
    # 1. Fetch relevant page content
    pr = requests.get(plink)

    # 2. Check for success
    if pr.status_code == 200:
        psoup = BeautifulSoup(pr.content, 'html.parser')

        # 2.1 Find title
        title = psoup.find('h1').text.strip()
        pnames.append(title if title else 'error')

        # 2.2. Find activities - 0 to multiple
        header = psoup.find('div', class_ = 'content--header__second')
        if header:
            allactlinks = header.find_all('a')
            individual_acts = []
            for actlink in allactlinks:
                individual_acts.append(actlink.text)
            pacts.append(individual_acts)
        else:
            pacts.append('error')

        print('Page ' + title + ': success')
    else:
        # 3. If fail: print error
        pnames.append(' ')
        pacts.append(' ')
        print('Page: ' + plink)
        print('Error: ' + pr.status_code)

    # Random naps to avoid getting blocked
    sleep(randint(1,5))

old_data_df = pd.read_excel('web-catalogue.xlsx')
new_data_df = pd.DataFrame({col3: pnames, col4: pacts})
df_combined = old_data_df.join(new_data_df, how='outer')
df_combined.to_excel('web-catalogue.xlsx', sheet_name='From website', index=False)
df_combined.to_json('web-catalogue.json', orient='split', compression='infer', index=False)