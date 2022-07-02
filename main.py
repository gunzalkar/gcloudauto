#import necessary libraries
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}

df = pd.read_csv("New_Submissions_Sheet1.csv")
df['Low Rent'] = df['Budget'] * 0.85
df['High Rent'] = df['Budget'] * 1.1
# df = df.drop([0, 1, 2, 3, 4, 5])
print(df.head())
df['Move-In Date'] = df['Move-In Date'] + ' 2022'
df['Bathrooms'] = df['Bathrooms'].astype('int')
df['Neighborhoods'] = df['Neighborhoods'].apply(lambda x: str(x).split(';'))

links_list = []
for index, row in df.iterrows():
# for index in range(len(df_test)):
    print('=======the index =============', index)
    # row = df.iloc[index+2, ]
    print('=============')
    print(f"On row with name {row['First Name']} {row['Last Name']}" )
    print('=============')
    areas_value = row['Neighborhoods']
    bed_value = int(row['Bedrooms'])
    bath_value = row['Bathrooms']
    low_rent = row['Low Rent']
    high_rent = row['High Rent']
    date_from = row['Move-In Date']
    link_to_use = row['Agent YGL Site']
    
    #instantiate the Chrome class web driver and pass the Chrome Driver Manager
    driver = webdriver.Chrome(options=chrome_options)
    

    #Maximize the Chrome window to full-screen
    driver.maximize_window() 

    driver.get(link_to_use)
    try:
        for area in areas_value:
            print(area)
            if ((area == "Other (Not Listed Here)") or (area == "Malden") or (area == "Medford")):
                pass
            else:
                area_value = area.replace(' - ', ':')
                areas = driver.find_element(By.ID, 'areas')
                Select(areas).select_by_value(area_value)
    except:
        pass
        


    try:
        beds_from = driver.find_element(By.ID, 'beds_from')
        beds_from_select = Select(beds_from).select_by_index(bed_value + 1)
    except:
        pass
    
    try:
        beds_to = driver.find_element(By.ID, 'beds_to')
        beds_to_select = Select(beds_to).select_by_index(bed_value + 1)
    except:
        pass

    try:
        baths = driver.find_element(By.ID, 'baths')
        baths_select = Select(baths).select_by_index(bath_value)
    except:
        pass
    
    try:
        rent_from = driver.find_element(By.ID, 'rent_from')
        rent_from_select = Select(rent_from).select_by_index(int(low_rent/100))
    except:
        pass
    
    try:
        rent_to = driver.find_element(By.ID, 'rent_to')
        rent_to_select = Select(rent_to).select_by_index(int(high_rent/100))
    except:
        pass



    driver1 = driver.find_element(By.XPATH, '//*[@id="date_from"]')
    driver1.click()
    


    current_month = driver1.find_element(By.XPATH, "/html/body/div/div[3]/ul[1]/li[2]")
    while current_month.text != date_from:
        button1 = driver1.find_element(By.XPATH, "/html/body/div/div[3]/ul[1]/li[3]")
        
        print("Element is visible? " + str(button1.is_displayed()))
        button1.click()
        

    driver1.find_element(By.XPATH, "//li[text()='1']").click()
    driver2 = driver.find_element(By.XPATH, '//*[@id="date_to"]')
    driver2.click()



    current_month = driver2.find_element(By.XPATH, "//li[text()='July 2022']")
    while current_month.text != date_from:
        button = driver2.find_element(By.XPATH, "/html/body/div[2]/div[3]/ul[1]/li[3]")
        
        print("Element is visible? " + str(button.is_displayed()))
        button.click()
    
    if date_from == 'August 2022':
        driver2.find_element(By.XPATH, "/html/body/div[2]/div[3]/ul[3]/li[2]").click()
    elif date_from == 'July 2022':
        driver2.find_element(By.XPATH, "/html/body/div[2]/div[3]/ul[3]/li[6]").click() 
    elif date_from == 'September 2022':
        driver2.find_element(By.XPATH, "/html/body/div[2]/div[3]/ul[3]/li[5]").click()
    elif date_from == 'October 2022':
        driver2.find_element(By.XPATH, "/html/body/div/div[3]/ul[3]/li[7]").click()
    elif date_from == 'November 2022':
        driver2.find_element(By.XPATH, "/html/body/div/div[3]/ul[3]/li[3]").click()
    elif date_from == 'December 2022':
        driver2.find_element(By.XPATH, "/html/body/div/div[3]/ul[3]/li[5]").click()


    try:
        driver.find_element(by=By.XPATH, value='/html/body/main/form/div/div[1]/div/div[2]/div[2]/div[3]/div/div[3]/button/i').click()
        
    except:
        driver.find_element(by=By.XPATH, value='//*[@id="search_btn"]').click()
    

    print('====================================')
    print()
    print(driver.current_url)
    links_list.append(driver.current_url)
    # print(links_list)
linkss = pd.Series(links_list)
linkss.to_csv('links.csv')
new_result = pd.concat([df.reset_index(), pd.Series(links_list)], axis=1, ignore_index=True)
print(new_result)
new_result.to_csv('test2_result.csv')

