import requests
from pathlib import Path
from urllib.parse import urljoin
import bs4
import pymongo

class MagnitPars:

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client['test_datamining']
        self.collection = db['magnit']

    def _get_response(self, url, *args, **kwargs):
        return requests.get(url, *args, **kwargs)

    def _get_soup(self, url, *args, **kwargs):
        return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, 'lxml')

    def run(self):
        for prouct in self._parse(self.start_url):
            self._save(prouct)

    @property
    def _jesus(self):
        return {
            'product_name': lambda tag: tag.find('div', attrs={'class': 'card-sale__discount'}),
            'url': lambda  tag: urljoin(self.start_url, tag.attrs.get('href', ""))
        }


    def _parse(self, url):
        soup = self._get_soup(url)
        catalog_main = soup.find('div', attrs={'class': 'сatalogue__main'})
        product_tags = catalog_main.find_all('a', recursive=False)
        for product_tag in product_tags:
            product = {}
            for key, funk in self._jesus.items():
                product[key] = funk(product_tag)
            yield product

    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == '__main__':
    db_client = pymongo.MongoClient()
    pars = MagnitPars('https://magnit.ru/promo/?geo=moskva', db_client)
    pars.run()