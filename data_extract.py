from bs4 import BeautifulSoup
import json
import os
import random
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
prefs = {"profile.managed_default_content_settings.images": 2,'profile.managed_default_content_settings.javascript': 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

# getting urls to scrape through
with open('url_database.json','r+') as file:
    data = json.load(file)

# shorts for some repeating code blocks
def find_text(xpath):
    try:
        return driver.find_element(By.XPATH,xpath).text
    except: 
        return None

def check_for_div(xpath):
    try:
        return driver.find_element(By.XPATH,xpath)
    except: 
        return None


for dic_t in data['url_list'] :
    driver.get(dic_t['bn_url'])
    # 
    if check_for_div('//*[@id="indications"]')!= None:
        pass
    else:
        print(i)


time.sleep(10)
driver.quit()