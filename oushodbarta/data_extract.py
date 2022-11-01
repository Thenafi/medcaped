import json
import time
import sys
from bs4 import BeautifulSoup
import os
import re


cwd =  os.getcwd()
try:
    with open(f'{cwd}/shakal/url_database.json','r') as file:
        file_data = json.load(file)
except:
    print('you are missing the url database file. Run link extract')
    sys.exit()
#  need to exclude the git ignore and bangla folder
dir_list = os.listdir(cwd+"/shakal/html")[1:]
print(len(dir_list))


if len(dir_list)<=2:
    print("No html or data files. Extract html files")
    sys.exit()

# saving data as json file
for index,i in enumerate(dir_list):
    print(f"Loading {round(index*100/len(dir_list), 2)}%",end='\r')
    med_data = {}
    med_data["med_id"] = i.split(".")[0]
    file= cwd+"/shakal/html/"+i
    with open(file, encoding="utf-8") as fp:
        try:
            soup = BeautifulSoup(fp, 'html5lib')
            # cleaning the html
            for i in soup.select("div.woocommerce"):
                i.replace_with(" ")
            for i in soup.select("div.mashsb-box"):
                i.replace_with(" ")
            #get the url from the json file
            for dic in file_data['url_list']:
                if dic['id'] == med_data["med_id"]:
                    med_data['url'] = dic['url']
                    break
            
            med_data['title'] = soup.select_one('#sf-module-post > article > header > h1').getText().strip()
            med_data['name'] =soup.select_one("#sf-module-post > article > div.sf-entry-content.sf-has-dropcap").getText().replace('\n','').replace('\r','').strip()
            with open(f'{cwd}/shakal/json/{med_data["med_id"]}.json', 'w+',encoding="utf-8", errors='ignore') as fp:
                json.dump(med_data, fp)

        except Exception as e:
            print(file , e)
