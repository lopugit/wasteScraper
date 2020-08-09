import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.recycling.vic.gov.au/can-i-recycle-this'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

items = soup.find_all('li', class_='accordion__item')
data = {}

#Categories
for i in items:
    category = i.find('span', class_='accordion__title__text').text.strip()
    data[category]={}
    # print(f'category: {category}')

    #Tiles
    tiles = i.find_all('div', class_='tile')
    for t in tiles:
        try:
            name = t.find('div', class_='item__intro__heading').text.strip()
            data[category][name]={}
            # print(f'name: {name}')
        except:
            pass

        try:
            alias = t.find('div', class_='item__intro__subheading').text.strip()
            data[category][name]['alias']=alias
            # print(f'alias: {alias}')
        except:
            pass

        try:
            rec = t.find('span', class_='status__box__heading').text.strip()
            data[category][name]['recyclable']=rec
            # print(f'Recyclable: {rec}')
        except:
            pass

        try:
            adv = t.find('div', class_='status__box__content').text.strip()
            data[category][name]['advice']=adv
            # print(f'Advice: {adv}')
        except:
            pass

        try:
            data[category][name]['tips'] = []
            tips = t.find_all('li')
            for tip in tips:
                tip = tip.text.strip()
                if tip == 'collected by REDcycle.':
                    break
                if tip:
                    data[category][name]['tips'].append(tip)
                    # print(f'tips: {tip}')
        except:
            pass
        # print('=====================================================================')

# print(data)
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)


# Why can’t _____ go in my recycling bin?
# Our current recycling sorting facilities aren’t equipped to sort these softer types of plastic and they can get caught in equipment. This slows down the sorting lines and can even stop the equipment for periods of time.