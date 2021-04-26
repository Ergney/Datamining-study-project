import requests
from bs4 import BeautifulSoup
import typing
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from DataBase.database import Database
import datetime

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
page_url = 'https://gb.ru/posts'
response = requests.get(page_url, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
url_list = []
counter = 0
while page_url is not None:

    response = requests.get(page_url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    url_cotent = soup.find('div', attrs={'class': 'post-items-wrapper'}) \
        .find_all('div', attrs={'class': 'post-item event'})
    for url in url_cotent:
        url_list.append(f'https://gb.ru{url.a["href"]}')
        counter += 1
        print(f"#{counter} url={url.a['href']} is ok add in url_list")

    page_url = soup.find('div', attrs={'class': 'row'}) \
        .ul.find_all(['li'], attrs={'class': 'page'})
    for i in page_url:
        page_url = i.find('a', attrs={'rel': 'next'})
        if page_url is not None:
            # if page_url is not None:
            page_url = f'https://gb.ru{page_url["href"]}'


def parce(url_list):
    for url in url_list:
        response = requests.get(url, headers=headers,
                                params={'page-url': 'goal://gb.ru/scroll_90', 'page-ref': url}).text
        soup = BeautifulSoup(response, 'lxml')
        date_time = soup.find('time')['datetime']
        dt = [int(datetime_values) for datetime_values in date_time[0:10].split("-") + date_time[11:16].split(":")]
        data = {
            'post_data': {
                'url': url,
                'title': soup.find('h1', attrs={'class': 'blogpost-title'}).text,
                'image': soup.find('img')["src"],
                'publicationdate': datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4]),
                "countcomments": int(soup.find("comments")["total-comments-count"]),
                "timeread": soup.find("span", attrs={"class": "text-md text-muted m-r-md"}).text,
                "views": int(soup.find("svg", attrs={"class": "icon-views-mini"}).parent.text),
                "commentable_id": int(soup.find("comments")["commentable-id"])

            },
            'author_data': {
                'url': urljoin(url, soup.find('div', attrs={'itemprop': 'author'}).parent.attrs.get('href')),
                'name': soup.find('div', attrs={'itemprop': 'author'}).text
            },
            'tags_data':
                [{'url': urljoin(url, tag.attrs.get('href')), 'name': tag.text} for tag in
                 soup.find_all('a', attrs={'class': 'small'})]

        }
        db.create_post(data)


url_list = set(url_list)

db = Database("sqlite:///gb_blog.db")
parce(url_list)
