import json
import os
import random
import re
import requests
from concurrent import futures
from dotenv import load_dotenv

load_dotenv()
def randomuseragent():
    with open(os.getcwd() + "/files/user-agents_chrome_browser_96-0.txt") as f:
        io = f.read().splitlines()
        return random.choice(io)

data={}   
with open('data.json','r+') as file:
    file_data = json.load(file)
    data =  file_data

YOUR_API_KEY = os.getenv("YOUR_API_KEY")

dic_list= [dic for dic in data['url_list']][19600:22000]


def getData(object_data):
    if object_data['scraped']==False:
        medicine_id= re.findall("([0-9]+)",object_data["bn_url"])[0]
        headers = {"User-Agent": randomuseragent()}
        print(medicine_id,end='\r')
        url = f'https://api.rocketscrape.com/?apiKey={YOUR_API_KEY}&url={object_data["bn_url"]}&keep_headers=true'
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            with open(f"data/{medicine_id}.html", "w+",encoding="utf-8") as file1:
                file1.writelines(res.text)
            object_data['scraped']= True

        return res.status_code
    else:
        return['Done',object_data ]

with futures.ThreadPoolExecutor(max_workers=4) as executor:
    res = executor.map(getData,dic_list)
responses = list(res)
with open('data.json', 'w+') as fp:
    json.dump(data, fp)
print(responses)