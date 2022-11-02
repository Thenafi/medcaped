from concurrent import futures
import json
import os
import random
import re
import time
from urllib import response
import uuid
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
cwd =  os.getcwd()
try:
    with open(f'{cwd}/oushodbarta/url_database.json','r+') as file:
        file_data = json.load(file)
        data =  file_data
except:
    data = {
        "first": "https://ousudbarta.com/category/%e0%a6%94%e0%a6%b7%e0%a6%a7-%e0%a6%a4%e0%a6%a5%e0%a7%8d%e0%a6%af/",
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
        if res.status_code!=200:
            continue
        break
    # getting next page link
    next_page_ele= soup.find("a",string="Next")
    if next_page_ele!= None:
        data['last']=next_page_ele['href']
        print(data['last'])
    else:
        return "No Page"

    # extracting medicine urls
    med_brand_link = soup.find_all("h1",{"class":"title gradient-effect"})

    for i in med_brand_link:
        data['url_list'].append({
            "id" : str(uuid.uuid4()),
            "url": i.a['href'],
            "scraped": False
        })
    with open(f'{cwd}/oushodbarta/url_database.json','w+') as file:
        json.dump(data, file)
    return "Success"

res_list=[]

for _ in range(100):
    res_list.append(get_link(_))
print(res_list)

# #sometimes file get corrupted because of threading thats why saving file at last
# with open(f'{cwd}/oushodbarta/url_database.json','w+') as file:
#     json.dump(data, file)