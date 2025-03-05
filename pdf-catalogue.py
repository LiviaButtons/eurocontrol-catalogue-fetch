# PDF Reader to extract text of the PDF catalogue
from pdfquery import PDFQuery
# Pandas for easier analysis etc.
# import pandas as pd
# BeautifulSoup to read XML
from bs4 import BeautifulSoup

# Load the PDF catalogue and convert it to XML for readability
#pdf = PDFQuery('catalogue.pdf')
#pdf.load()
#pdf.tree.write('catalogue.xml', pretty_print = True)

# Reading data from the xml file, then parsing it with beautifulsoup
with open('catalogue.xml', 'r') as f:
    data = f.read()
bs_data = BeautifulSoup(data, 'xml')

# Declaring variables
pages = bs_data.find_all('LTPage')
c_titles = []
c_urls = []
c_beneficiaries = []
c_categories = []
c_availabilities = []

# Run through all pages with index
for index, page in enumerate(pages):
    # Skip first 6 pages of blabla
    if index <= 5:
        continue
    is_service_page = False

    page_texts = page.find_all('LTTextBoxHorizontal')
        
    page_title = ''
    
    for page_text in page_texts:
        # The first 0-3 are the page title, then comes the "Service/tool" description - so break when you reach that
        if page_text.text.startswith('Service/tool'):
           is_service_page = True
           break
        page_title += page_text.text
    
    # Ignore pages that aren't a service page
    if not is_service_page:
        continue

    #print(page_title)
    final_page_title = page_title.split(' ', 1)
    print(final_page_title)

    # Find annotations - because they contain Links
    annots = page.find_all('Annot')
    if annots:
        for annot in annots:
            urls = annot.get('URI')
            #print(urls)

#print(pages)