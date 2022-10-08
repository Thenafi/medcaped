import json

with open('final_data.json','r+') as file:
    data = json.load(file)


for i in data[1:10]:
    print(i['med_id'])
    with open(f'datatest12/{i["med_id"]}.json', 'w') as fp:
        json.dump(data, fp)