# Module that makes HTTP requests to URL and returns response 
import requests
# Module that provides methods and phrases for guiding, searching and changin parse tree
from bs4 import BeautifulSoup
# Pandas for writing DataFrame
import pandas as pd

# Start from product catalogue page with pagination parameter
url = 'https://www.eurocontrol.int/what-we-offer?page='

# Number of pages (could also be made dynamic)
pages = 25

# Arrays we will store information
plinks = []
pnames = []
pacts = []

# Loop through all pages to fetch URLs of each product/tool
for page in range(0, pages):
    # GET request
    r = requests.get(url + str(page))

    # Parse HTML from response - zero in on the cards with the content I want, avoid getting menu links etc
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find('div', class_='card-deck')

    # Find the URL for each product/tool (excluding external links)
    for a in content.find_all('a'):
        link = a.get('href')
        if link.startswith('/'):
            plinks.append('https://www.eurocontrol.int' + link)
            
# Fetch page info for each product/tool based on previously found URL
for plink in plinks:
    # 1. Fetch relevant page content
    pr = requests.get(plink)
    psoup = BeautifulSoup(pr.content, 'html.parser')
    print(plink)
    # 2. Find title
    #title = psoup.find('h1').text
    #pnames.append(title)

    # 3. Find activities - 0 to multiple
    #acts = []
    #allactlinks = psoup.find('div', class_ = 'content--header__second').find_all('a')

    #for actlink in allactlinks:
    #    acts.append(actlink.text)

    #pacts.append(acts)

col1 = "Link"
#col2 = "Page title"
#col3 = "Activities"

#productsdf = pd.DataFrame({col1: plinks, col2: pnames, col3: pacts})
productsdf = pd.DataFrame({col1: plinks})
productsdf.to_excel("output.xlsx", sheet_name="From website", index=False)