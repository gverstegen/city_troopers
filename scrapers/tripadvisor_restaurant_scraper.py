import lxml.html
import requests
import pandas as pd
import time
import re

domain = "https://www.tripadvisor.nl"
#start_uri = "/Restaurants-g188632-Rotterdam_South_Holland_Province.html#EATERY_OVERVIEW_BOX"
start_uri = "/Restaurants-g293974-Istanbul.html"

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
        items = root.xpath(".//*[@id='EATERY_SEARCH_RESULTS']/div[contains(@class, 'listing rebrand listingIndex')]")
        for i in items:
            itemName = i.xpath(".//*[contains(@class, 'title')]/a/text()")[0]
            itemName = itemName.replace("\n", "")

            itemUri = i.xpath(".//*[contains(@class, 'title')]/a/@href")[0]
            itemUri = itemUri.replace("\n", "")

            itemLink = domain + itemUri
            itemLink = itemLink.replace("\n", "")

            try:
                itemRank = i.xpath(".//*[contains(@class, 'popIndex rebrand popIndexDefault')]/text()")[0]
                itemRank = itemRank.replace("\n", "")
            except:
                itemRank = None
            try:
                itemRating = i.xpath(".//*[contains(@class, 'bubble_rating')]/@alt")[0]
                itemRating = itemRating.replace("\n", "")
            except:
                itemRating = None
            try:
                itemReviews = i.xpath(".//*[contains(@class, 'reviewCount')]/a/text()")[0]
                itemReviews = itemReviews.replace("\n", "")
                itemReviews = re.findall("\d+", itemReviews)[0]
            except:
                itemReviews = None
            try:
                itemPrice = i.xpath(".//*[@class='item price']/text()")[0]
                itemPrice = itemPrice.replace("\n", "")
            except:
                itemPrice = None
            row = [itemName, itemLink, itemRank, itemRating, itemReviews, itemPrice]
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

    print("Requesting url...")
    attempt = 1
    while True:
        try:
            r = requests.get(next_page_url, timeout = 5)
            print("Success")
            break
        except requests.exceptions.Timeout:
            attempt += 1
            print(attempt)
            continue
    root = lxml.html.fromstring(r.content)

df_restaurants = pd.DataFrame(output, columns=['Name', 'Link', 'Rank', 'Rating', 'Reviews', 'Price'])
df_restaurants.to_csv("C:/Users/gjave/Desktop/restaurants_istanbul.csv", sep = '|', encoding='UTF-8',index=False)