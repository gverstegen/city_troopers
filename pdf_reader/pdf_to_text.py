import PyPDF2
import re
import pandas as pd

pdfFileObj = open('C:/Users/gjave/Desktop/Biergarten2018-BASISMENU-DRIELUIK-JUNI-FOOD.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pdfReader.numPages
pageObj = pdfReader.getPage(0)
text = pageObj.extractText()
text

menu_items = re.findall(".*\\n", text)
df_menu = pd.DataFrame(menu_items, columns=['item'])

import pdfminer.six

import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text

if __name__ == '__main__':
    print(extract_text_from_pdf('C:/Users/gjave/Desktop/Biergarten2018-BASISMENU-DRIELUIK-JUNI-FOOD.pdf'))

from pdftablr.table_extractor import Extractor
import pdftotree
pdftotree.parse('C:/Users/gjave/Desktop/Biergarten2018-BASISMENU-DRIELUIK-JUNI-FOOD.pdf', html_path=None, model_type=None, model_path=None, favor_figures=True, visualize=False)
