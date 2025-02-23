# Module that makes HTTP requests to URL and returns response 
import requests
# Module that provides methods and phrases for guiding, searching and changin parse tree
from bs4 import BeautifulSoup
# Pandas for writing DataFrame
import pandas as pd

# Start from product catalogue page with pagination parameter
url = 'https://www.eurocontrol.int/what-we-offer?page=0'

# Number of pages (could also be made dynamic)
pages = 24

# Loop through all pages to fetch URLs of each product/tool
for page in range(0,25):
    # GET request
    r = requests.get(url + str(page))

    # Parse HTML from response - zero in on the cards with the content I want, avoid getting menu links etc
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find('div', class_='card-deck')

    # Find the URL for each product/tool (excluding external links)
    urls = []
    for a in content.find_all('a'):
        if a.get('href').startswith('/'):
            urls.append(a.get('href'))

plinks = []
pnames = []
pacts = []

# Fetch page info for each product/tool and add it to dataclass
for url in urls:
    # 1. Declare page link
    link = 'https://www.eurocontrol.int' + url
    plinks.append(link)
    
    # 2. Fetch relevant page content
    pr = requests.get(link)
    psoup = BeautifulSoup(pr.content, 'html.parser')
    
    # 3. Find title
    title =  psoup.find('h1').text
    pnames.append(title)

    # 4. Find activities - 0 to multiple
    acts = []
    allactlinks = psoup.find('div', class_ = 'content--header__second').find_all('a')

    for actlink in allactlinks:
        acts.append(actlink.text)

    pacts.append(acts)

col1 = "Link"
col2 = "Page title"
col3 = "Activities"

productsdf = pd.DataFrame({col1: plinks, col2: pnames, col3: pacts})
productsdf.to_excel("output.xlsx", sheet_name="From website", index=False)