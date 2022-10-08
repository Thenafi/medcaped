import json
from bs4 import BeautifulSoup
import os
import re
cwd =  os.getcwd()
dir_list = os.listdir(cwd+"/bangla")

data = []


for index,i in enumerate(dir_list):
    med_data = {}
    file= cwd+"/bangla/"+i
    print(index,end='\r')
    with open(file, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, 'html5lib')
    headers = soup.find_all("h4",{"class":"ac-header"})
    med_data['med_id'] = re.findall("([0-9]+)",i)[0]
    med_data['name'] =soup.find("h1", {"class":"page-heading-1-l"}).getText().replace('\n','').replace('\r','').strip()
    med_data['url'] = "https://medex.com.bd/brands/"+ i
    for i in headers:
        main_data_div = i.find_parent('div').find_parent('div')
        med_data[main_data_div.find("h4",{"class":"ac-header"}).get_text()] = main_data_div.find("div",{"class":"ac-body"}).get_text()

    data.append(med_data)


with open('final_data.json', 'w+') as fp:
    json.dump(data, fp)
