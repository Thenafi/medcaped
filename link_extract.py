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


options = Options()
def randomuseragent():
    with open(os.getcwd() + "/files/user-agents_chrome_browser_96-0.txt") as f:
        io = f.read().splitlines()
        return random.choice(io)
options.add_argument(f'user-agent={randomuseragent()}')

driver = webdriver.Chrome(ChromeDriverManager().install())
data = {
    "first": "https://medex.com.bd/brands",
    "url":[]
}

with open('data.json','r+') as file:
    file_data = json.load(file)
    data =  file_data
data['url'] = list(set(data['url']))
time.sleep(15)


for i in range(200):
    if 'last' in data:
        driver.get(data['last'])
    else:
        driver.get(data['first'])
    data['url'] = list(set(data['url']))
    try:
       element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'List of Brand Names')]")))
    except Exception as e:
        print("Not in brand's Page")
        break
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li/a[@rel="next"]'))
        )
        element = driver.find_element(By.XPATH, '//li/a[@rel="next"]')
        data['last']=element.get_attribute("href")
        print(data['last'])
        element.click()
    except Exception as e:
        print(e, "Page Link error")
        break
    try:
        elements = driver.find_elements(By.XPATH, '//a[@class="hoverable-block"]')
    except Exception as e:
        print("Link Extraction Error")
    for i in elements:
        data['url'].append(i.get_attribute("href"))
        
    with open('data.json', 'w') as fp:
        json.dump(data, fp)


driver.quit()