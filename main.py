import re
import json
import os
import random
import time
import aiohttp
import asyncio

def randomuseragent():
    with open(os.getcwd() + "/files/user-agents_chrome_browser_96-0.txt") as f:
        io = f.read().splitlines()
        return random.choice(io)

data={}   
with open('data.json','r+') as file:
    file_data = json.load(file)
    data =  file_data

YOUR_API_KEY = "9008aecb-2376-471a-8a02-e2c38e0f745e"


async def main():
    async with aiohttp.ClientSession() as session:
        for i in  [dic for dic in data['url_list']][4900:9900]:
            if i['scraped']==False:
                url = i['bn_url']
                print(url,end='\r')
                medicine_id= re.findall("([0-9]+)",url)[0]
                headers = {"User-Agent": randomuseragent()}
                pokemon_url = f'https://api.rocketscrape.com/?apiKey={YOUR_API_KEY}&url={url}&keep_headers=true'
                async with session.get(pokemon_url,headers=headers) as resp:
                    if resp.status == 200:
                        with open(f"data/{medicine_id}.html", "w+",encoding="utf-8") as file1:
                            file1.writelines(await resp.text())
                        i['scraped']= True
                        with open('data.json', 'w') as fp:
                            json.dump(data, fp)

            else:
                print("Done", end="\r")
                            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())



with open('data.json', 'w') as fp:
    json.dump(data, fp)
