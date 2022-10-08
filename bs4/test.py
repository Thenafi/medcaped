from concurrent import futures
import json
import os
import random
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

data={}   
with open('data copy.json','r+') as file:
    file_data = json.load(file)
    data =  file_data

dic_list= [dic for dic in data['url_list']][19600:19700]


def getData(object_data):
        medicine_id= re.findall("([0-9]+)",object_data["bn_url"])[0]
        headers = {"User-Agent": ua.random}
        print(medicine_id,end='\r')
        url = object_data['bn_url']
        res = requests.get(url,headers=headers,allow_redirects=False)
       
        soup = BeautifulSoup(res.text, 'html5lib')
        id_html = soup.find(id="indications")
        if id_html!=None:
            with open(f"data45/{medicine_id}.html", "w+",encoding="utf-8") as file1:
                file1.writelines(res.text)
            return res.status_code
        else:
            return medicine_id

with futures.ThreadPoolExecutor(max_workers=20) as executor:
    res = executor.map(getData,dic_list)
responses = list(res)
print(responses)

