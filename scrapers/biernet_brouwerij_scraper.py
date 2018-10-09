import lxml.html
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
domain = "https://www.biernet.nl"
url = domain + "/bier/brouwerijen"
browser.get(url) #navigate to the page

element1 = browser.find_element_by_id("bottom_list")
actions = ActionChains(browser)
actions.move_to_element(element1).perform()
body = browser.find_element_by_css_selector('body')
body.send_keys(Keys.PAGE_DOWN)

while True:
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_DOWN)
    element2 = browser.find_element_by_id("bottom_list")
    actions = ActionChains(browser)
    actions.move_to_element(element2).perform()
    find_elem = browser.find_element_by_xpath(".//*[@id='bottom_list']").get_attribute('style')
    time.sleep(1)
    if find_elem == 'display: none;':
        break

try:
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    root = lxml.html.fromstring(innerHTML)
    items = root.xpath(".//*[@id='brouwerijLijst']")
    output_list_brouwerij = []
except:
    print('error')

page_list = []
try:
    items = root.xpath(".//*[@id='brouwerijLijst']/li")
except:
    print('no items found')
for i in items:
    try:
        brouwerij = i.xpath(".//h2/a/text()")[0]
    except:
        brouwerij = ''
    try:
        stad = i.xpath(". //p/a[1]/text()")[0]
    except:
        stad = ''
    try:
        provincie = i.xpath(". //p/a[2]/text()")[0]
    except:
        provincie = ''
    try:
        url = domain +  i.xpath(". //a/@href")[0]
    except:
        url = ''
    # Break if last row of the table has been reached

    # Append the new row data
    row = [brouwerij, stad, provincie, url]
    page_list.append(row)

# Add the new page data
output_list_brouwerij.extend(page_list)

df_brouwerij = pd.DataFrame(output_list_brouwerij, columns=['brouwerij', 'stad', 'provincie', 'url'])
df_brouwerij.to_csv("C:/Users/gjave/Desktop/brouwerijen1.csv", sep='|', encoding='UTF-8',index=False)