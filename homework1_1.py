import requests
import json

url = 'https://5ka.ru/api/v2/special_offers/'
url_category = 'https://5ka.ru/api/v2/categories/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

# r = requests.get(url, headers=headers)
r2 = requests.get(url_category, headers=headers)
categorys_data = json.loads(r2.text)
for category in categorys_data:
    category_code_name = {category['parent_group_code']: category['parent_group_name']}
    code = category['parent_group_code']
    # for code in codes:
    r = requests.get(url, headers=headers, params={'categories': code})
    data = json.loads(r.text)
    # code = str(code)
    f = open(f'{category_code_name[code]}.json', 'a', encoding='utf-8')
    if data['results'] == []:
        f.write("Нет товаров в рамках данной акции")
    else:
        for info_product in data['results']:
            f.write(f'\nНазвание товара: {info_product["name"]}'
                    f'\n      ID товара: {info_product["id"]}        '
                    f'\n      Стоимость товара без акции: {info_product["current_prices"]["price_reg__min"]}₽'
                    f'\n      Стоимость товара по акции: {info_product["current_prices"]["price_promo__min"]}₽'
                    f'\n      Дата начала акции: {info_product["promo"]["date_begin"]}'
                    f'\n      Дата окончания акции: {info_product["promo"]["date_end"]}'
                    f'\n________________________________________________________________________________________')
