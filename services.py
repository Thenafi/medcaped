import json
import re

data={}   
with open('data.json','r+') as file:
    file_data = json.load(file)
    data =  file_data

print(len([dic for dic in data['url_list']][19600:22000]))
 