"""
- Waste Managers - 
Nikolaj Frey, Mathen Jose, Alvin Zhao
FIT3162
This program scrapes data off https://www.recycling.vic.gov.au/can-i-recycle-this 
"""

import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.recycling.vic.gov.au/can-i-recycle-this'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser') #soup contains the page's HTML content
data = {} #data dictionary which will hold all our items

#Loop over each category
items = soup.find_all('li', class_='accordion__item')
for i in items:
    category = i.find('span', class_='accordion__title__text').text.strip()
    data['category'] = category

    #Loop over each tile item
    tiles = i.find_all('div', class_='tile')
    for t in tiles:
        #Try to fetch a name and add it to our data object
        try:
            name = t.find('div', class_='item__intro__heading').text.strip()
            data['name']=name
        except:
            pass
        #Try to fetch aliases and add it to our data object
        try:
            alias = t.find('div', class_='item__intro__subheading').text.strip()
            data[category][name]['alias']=alias
        except:
            pass
        #Try to fetch recyclability and add it to our data object
        try:
            recyclable = t.find('span', class_='status__box__heading').text.strip()
            data[category][name]['recyclable']=recyclable
        except:
            pass
        #Try to fetch advice and add it to our data object
        try:
            advice = t.find('div', class_='status__box__content').text.strip()
            data[category][name]['advice']=advice
        except:
            pass
        #Try to fetch suggested tips and add it to our data object, skipping REDcycle tips
        try:
            data[category][name]['tips'] = []
            tips = t.find_all('li')
            for tip in tips:
                tip = tip.text.strip()
                if tip == 'collected by REDcycle.':
                    break
                if tip:
                    data[category][name]['tips'].append(tip)       
        except:
            pass
       
# print(data)

# Save data to a json for database querying
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)