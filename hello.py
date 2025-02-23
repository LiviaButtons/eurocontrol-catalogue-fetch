# Module that makes HTTP requests to URL and returns response 
import requests
# Module that provides methods and phrases for guiding, searching and changing parse tree
from bs4 import BeautifulSoup
# URL parse to fetch product type
from urllib.parse import urlparse
# Pandas for writing DataFrame & Excel
import pandas as pd
# Random & time to add delays
from random import randint
from time import sleep

# Start from product catalogue page with pagination parameter
baseurl = 'https://www.eurocontrol.int'
prodsurl = '/what-we-offer?page='

# Number of pages (could also be made dynamic)
pages = 25

# Declaring variables for later
plinks = []
ptype = []
pnames = []
pacts = []
col1 = "Link"
col2 = "Type"
col3 = "Page title"
col4 = "Activities"

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
            subtype = parsedlink.rpartition('/')[0]
            ptype.append(subtype)
            
productsdf = pd.DataFrame({col1: plinks, col2: ptype})
productsdf.to_excel("output.xlsx", sheet_name="From website", index=False)

# Fetch page info for each product/tool based on previously found URL
for plink in plinks:
    # 1. Fetch relevant page content
    pr = requests.get(plink)

    # 2. Check for success
    if pr.ok:
        psoup = BeautifulSoup(pr.content, 'html.parser')

        # 2.1 Find title
        title = psoup.find('h1').text
        pnames.append(title)

        # 2.2. Find activities - 0 to multiple
        acts = []
        allactlinks = psoup.find('div', class_ = 'content--header__second').find_all('a')

        for actlink in allactlinks:
            acts.append(actlink.text)

        pacts.append(acts)

        # 2.3. Add line to Excel

    else:
        # 3. If fail: print error
        print('Error: ' + pr.status_code)

    # Random naps to avoid getting blocked
    sleep(randint(1,5))

productsdf[col2] = ptype
productsdf[col3] = pnames
productsdf[col4] = pacts
productsdf.to_excel("webcatalogue.xlsx", sheet_name="From website", index=False)