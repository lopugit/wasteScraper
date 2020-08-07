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

    try:
        rec = i.find('span', class_='status__box__heading')
        print(f'Recyclable? {rec.text.strip()}')
    except:
        pass

    try:
        adv = i.find('div', class_='status__box__content')
        print(f'Advice: {adv.text.strip()}')
    except:
        pass

    try:
        tips = i.find_all('li')
        for t in tips:
            if t.text.strip() == 'collected by REDcycle.':
                break
            if t:
                print(f'tips: {t.text.strip()}')
    except:
        pass
    print('=====================================================================')