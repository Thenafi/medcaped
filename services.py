import json
import os
import re
import time 
from bs4 import BeautifulSoup
import shutil

data={}   
with open('data.json','r+') as file:
    file_data = json.load(file)
    data =  file_data

# print(len([dic for dic in data['url_list']]))


# checking number of files 

cwd = os.getcwd()
dir_list = os.listdir(cwd+"/data/data")

# print(len(dir_list))


# find missing medicine

list_of_medicine_in_json = [re.findall("([0-9]+)",dic["bn_url"])[0] for dic in data['url_list']]
list_of_medicine_in_directory= [re.findall("([0-9]+)",i)[0] for i in dir_list]

# print(len(list_of_medicine_in_directory), len(list_of_medicine_in_json), list_of_medicine_in_directory[0:3], list_of_medicine_in_json[0:3])

set2 = set(list_of_medicine_in_directory)
set1= set(list_of_medicine_in_json)

missing = list(sorted(set1 - set2))
added = list(sorted(set2 - set1))
# print('missing:', missing)
# print('added:', added)

# print("=======================================================")
# #checking if every file as indications or other div
# for finding if its content is in bengali or not
# for index,i in enumerate(dir_list):
#     file= cwd+"/data/data/"+i
#     with open(file, encoding="utf-8") as fp:
#         soup = BeautifulSoup(fp, 'html5lib')
#     id_html = soup.find(id="indications")
#     print(index,end='\r')
#     if id_html == None:
#         print(i)

# 31869.html
# 32474.html
# 33506.html
# these have no indications

dst= cwd+"/bangla"
not_bangla= []
for index,i in enumerate(dir_list):
    file= cwd+"/data/data/"+i
    dst = cwd+"/bangla/"+i
    print(index,end='\r')
    with open(file, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, 'html5lib')
    id_indications = soup.find(id="indications")
    if id_indications != None:
        if id_indications.get_text() == "নির্দেশনা":
               shutil.copy2(file, dst)
        else:
            not_bangla.append(i)

print(len(not_bangla))