# PDF Query to read the PDF catalogue
from pdfquery import PDFQuery
# Pandas for easier analysis etc.
import pandas as pd
# BeautifulSoup to read XML
from bs4 import BeautifulSoup

# Load the PDF catalogue and convert it to XML for readability
pdf = PDFQuery('catalogue.pdf')
pdf.load()
pdf.tree.write('catalogue.xml', pretty_print = True)