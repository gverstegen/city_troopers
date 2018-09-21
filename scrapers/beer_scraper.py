import lxml.etree
import lxml.html
import requests
import pandas as pd

pageNumber = 1
output_list_bier = []

while True:
    # Request connection to page
    r = requests.get("https://www.biernet.nl/bier/merken?l=" + str(pageNumber))

    # Get content as string
    root = lxml.html.fromstring(r.content)

    # If there is an error on the page, quit
    error = root.xpath("//div[contains(@class, 'error')]/text()")
    if error != []:
        print("Page number " + str(pageNumber) + " returns an error. Page has no content to be scraped.")
        break

    print("Scraping page " + str(pageNumber))
    # Page output
    page_list = []
    i = 1
    while True:
        # Get the values of interest
        try:
            biermerk = root.xpath("//tbody/tr[" + str(i) + "]/td/a[contains(@href, 'merken')]/text()")[0]
        except:
            biermerk = ''
        try:
            biersoort = root.xpath("//tbody/tr[" + str(i) + "]/td/a[contains(@href, 'biersoorten')]/text()")[0]
        except:
            biersoort = ''
        try:
            brouwerij = root.xpath("//tbody/tr[" + str(i) + "]/td/a[contains(@href, 'brouwerijen')]/text()")[0]
        except:
            brouwerij = ''
        try:
            alcohol = root.xpath("//tbody/tr[" + str(i) + "]/td[4]/text()")[0]
        except:
            alcohol = ''

        # Break if last row of the table has been reached
        if (biermerk == ''  and biersoort == '' and brouwerij == '' and alcohol == ''):
            break

        # Append the new row data
        row = [biermerk, biersoort, brouwerij, alcohol]
        page_list.append(row)
        i = i + 1

    # Add the new page data
    output_list_bier.extend(page_list)
    pageNumber = pageNumber + 1

df_biermerken = pd.DataFrame(output_list_bier, columns=['biermerk', 'biersoort', 'brouwerij', 'alcohol'])
