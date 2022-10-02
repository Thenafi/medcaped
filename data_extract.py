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
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

driver.get("https://medex.com.bd/brands")

