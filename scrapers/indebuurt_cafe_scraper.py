import lxml.html
import requests
import pandas as pd
import time
import re

domain = "https://indebuurt.nl"
start_uri = "/rotterdam/gids/rubrieken/cafes/"
start_page_url = domain + start_uri

# Request connection to page
r = requests.get(start_page_url)
# Get content as string
root = lxml.html.fromstring(r.content)

pageNumber = 1
output = []

while True:
    pageOutput = []
    try:
        items = root.xpath(".//*[@class='guide-items']//*[@class='guide-item']")

        for i in items:
            itemName = i.xpath(".//div/h2/text()")[0]
            itemName = itemName.replace("\n", "")

            itemLink = i.xpath(".//a/@href")[0]
            itemLink = itemLink.replace("\n", "")

            itemAddress = i.xpath(".//div/address/text()")[0]
            itemAddress = itemAddress.replace("\n", "")

            row = [itemName, itemLink, itemAddress]
            pageOutput.append(row)
        output.extend(pageOutput)
    except Exception:
        print("No items on this page.")

    # Avoid request overload
    time.sleep(1)

    # Get to the next page, if possible
    try:
        next_page_url = root.xpath(".//*[@class = 'next page-numbers']/@href")[0]
        pageNumber = pageNumber + 1
        print("Page number is now " + str(pageNumber))
        print("Url of page " + str(pageNumber) + " is: " + next_page_url)
    except Exception:
        print("Next page not found")
        break
    r = requests.get(next_page_url)
    root = lxml.html.fromstring(r.content)

df_cafes = pd.DataFrame(output, columns=['Name', 'Link', 'Address'])
df_cafes.to_csv("C:/Users/gjave/Desktop/cafes.csv", sep='|', encoding='UTF-8',index=False)