from pathlib import Path
import requests
import json
import time
from bs4 import BeautifulSoup

url_category = 'https://5ka.ru/api/v2/categories/'
url = 'https://5ka.ru/api/v2/special_offers/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

#items = soup.find_all("div", class_='filter__menu_link')


def asd(url, headers):
    response: requests.Response = requests.get(url, headers=headers)

    for category_code in response.json():
        cat = category_code['parent_group_code']
        return cat

def product(url, headers):
    resource: requests.Response = requests.get(url, headers=headers, params={'categories':asd(url_category,headers)})
    #data: dict = resource.json()
    data = json.loads(resource.text)
    #data_product = data['results']

    print(data)

product(url, headers)



