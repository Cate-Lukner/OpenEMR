"""
PDF Data Extractor

Author: Catherine Lukner

"""

# Imports

import PyPDF2 as p2
import textract

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

filename = "sample3.pdf"

pdfFileObj = open(filename, 'rb')
pdfReader = p2.PdfFileReader(pdfFileObj)

# Discerning the number of pages to allow us to parse through all the pages
num_pages = pdfReader.numPages
count = 0
text = ""

# Read through each page.
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count += 1
    text += pageObj.extractText()

# check if the library above returned words
if text != "":
    text = text

# If false above, use the OCR library textract to 
# convert scanned/image based PDF files into text.

else:
    text = textract.process(filename, method='tesseract', language='eng')

# This tokenizes the words, but I am not sure if I need it
"""
tokens = word_tokenize(text)

punctuations = ['(',')',';',':','[',']', ',']

stop_words = stopwords.words('english')

keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

print(keywords)
"""
