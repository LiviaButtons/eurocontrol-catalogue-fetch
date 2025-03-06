# Module that makes HTTP requests to URL and returns response 
import requests
# PDF Reader to extract text of the PDF catalogue
from pdfquery import PDFQuery
# Pandas for easier analysis etc.
#import pandas as pd
# BeautifulSoup to read XML
from bs4 import BeautifulSoup

# Find latest edition of the catalogue on publication page
pdf_name = 'nm-product-catalogue.pdf'
xml_name = 'nm-product-catalogue.xml'
base_url = 'https://www.eurocontrol.int'
catalogue_page = 'https://www.eurocontrol.int/publication/eurocontrol-products-services-catalogue'

# GET request to find lates edition of catalogue on publication page
r = requests.get(catalogue_page)
soup = BeautifulSoup(r.content, 'html.parser')
target_link = soup.find('a', type="application/pdf").get('href')
pdf_url = base_url + target_link

# Open and save the latest PDF catalogue
pdf_response = requests.get(pdf_url)
pdf = open(pdf_name, 'wb')
pdf.write(pdf_response.content)
pdf.close

# Load the PDF catalogue and convert it to XML for readability
pdf = PDFQuery(pdf_name)
pdf.load()
pdf.tree.write(xml_name, pretty_print = True)

# Reading data from the xml file, then parsing it with beautifulsoup
with open(xml_name, 'r') as f:
    data = f.read()
bs_data = BeautifulSoup(data, 'xml')

# Declaring variables
pages = bs_data.find_all('LTPage')
c_titles, c_urls, c_categories, c_beneficiaries,  c_availability, c_pcode = [], [], [], [], [], []
col1, col2, col3, col4, col5, col6 = 'Name', 'URL', 'Category', 'Beneficiaries', 'Availability', 'Product code'

# Run through all pages with index
for index, page in enumerate(pages):
    # Skip first 6 pages of blabla
    if index <= 5:
        continue

    # Bools to determine when we are in the right place
    is_service_page, is_beneficiary, is_availability, is_pcode, is_category = False, False, False, False, False
    # Strings for easier concatenation (since info can be spread over multiple text blocks)
    page_title, page_beneficiaries, page_availability, page_pcode, page_category = '', '', '', '', ''
    
    # Fetch all text blocks on a page
    page_texts = page.find_all('LTTextBoxHorizontal')
    
    # Find page title
    for page_text in page_texts:
        # The first 0-3 are the page title, then comes the "Service/tool" description - so break when you reach that
        if page_text.text.startswith('Service/tool'):
           is_service_page = True
           break
        page_title += page_text.text

    # Ignore pages that aren't a service page
    if not is_service_page:
        continue

    # Find Beneficiaries - text found between "Beneficiaries" and "Availability"
    for page_text in page_texts:
        if page_text.text.startswith('Beneficiaries'):
            is_beneficiary = True
            continue

        if page_text.text.startswith('Availability'):
            is_beneficiary = False
            break

        if is_beneficiary:  
            page_beneficiaries += page_text.text

    # Find Availability - text found between "Availability" and "Product code"
    for page_text in page_texts:
        if page_text.text.startswith('Availability'):
            is_availability = True
            continue

        if page_text.text.startswith('Product code'):
            is_availability = False
            break

        if is_availability:  
            page_availability += page_text.text


    # Find Product code - text between "Product code" and "EUROCONTROL PRODUCTS & SERVICES CATALOGUE"
    # /!\ Products & services catalogue can have a page number before or after, so check for substring in string
    for page_text in page_texts:
        if page_text.text.startswith('Product code'):
            is_pcode = True
            continue

        if 'EUROCONTROL PRODUCTS & SERVICES CATALOGUE' in page_text.text:
            is_pcode = False
            break

        if is_pcode:  
            page_pcode += page_text.text

    # Find Activity - only text after EUROCONTROL PRODUCTS & SERVICES CATALOGUE
    # /!\ can be empty
    for page_text in page_texts:
        if 'EUROCONTROL PRODUCTS & SERVICES CATALOGUE' in page_text.text:
            is_category = True
            continue

        if len(page_text.get_text(strip=True)) > 0: 
            page_category += page_text.text
            break

        #if is_category & not page_text.text.is_empty_element:  
        #    page_category += page_text.text
        else:
            page_category += 'Empty'
            break

    # Print outputs and place info in arrays
    # /!\ clean up page title: some of them don't have white space
    print('Page title is: ' + page_title)
    #final_page_title = page_title.split(' ', 1)
    c_titles.append(page_title)

    print('Beneficiaries are: ' + page_beneficiaries)
    c_beneficiaries.append(page_beneficiaries)

    print('Availability is: ' + page_availability)
    c_availability.append(page_availability)

    print('Product code is: ' + page_pcode)
    c_pcode.append(page_category)

    print('Category is: ' + page_category)
    c_categories.append(page_category)

    # Find annotations - because they contain Links
    # /!\ can be multiple
    annots = page.find_all('Annot')
    if annots:
        for annot in annots:
            urls = annot.get('URI')
            #print(urls)

# Build dataframe with all the info we obtained
#catalogue_df = pd.DataFrame({col1: c_titles, col2: c_urls, col3: c_categories, col4: c_beneficiaries, col5: c_availability, col6: c_pcode})