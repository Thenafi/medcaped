import json
import shutil
import sys
from bs4 import BeautifulSoup
import os
import re

cwd =  os.getcwd()

#  need to exclude the git ignore and bangla file
dir_list = os.listdir(cwd+"/bs4/html")[1:-1]

if len(dir_list)<=2:
    print("No html or data files. Extract html files")
    sys.exit()

#shorting language specific file and filtering invalid/ no data medicines 
not_bangla= []
for index,i in enumerate(dir_list):
    file= cwd+"/bs4/html/"+i
    dst= cwd+"/bs4/html"+"/bangla/"+i
    print(index,end='\r')
    with open(file, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, 'html5lib')
    id_indications = soup.find(id="indications")
    if id_indications != None:
        if id_indications.get_text() == "নির্দেশনা":
               shutil.move(file, dst)
        else:
            not_bangla.append(i)
    else :
        print(index+'failed to fin indications')
print(not_bangla)

dir_list = os.listdir(cwd+"/bs4/html/bangla")[1:]
# saving data as json file
for index,i in enumerate(dir_list):
    med_data = {}
    file= cwd+"/bs4/html/bangla/"+i
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

    with open(f'{cwd}/bs4/json/{med_data["med_id"]}.json', 'w+') as fp:
        json.dump(med_data, fp)
