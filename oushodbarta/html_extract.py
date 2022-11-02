from concurrent import futures
import hashlib
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
    with open(f'{cwd}/oushodbarta/url_database.json','r') as file:
        file_data = json.load(file)
        data =  file_data
except:
    print('you are missing the url database file. Run link extract')
    sys.exit()


err_dic={}
dic_list= [dic for dic in data['url_list']]
print(len(dic_list))

# getting full page data. here the language specific data can be filtered but chose to download all then filter later.
def getData(object_data):
    headers = {"User-Agent": ua.random}
    if object_data['scraped']== False:
        url = object_data['url']
        id = object_data['id']
        print(id,end='\r')
        for p in range(10):
            try:
                res = requests.get(url,headers=headers,allow_redirects=False ,timeout=15)
                if res.status_code==200:
                    for dic in data['url_list']:
                        if dic['id'] == id:
                            dic['scraped'] = True
                            break
                    with open(f"{cwd}/oushodbarta/html/{id}.html", "w+",encoding="utf-8") as file1:
                        print(res.encoding)
                        file1.write(str(BeautifulSoup(res.content, 'html5lib' , from_encoding="utf-8")))
                    break
            except Exception as e:
                print(e)
                if p>5:
                    err_dic[id] = {"url":url,"tries":p}

        return res.status_code
    else:
        return "Done"

# running multiple request to speed up the process
with futures.ThreadPoolExecutor(max_workers=4) as executor:
    res = executor.map(getData,dic_list)
responses = list(res)

print(len(responses))
print(err_dic)

#sometimes file get corrupted because of threading thats why saving file at last
with open(f'{cwd}/oushodbarta/url_database.json','w+') as file:
    json.dump(data, file)