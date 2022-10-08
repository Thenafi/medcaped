from concurrent import futures
import json
import os
import random
import re
from tkinter.messagebox import NO
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
cwd =  os.getcwd()
with open(f'{cwd}/bs4/url_database.json','w+') as file:
    try:
        file_data = json.load(file)
        data =  file_data
    except:
        data = {
            "first": "https://medex.com.bd/brands",
            "url_list":[]
        }


def get_link(_):
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
        list_of_brand_element = soup.select_one('h1.col-xs-12')
        if list_of_brand_element!=None:
            if list_of_brand_element.get_text().strip() == "List of Brand Names":
                pass
            else:
                print("Not in brand's Page")
                continue
        break
    
    # getting next page link
    next_page_ele= soup.find("a",{"aria-label":"Next »"})
    if next_page_ele!= None:
        data['last']=next_page_ele['href']
    else:
        return "No Page"

    # extracting medicine urls
    med_brand_link = soup.find_all("a",{"class":"hoverable-block"})
    for i in med_brand_link:
        data['url_list'].append({
            "url": i['href'],
            'bn_url': i['href']+"/bn",
            "scraped": False
        })
    return "Success"



with futures.ThreadPoolExecutor(max_workers=5) as executor:
    res = executor.map(get_link,range(200))
responses = list(res)
print(responses)

#sometimes file get corrupted because of threading thats why saving file at last
with open(f'{cwd}/bs4/url_database.json','w+') as file:
    json.dump(data, file)