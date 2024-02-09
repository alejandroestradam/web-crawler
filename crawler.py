import requests
from bs4 import BeautifulSoup
import json
import os
import re
import aiofiles
import asyncio

def getItems (divItems, condition):
    items = []
    for divItem in divItems:
        url = divItem.find('a').get('href')
        item = dict()
        if "https://www.ebay.com/itm/" in url:
            item["title"] = divItem.select_one('span[role="heading"]').text.strip() if divItem.select_one('span[role="heading"]') else None
            item["condition"] = divItem.select_one('span.SECONDARY_INFO').text.strip() if divItem.select_one('span.SECONDARY_INFO') else None
            item["price"] = divItem.select_one('span.s-item__price').text.replace('\xa0', '').strip() if  divItem.select_one('span.s-item__price') else None
            item["product_url"] = url

            if item["condition"] == condition:
                items.append(item)
    return items

async def writeJSON (item, data_folder):
    item_id = re.search(r'/(\d+)\?', item["product_url"]).group(1)

    if item_id:
        file_path = os.path.join(data_folder, f"{item_id}.json")
        async with aiofiles.open(file_path, mode="w") as outfile:
            await outfile.write(json.dumps(item))

async def main():
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)
    current_url = "https://www.ebay.com/sch/i.html?_ssn=garlandcomputer&_pgn="
    numberPages = 1
    counter = 1
    itemCondition = {
        'New': 'Totalmente nuevo', #Brand New
        'OpenBox': 'Caja Abierta', #Open Box
        'PreOwned': 'De segunda mano' #Pre-Owned
    }
    foundItems = 0
    print('Searching data...')
    while counter <= numberPages:
        response = requests.get(current_url + str(counter))
        soup = BeautifulSoup(response.content, "html.parser")
        divItems = soup.find_all('div', class_='s-item__info')
        
        items = getItems(divItems, itemCondition["PreOwned"])
        foundItems = foundItems + len(items)

        for item in items:
            await writeJSON(item, data_folder)
        counter += 1
    
    if foundItems > 0:
        print(f"{foundItems} items saved")
    else: 
        print('Not Items found')

if __name__ == "__main__":
    asyncio.run(main())