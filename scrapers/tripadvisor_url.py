from selenium import webdriver
import pandas as pd

def get_url(trip_url):
    browser = webdriver.Chrome()
    browser.get(trip_url) #navigate to the page
    element = browser.find_element_by_xpath(".//*[@class = 'blEntry website']")
    element.click()
    windows = browser.window_handles
    browser.switch_to.window(windows[1])
    return_url = browser.current_url
    browser.quit()
    return return_url

def add_url_column(df, trip_url_feature, output_feature):
    trip_url_list = df[trip_url_feature].tolist()
    url_list = []
    count = 1
    for i in trip_url_list:
        print("item " + str(count))
        try:
            url = get_url(i)
        except:
            url = ''
        print(url)
        url_list.append(url)
        count += 1

    df[output_feature] = url_list
    return df

file_path = "C:/Users/gjave/Desktop/Scraped/restaurants.csv"
file = pd.read_csv(file_path, sep='|')
df_output = add_url_column(file, 'Link', 'url_scrape')
