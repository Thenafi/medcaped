from concurrent import futures
import json
import os
import random
import re
import sys
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

cwd =  os.getcwd() 
try:
    with open(f'{cwd}/bs4/url_database.json','r+') as file:
        file_data = json.load(file)
        data =  file_data
except:
    print('you are missing the url database file. Run link extract')
    sys.exit()


dic_list= [dic for dic in data['url_list']][0:100]

# getting full page data. here the language specific data can be filtered but chose to download all then filter later.
def getData(object_data):
        medicine_id= re.findall("([0-9]+)",object_data["bn_url"])[0]
        headers = {"User-Agent": ua.random}
        print(medicine_id,end='\r')
        url = object_data['bn_url']
        res = requests.get(url,headers=headers,allow_redirects=False)
        soup = BeautifulSoup(res.text, 'html5lib')
        id_html = soup.find(id="indications")
        if id_html!=None:
            with open(f"{cwd}/bs4/html/{medicine_id}.html", "w+",encoding="utf-8") as file1:
                file1.writelines(res.text)
            return res.status_code
        else:
            return medicine_id

with futures.ThreadPoolExecutor(max_workers=20) as executor:
    res = executor.map(getData,dic_list)
responses = list(res)
print(responses)

for i,e in enumerate(responses):
    if e==200:
        data['url_list'][i]['scraped']= True

#sometimes file get corrupted because of threading thats why saving file at last
with open(f'{cwd}/bs4/url_database.json','w+') as file:
    json.dump(data, file)