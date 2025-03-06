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

    # Bools to determine when we are in the right place
    is_service_page = False
    is_beneficiary = False
    is_availability = False

    # Declare strings for easier concatenation (since info can be spread over multiple text blocks)
    page_title = ''
    page_beneficiaries = ''
    page_availability = ''
    page_pcode = ''
    page_category = ''
    
    # Fetch all text blocks on a page
    page_texts = page.find_all('LTTextBoxHorizontal')
    
    # Find page title
    for page_text in page_texts:
        # The first 0-3 are the page title, then comes the "Service/tool" description - so break when you reach that
        if page_text.text.startswith('Service/tool'):
           is_service_page = True
           break
        page_title += page_text.text
    
    c_titles.append(page_title)
    print(page_title)
    # Ignore pages that aren't a service page
    if not is_service_page:
        continue

    # Find beneficiaries - text found between "Beneficiaries" and "Availability"
    for page_text in page_texts:
        if page_text.text.startswith('Beneficiaries'):
            is_beneficiary = True

        if page_text.text.startswith('Availability'):
            is_beneficiary = False
            break

        if is_beneficiary:  
            page_beneficiaries += page_text.text

    # /!\ clean up page title: some of them don't have white space
    #final_page_title = page_title.split(' ', 1)
    print('beneficiaries are: ' + page_beneficiaries)
    c_beneficiaries.append(page_beneficiaries)

    # Find Availability - text found between "Availability" and "Product code"
    for page_text in page_texts:
        if page_text.text.startswith('Availability'):
            is_availability = True

        if page_text.text.startswith('Product code'):
            is_availability = False
            break

        if is_availability:  
            page_availability += page_text.text

    print('Availability is: ' + page_availability)
    c_availabilities.append(page_availability)

    # Find Product code - text between "Product code" and "EUROCONTROL PRODUCTS & SERVICES CATALOGUE"
    # /!\ Products & services catalogue can have a page number before or after, so use contain instead of starts_with

    # Find Activity - text after EUROCONTROL PRODUCTS & SERVICES CATALOGUE
    # /!\ can be empty

    # 

    # Find annotations - because they contain Links
    # /!\ can be multiple
    annots = page.find_all('Annot')
    if annots:
        for annot in annots:
            urls = annot.get('URI')
            #print(urls)

#print(pages)