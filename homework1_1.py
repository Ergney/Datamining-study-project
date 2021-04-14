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
    f.write("{"f'"Название акции":"{category_code_name[code]}"'"}"
             "\n{"f'"Код акции":"{code}"'"}\n\n")
    if data['results'] == []:
        f.write("{"f'"Товары":"Нет товаров в рамках данной акции"'"}")
    else:
        f.write("\n{"f'"Товары":')
        for info_product in data['results']:

            f.write(
                    "["
                    "\n     {"f'"Название товара": "{info_product["name"]}"'"},"
                    "\n     {"f'"ID товара": "{info_product["id"]}"'"},"
                    "\n     {"f'"Стоимость товара без акции": "{info_product["current_prices"]["price_reg__min"]}₽"'"},"
                    "\n     {"f'"Стоимость товара по акции": "{info_product["current_prices"]["price_promo__min"]}₽"'"},"
                    "\n     {"f'"Дата начала акции": "{info_product["promo"]["date_begin"]}"'"},"
                    "\n     {"f'"Дата окончания акции": "{info_product["promo"]["date_end"]}"'"}"
                    "\n]"
                   )
            if len(data['results'])-1 != (data['results']).index(info_product):
                f.write(",\n\n")
        f.write("\n}")
        f.close()

