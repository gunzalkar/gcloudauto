#import necessary libraries
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

df = pd.read_csv("YGL ID To URL For Incubator (1).csv")
df = df.drop('AAB URL', axis=1)
new_list = []


for index, row in df.iterrows():
    #instantiate the Chrome class web driver and pass the Chrome Driver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #Maximize the Chrome window to full-screen
    driver.maximize_window() 
    # chrome_options.add_argument("window-size=1200x600")
    driver.get("https://www.allaccessboston.com/rental_searches")

    # driver.implicitly_wait(20)
    search_id = driver.find_element(By.XPATH, '//*[@id="rental_search_listing_ids"]').send_keys(int(row["YGL ID"]))

    driver.find_element(By.XPATH, '//*[@id="advancedSearchForm"]/div[2]/input[1]').click()
    # time.sleep(1)
    print(driver.current_url)

    new_list.append(driver.current_url)

# print(df.tail())
new_list = pd.Series(new_list)
new_list.to_csv('links.csv')
new_result = pd.concat([df.reset_index(), pd.Series(new_list)], axis=1, ignore_index=True)
print(new_result.columns)
new_result = new_result.iloc[:, 1:4]
new_result = new_result.set_axis(['Contact ID', 'YGL ID', 'AAB URL'], axis=1)
print(new_result)
new_result.to_csv('incubator links.csv')
    