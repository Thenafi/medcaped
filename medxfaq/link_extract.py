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
    with open(f'{cwd}/medxfaq/url_database.json','r+') as file:
        file_data = json.load(file)
        data =  file_data
except:
    data = {
        "url_list":[
            {
                "url": "https://www.medicinesfaq.com/brand/bn/tulip",
                "scraped": False,
                "indexed": False
            }
        ],
    }


print(len(set([i['url'] for i in data['url_list']])))

# function that returns unique unindexed url
print(len(data['url_list']))
def get_unindexed():
    for i in data['url_list']:
        if i['indexed'] == False:
            return i
    return None



def get_link():
    print(len(data['url_list']))
    # get the length of unindexed url
    print( len([i for i in data['url_list'] if i['indexed'] == False]))
    temp_obj = get_unindexed()
    print(temp_obj)
    if temp_obj == None:
        return "Done"
    while True:
        res = requests.get(temp_obj['url'],headers={"User-Agent": ua.random})
        #update the indexed property to true for same urls
        for i in data['url_list']:
            if i['url'] == temp_obj['url']:
                i['indexed'] = True

        soup = BeautifulSoup(res.text, 'html5lib')
        if res.status_code!=200:
            return res.status_code
        break
    # getting next page link
    all_medicines= soup.select("body > div.q-container > div > div.rl-main > aside > div > p > a")
    for i in all_medicines:
        # check if the url is already present in the database
        if i['href'] not in [i['url'] for i in data['url_list']]:
            data['url_list'].append({
                "url": i['href'],
                "scraped": False,
                "indexed": False
            })
    # update the database with only unique urls using set method
    data['url_list'] = list({v['url']:v for v in data['url_list']}.values())

    with open(f'{cwd}/medxfaq/url_database.json','w+') as file:
        json.dump(data, file)
    return "Success"

res_list=[]

print(get_unindexed())
while get_unindexed() != None:
    get_link()

# #sometimes file get corrupted because of threading thats why saving file at last
# with open(f'{cwd}/medxfaq/url_database.json','w+') as file:
#     json.dump(data, file)