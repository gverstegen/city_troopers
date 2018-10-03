import lxml.html
import requests
import pandas as pd
import time
import re

domain = "https://www.tripadvisor.nl"
start_uri = "/Attractions-g188632-Activities-Rotterdam_South_Holland_Province.html#FILTERED_LIST"
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
        items = root.xpath(".//*[@id='FILTERED_LIST']/*[@class='attraction_element']")
        for i in items:
            itemName = i.xpath(".//*[contains(@class, 'listing_title')]/a/text()")[0]
            itemName = itemName.replace("\n", "")

            itemUri = i.xpath(".//*[contains(@class, 'listing_title')]/a/@href")[0]
            itemUri = itemUri.replace("\n", "")

            itemLink = domain + itemUri
            itemLink = itemLink.replace("\n", "")
            try:
                itemRank = i.xpath(".//*[@class='listing_rating']/div[3]/text()")[0]
                itemRank = itemRank.replace("\n", "")
            except:
                itemRank = None
            try:
                itemRating = i.xpath(".//*[contains(@class, 'rs rating')]/*[contains(@class, 'bubble_rating')]/@alt")[0]
                itemRating = itemRating.replace("\n", "")
            except:
                itemRating = None
            try:
                itemReviews = i.xpath(".//*[contains(@class, 'rs rating')]/span[2]/a/text()")[0]
                itemReviews = itemReviews.replace("\n", "")
                itemReviews = re.findall("\d+", itemReviews)[0]
            except:
                itemReviews = None

            row = [itemName, itemLink, itemRank, itemRating, itemReviews]
            pageOutput.append(row)
        output.extend(pageOutput)
    except Exception:
        print("No items on this page.")

    # Avoid request overload
    time.sleep(1)

    # Get to the next page, if possible
    try:
        next_uri = root.xpath(".//*[contains(@class, 'nav next')]/@href")[0]
        next_page_url = domain + next_uri
        pageNumber = pageNumber + 1
        print("Page number is now " + str(pageNumber))
        print("Url of page " + str(pageNumber) + " is: " + next_page_url)
    except Exception:
        print("Next page not found")
        break
    r = requests.get(next_page_url)
    root = lxml.html.fromstring(r.content)

df_attractions = pd.DataFrame(output, columns=['Name', 'Link', 'Rank', 'Rating', 'Reviews'])
df_attractions.to_csv("C:/Users/gjave/Desktop/attractions.csv", sep = '|', encoding='UTF-8', index=False)