from selenium import webdriver
import time
import pandas as pd

driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")
driver.get("https://www.tripadvisor.nl/Restaurants-g188632-Rotterdam_South_Holland_Province.html#EATERY_OVERVIEW_BOX")

output = []
while True:
    pageOutput = []
    try:
        restaurants = driver.find_elements_by_xpath("//*[@id='EATERY_SEARCH_RESULTS']/div[contains(@class, 'listing rebrand listingIndex')]/div[2]/div[1]")
    except Exception:
        print("No restaurants on this page.")

    for rest in restaurants:
        restName = rest.find_element_by_xpath(".//div[1]/a").text
        restLink = rest.find_element_by_xpath(".//div[1]/a").get_attribute("href")
        restRank = rest.find_element_by_xpath(".//div[3]/div").text
        try:
            restRating = rest.find_element_by_xpath(".//div[2]/span").get_attribute("alt")
        except:
            restRating = 'No Rating'
        try:
            restReviews = rest.find_element_by_xpath(".//*[@class='reviewCount']/a").text
        except:
            restReviews = 'No Reviews'
        try:
            restPrice = rest.find_element_by_xpath(".//*[@class='item price']").text
        except:
            restPric = 'No Price Information'
        row = [restName, restLink, restRank, restRating, restReviews, restPrice]
        pageOutput.append(row)

    try:
        elem1 = driver.find_element_by_link_text("Volgende")
        elem1.click()
    except:
        print("Next page can't be reached.")
        break
    output.extend(pageOutput)
    time.sleep(5)

df_restaurants = pd.DataFrame(output, columns=['Name', 'Link', 'Rank', 'Rating', 'Reviews', 'Price'])
df_restaurants.to_csv("C:/Users/gjave/Desktop/restaurants.csv", sep = '|', encoding='UTF-8')