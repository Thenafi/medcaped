import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

ua = UserAgent()
options = Options()
options.add_argument(f'user-agent={ua.random}')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

cwd =  os.getcwd()

with open(f'{cwd}/selenium/url_database.json','w+') as file:
    try:
        file_data = json.load(file)
        data =  file_data
    except:
        data = {
            "first": "https://medex.com.bd/brands",
            "url_list":[]
        }

print('Starting in 5 seconds')      
time.sleep(5)

# for going through pages and extracting URLs of the medicine
for i in range(750):
    while True:
        if 'last' in data:
            driver.get(data['last'])
        else:
            driver.get(data['first'])
        # sometimes website blocks access for a user agent so changing it to a random one
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'List of Brand Names')]")))
        except Exception as e:
            print("Not in brand's Page")
            driver.quit()
            options.add_argument(f'user-agent={ua.random}')
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            continue
        break
    
    # going to the next page
    try:
        next_page_button = driver.find_element(By.XPATH, '//li/a[@rel="next"]')
        data['last']=next_page_button.get_attribute("href")
        print(data['last'])
        next_page_button.click()
    except Exception as e:
        print("Next page link error/ No more p\age")
        break

    #extracting the URLs for the medicine is available
    try:
        medicine_url = driver.find_elements(By.XPATH, '//a[@class="hoverable-block"]')
    except Exception as e:
        print("Link Extraction Error")
    for i in medicine_url:
        extracted_medicine_url = i.get_attribute("href")
        temp_dictionary= {
            "url": extracted_medicine_url,
            "bn_url": extracted_medicine_url +"/bn",
            "scraped": False
        }
        data['url_list'].append(temp_dictionary)
        
    with open(f'{cwd}/selenium/url_database.json', 'w') as fp:
        json.dump(data, fp)


driver.quit()