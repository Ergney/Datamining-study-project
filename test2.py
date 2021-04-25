from pathlib import Path
import requests
import json
import time


class Parse_1:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
    #params = {'categories':[680,732,700,827]}

    def __init__(self, save_path: Path, start_url: str):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            response = requests.get(url, *args, **kwargs, headers=self.headers) #params=self.params
            if response.status_code in (200, 301, 304):
                return response
            time.sleep(1)

    def run(self):
        for product in self._parce(self.start_url):
            product_path = self.save_path.joinpath(f'{product["id"]}')
            self._save(product, product_path)

    def _parce(self, url):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data.get('next')
            for product in data.get('results', []):
                yield product

    def _save(self, data, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        #file_path.write_bytes(json.dumps(data, ensure_ascii=False))

class categorys(Parse_1):
    def __init__(self, category_url, *args, **kwargs):
        self.category_url = category_url
        super().__init__(*args,**kwargs)

    def category_product_get(self):
        resourse = self._get_response((self.category_url))
        data = resourse.json()
        return data

    def go(self):
        for category in self.category_product_get():
            category['product'] = []
            params = f'?categories={category["parent_group_code"]}'
            url = f'{self.start_url}{params}'

            category["product"].extend(list(self._parse(url)))
            file_name = f"{category['parent_group_code']}.json"
            category_path = self.save_path.joinpath(file_name)
            self._save(category, category_path)

def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == '__main__':
    category_url = 'https://5ka.ru/api/v2/categories/'
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_prod = get_save_path('products')
    save_category = get_save_path('category')
    test1 = Parse_1(url, save_prod)
    test2 = categorys(category_url, url, save_category)
    test2.run()


#class categorys(Parse_1):
#    catagory_url= 'https://5ka.ru/api/v2/categories/'
#    url= 'https://5ka.ru/api/v2/special_offers/'
#    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

#    def __init__(self, save_path: Path):
#        self.save_path = save_path


#    def ger_category(self, catagory_url):
#        response: requests.Response = requests.get(catagory_url, headers= headers)
#        catg = response.json()




#class categorys(Parse_1):
#    catagory_url= 'https://5ka.ru/api/v2/categories/'
#    url= 'https://5ka.ru/api/v2/special_offers/'

#    def __init__(self, save_path: Path):
#        self.save_path = save_path

#   def get_category_code(self, catagory_url):
#        response: requests.Response = requests.get(catagory_url, headers=headers)
#        data = response.json()
#        code_category = ['parent_group_code']
#        return code_category


#    def category_get(self):
#        for code in self.category(catagory_url):
#                response = requests.get(url, *args, **kwargs, headers=self.headers, params={'categories': code})  # params=self.params
#                if response.status_code in (200, 301, 304):
#                    return response
#                time.sleep(1)




#        def run(self):
#            for product in self._parce(self.catagory_url):
#                product_path = self.save_path.joinpath(f'{product["parent_group_name"]}')
#                self._save(product, product_path)

#        def _parce(self, url):
#            while catagory_url:
#                response = self._get_response(catagory_url)
#                data: dict = response.json()
#                catagory_url = data.get('next')
#                for product in data.get('results', []):
#                    yield product

#        def _save(self, data, file_path):
#            file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            # file_path.write_bytes(json.dumps(data, ensure_ascii=False))

#def asd(url, headers):
#    response: requests.Response = requests.get(url, headers=headers)

#    for category_code in response.json():
#        cat = category_code['parent_group_code']
#        return cat

#def product(url, headers):
#    resource: requests.Response = requests.get(url, headers=headers, params={'categories':asd(url_category,headers)})
#    data: dict = resource.json()
#    data = json.loads(resource.text)
#    data_product = data['results']

#    print(data)

#product(url, headers)

#headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
# url = 'https://5ka.ru/special_offers/'
#url = 'https://5ka.ru/api/v2/special_offers/'

#response: requests.Response = requests.get(url, headers=headers, params=params)

#file = Path(__file__).parent.joinpath('5a.json')

# file.write_bytes(response.content)
# file.write_text(response.text, encoding='utf-8')

#data = json.loads(response.text)


# data_product = data['results']

# data_product = json.loads(data_product.text)

#def prezent_product(parse_data):
#    data_product = parse_data['results']

#    for i in data_product:
#        print(f'Название товара: {i["name"]}'
#              f'\n      ID товара: {i["id"]}        '
#              f'\n      Стоимость товара без акции: {i["current_prices"]["price_reg__min"]}₽'
#              f'\n      Стоимость товара по акции: {i["current_prices"]["price_promo__min"]}₽'
#              f'\n      Дата начала акции: {i["promo"]["date_begin"]}'
#              f'\n      Дата окончания акции: {i["promo"]["date_end"]}'
#              f'\n________________________________________________________________________________________')


#prezent_product(data)






