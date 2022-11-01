import json
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# for refreshing the driver with new user agent
def declare_driver():
    global driver
    ua = UserAgent()
    options = Options()
    options.add_argument(f'user-agent={ua.random}')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
declare_driver()

cwd =  os.getcwd()
# checking database existence and pulling data
try:
    with open(f'{cwd}/selenium/url_database.json','r+') as file:
        file_data = json.load(file)
        data =  file_data
except:
    print('you are missing the url database file')


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

for ind,ele in enumerate(data['url_list']):
    med_data = {
        "med_id": re.findall("([0-9]+)",ele['bn_url'])[0]
    }
    
    if ele['scraped'] == False:
        driver.get(ele["bn_url"])
        # checking if we are in medicine's page
        while True:
            i = 0
            # sometimes website blocks access for a user agent so changing it to a random one
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@class="dosage-icon"]')))
            except Exception as e:
                print("Not in  medicine's Page")
                driver.quit()
                declare_driver()
                i+=1
                if i>= 10:
                    print('Something is wrong while finding dosage icon', ele)
                    ele['scraped'] = True
                    with open(f'{cwd}/selenium/url_database.json', 'w') as fp:
                        json.dump(data, fp)
                    break
                continue
            break
    
    if ele['scraped'] == False:
        # Scraping for specific language- Here some else can also look for English or other value if any. Targeting the "indications" div. 
        if find_text('//*[@id="indications"]')== "নির্দেশনা":
            html_source = driver.page_source
            med_data['name'] = find_text('//span[contains(@style,"margin-right: 6px;")]').replace(find_text('//span//small[@class="h1-subtitle"]'),'')
            med_data['url'] = med_data['url'] = "https://medex.com.bd/brands/"+ med_data["med_id"]
            ac_body =  driver.find_elements(By.XPATH, '//div[@class="ac-body"]')
            for op,hy in enumerate(driver.find_elements(By.XPATH,'//h4[@class="ac-header"]')):
                med_data[hy.text] = ac_body[op].text

            with open(f'{cwd}/selenium/json/{med_data["med_id"]}.json', 'w') as fp:
                json.dump(med_data, fp)
            with open(f'{cwd}/selenium/html/{med_data["med_id"]}.html', 'w') as fp:
                json.dump(html_source, fp)
    # updating database
    ele['scraped'] = True
    with open(f'{cwd}/selenium/url_database.json', 'w') as fp:
        json.dump(data, fp)