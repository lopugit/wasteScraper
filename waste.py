import requests
from bs4 import BeautifulSoup

URL = 'https://www.recycling.vic.gov.au/can-i-recycle-this'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup)

results = soup.find(class_='tiles__list')
# print(results.prettify())


items = results.find_all('div', class_='item__intro')
for i in items:
    # print(job_elem.prettify())
    # print()
    try:
        name = i.find('div', class_='item__intro__heading')
        print(f'name: {name.text.strip()}')
    except:
        pass

    try:
        alias = i.find('div', class_='item__intro__subheading')
        print(f'alias: {alias.text.strip()}')
    except:
        pass
    print('=====================================================================')