from concurrent import futures
import json
import os
import random
import re
import time
import uuid
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
cwd =  os.getcwd()
try:
    with open(f'{cwd}/shakal/url_database.json','r+') as file:
        file_data = json.load(file)
        data =  file_data
except:
    data = {
        "first": "https://www.shajgoj.com/category/health/",
        "url_list":[]
    }


def get_link(pa):
    global headers
    while True:
        if 'last' in data:
            try:
                res = requests.get(data['last'],headers={"User-Agent": ua.random})
            except:
                continue
        else:
            try:
                res = requests.get(data['first'],headers={"User-Agent": ua.random})
            except:
                continue
        # sometimes website blocks access for a user agent so changing it to a random one
        soup = BeautifulSoup(res.text, 'html5lib')
        list_of_brand_element = soup.select_one('#sf-module-category-title > h2')
        if list_of_brand_element!=None:
            if list_of_brand_element.get_text().strip() == "স্বাস্থ্য":
                pass
            else:
                print("Not in brand's Page")
                continue
        break

    # getting next page link
    next_page_ele= soup.find("a",{"class":"next page-numbers"})
    if next_page_ele!= None:
        data['last']=next_page_ele['href']
    else:
        return "No Page"

    # extracting medicine urls
    med_brand_link = soup.find_all("a",{"rel":"bookmark"})

    for i in med_brand_link:
        data['url_list'].append({
            "id" : str(uuid.uuid4()),
            "url": i['href'],
            "scraped": False
        })
    return "Success"


with futures.ThreadPoolExecutor(max_workers=5) as executor:
    res = executor.map(get_link,range(400))
responses = list(res)
print(responses)

#sometimes file get corrupted because of threading thats why saving file at last
with open(f'{cwd}/shakal/url_database.json','w+') as file:
    json.dump(data, file)