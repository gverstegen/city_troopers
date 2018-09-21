import lxml.etree
import lxml.html
import requests
import pandas as pd

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from lxml import html

class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()


pageNumber = 1
output_list_brouwerij = []

while True:
    # Request connection to page
    r = requests.get("https://www.biernet.nl/bier/brouwerijen")
    r = requests.get("https://www.biernet.nl/bier/brouwerijen?center=49.386571988986745,-15.80344336947519&zoom=4&filters=brouwerij,brouwerij_huurder")

    # Get content as string
    root = lxml.html.fromstring(r.content)

    # If there is an error on the page, quit
    error = root.xpath("//div[contains(@class, 'error')]/text()")
    if error != [] and error != ['De map functioneert alleen wanneer Javascript aan staat.']:
        print("Page returns an error.")
        break

    print("Scraping page.")
    # Page output
    page_list = []
    i = 1
    while True:
        # Get the values of interest
        try:
            brouwerij = root.xpath("//*[@id='brouwerijLijst']/li[1]/text()")
        except:
            brouwerij = ''
        try:
            stad = root.xpath("//*[@id='brouwerijLijst']/li[1]/p/a[1]/text()")
        except:
            stad = ''
        try:
            provincie = root.xpath("//*[@id='brouwerijLijst']/li[1]/p/a[2]/text()")
        except:
            provincie = ''

        # Hier moet nog een loop omheen
        try:
            perks = root.xpath("//*[@id='brouwerijLijst']/li[1]/div/text()")
        except:
            perks = ''

        # Break if last row of the table has been reached
        if (brouwerij == ''  and stad == '' and provincie == '' and perks == ''):
            break

        # Append the new row data
        row = [brouwerij, stad, provincie, perks]
        page_list.append(row)
        i = i + 1

    # Add the new page data
    output_list_brouwerij.extend(page_list)
    pageNumber = pageNumber + 1

df_brouwerij = pd.DataFrame(output_list_brouwerij, columns=['brouwerij', 'stad', 'provincie', 'perks'])
