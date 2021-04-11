import requests
from pathlib import Path
import json

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
# url = 'https://5ka.ru/special_offers/'
url = 'https://5ka.ru/api/v2/special_offers/'

params = {
    'store': None,
    'records_per_page': 12,
    'page': 1,
    'categories': None,
    'ordering': None,
    'price_promo__gte': None,
    'price_promo__lte': None,
    'search': 'Молоко'
}

response: requests.Response = requests.get(url, headers=headers, params=params)

file = Path(__file__).parent.joinpath('5a.json')

# file.write_bytes(response.content)
# file.write_text(response.text, encoding='utf-8')

data = json.loads(response.text)


# data_product = data['results']

# data_product = json.loads(data_product.text)

def prezent_product(parse_data):
    data_product = parse_data['results']

    for i in data_product:
        print(f'Название товара: {i["name"]}'
              f'\n      ID товара: {i["id"]}        '
              f'\n      Стоимость товара без акции: {i["current_prices"]["price_reg__min"]}₽'
              f'\n      Стоимость товара по акции: {i["current_prices"]["price_promo__min"]}₽'
              f'\n      Дата начала акции: {i["promo"]["date_begin"]}'
              f'\n      Дата окончания акции: {i["promo"]["date_end"]}'
              f'\n________________________________________________________________________________________')


prezent_product(data)

# data = data.items()

print(f'\n\n\n')

# f'\n      Дата начала акции: {i["date_begin"]}'
# f'\n      Дата окончания акции: {i["date_end"]}'  f'\n
# f'\n      Скидка: {(({i["current_prices"]["price_reg__min"]}/{i["current_prices"]["price_promo__min"]})/{i["current_prices"]["price_reg__min"]})*100}%'


response1: requests.Response = requests.get(url, headers=headers)

data1 = response1.json()

prezent_product(data1)

params = {
    'store': None,
    'records_per_page': 12,
    'page': 1,
    'categories': None,
    'ordering': None,
    'price_promo__gte': None,
    'price_promo__lte': None,
    'search': 'Молоко'}