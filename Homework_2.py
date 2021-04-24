import requests
from bs4 import BeautifulSoup
import pymongo


class ParseMagnit:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client['db_lesson2_homework']
        self.collection = db['Magnit']

    def _get_response(self, url):
        r = requests.get(url, headers=self.headers)
        if r.ok:
            r = r.text
            return r
        else:
            print(f'Error! Satus code:{r.status_code}.')

    def _soup(self, url):
        soup = BeautifulSoup(self._get_response(url), 'lxml')
        catalog_name = soup.find('div', attrs={'class': 'сatalogue__main'})
        if catalog_name == None:
            print('Error! Not tag сatalogue__main.')
        else:
            products = catalog_name.find_all('a', recursive=False)
            if products == None:
                print("Error! Catalog products empty.")
            else:
                return products

    def _parse(self, url):
        data = []
        for product in self._soup(url):
            if product.find('div', attrs={'class': 'card-sale__title'}) != None:
                url = product['href']
                try:
                    name_promotion = product.find('div', attrs={'class': 'card-sale__header'}).text
                except AttributeError:
                    name_promotion = None
                try:
                    sale = product.find('div', attrs={'class': 'label'}).text.split()[0]
                except AttributeError:
                    sale = None
                try:
                    picture = product.picture.find('img')['data-src']
                except AttributeError:
                    picture = None
                try:
                    promotion_price = float('.'.join(
                        product.find('div', attrs={'class': 'label__price label__price_old'}).text.split()))
                    not_promotion_price = float('.'.join(
                        product.find('div', attrs={'class': 'label__price_new'}).text.split()))
                except AttributeError:
                    promotion_price = None
                    not_promotion_price = None
                try:
                    name_product = product.find('div', attrs={'class': 'card-sale__title'}).text
                except AttributeError:
                    name_product = None
                try:
                    date = str(product.find('div', attrs={'class': 'card-sale__date'}).text).split()
                    start_promotion = f'{date[1]} {date[2]}'
                    end_promotion = f'{date[4]} {date[5]}'
                except AttributeError:
                    start_promotion = None
                    end_promotion = None
                except IndexError:
                    start_promotion = None
                    end_promotion = None

                tovar = {
                    'url': url,
                    'name_promotion': name_promotion,
                    'name_product': name_product,
                    'sale': sale,
                    'picture': picture,
                    'promotion_price': promotion_price,
                    'not_promotion_price': not_promotion_price,
                    'start_promotion': start_promotion,
                    'end_promotion': end_promotion
                }
                data.append(tovar)
        return data

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)


    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == '__main__':
    url = 'https://magnit.ru/promo/?geo=moskva'
    db_client = pymongo.MongoClient()
    X = ParseMagnit(url, db_client)
    X.run()
#"mongodb://localhost.27017"