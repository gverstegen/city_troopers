from selenium import webdriver
import time
import pandas as pd

driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")
driver.get("https://www.tripadvisor.nl/Attractions-g188632-Activities-Rotterdam_South_Holland_Province.html#FILTERED_LIST")

output = []
while True:
    pageOutput = []
    try:
        attractions = driver.find_elements_by_xpath("//*[@id='FILTERED_LIST']/*[@class='attraction_element']")
    except Exception:
        print("No attractions on this page.")

    for attr in attractions:
        attrName = attr.find_element_by_xpath(".//*[contains(@class, 'listing_title')]/a").text
        attrLink = attr.find_element_by_xpath(".//*[contains(@class, 'listing_title')]/a").get_attribute("href")
        attrRank = attr.find_element_by_xpath(".//*[@class='listing_rating']/div[3]").text
        try:
            attrRating = attr.find_element_by_xpath(".//*[contains(@class, 'rs rating')]/*[contains(@class, 'bubble_rating')]").get_attribute("alt")
        except:
            attrRating = 'No Rating'
        try:
            attrReviews = attr.find_element_by_xpath(".//*[contains(@class, 'rs rating')]/span[2]/a").text
        except:
            attrReviews = 'No Reviews'

        row = [attrName, attrLink, attrRank, attrRating, attrReviews]
        pageOutput.append(row)

    try:
        elem2 = driver.find_element_by_link_text("Nu liever niet.")
        print("Pop up")
        elem2.click()
        time.sleep(5)
    except:
        print("No pop-up.")

    try:
        elem1 = driver.find_element_by_xpath(".//*[contains(@class, 'nav next')]")
        elem1.click()
    except:
        print("Next page can't be reached.")
        break
    output.extend(pageOutput)
    time.sleep(5)

df_attractions = pd.DataFrame(output, columns=['Name', 'Link', 'Rank', 'Rating', 'Reviews'])
df_attractions.to_csv("C:/Users/gjave/Desktop/attractions.csv", sep = '|', encoding='UTF-8')