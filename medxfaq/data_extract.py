import json
import time
import sys
from bs4 import BeautifulSoup
import os
import re
import requests
from bs4.dammit import EncodingDetector
    
cwd =  os.getcwd()
try:
    with open(f'{cwd}/medxfaq/url_database.json','r') as file:
        file_data = json.load(file)
except:
    print('you are missing the url database file. Run link extract')
    sys.exit()
#  need to exclude the git ignore and bangla folder
dir_list = os.listdir(cwd+"/medxfaq/html")[1:]
print(len(dir_list))


if len(dir_list)<=2:
    print("No html or data files. Extract html files")
    sys.exit()

# saving data as json file
for index,i in enumerate(dir_list):
    med_data = {}
    med_data["med_id"] = i.split(".")[0]
    file= cwd+"/medxfaq/html/"+i
    with open(file, encoding="utf-8") as fp:
        try:
            soup = BeautifulSoup(fp.read(), 'lxml' )
            med_data['title'] = soup.select_one('#introduction > a > h1').getText()  
            med_data['all_'] =soup.select_one("body > div.q-container > div > div.qa-main > main > div > article").getText().replace('\n','').replace('\r','').strip()
            sections = soup.select(".drug-details > section")
            for section in sections:
                section_name = section.select_one('div')
                if section_name:
                    section_name = section_name['id']
                if section_name != None:
                    try:
                        for i in soup.select("#uses > div"):
                            i.replace_with(" ")
                    except:
                        pass
                    med_data[section_name] = section.getText().replace('\n','').replace('\r','').strip()
                        
            with open(f'{cwd}/medxfaq/json/{med_data["med_id"]}.json', 'w+',encoding="utf-8", errors='ignore') as fp:
                json.dump(med_data, fp)

        except Exception as e:
            print(file , e)
