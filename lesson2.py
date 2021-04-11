import requests
from pathlib import Path
import bs4

url = 'https://magnit.ru/promo/'

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, 'lxml')

#auf = soup.find('div',attrs={'class':'сatalogue__main'})
#z = auf.parent
#t = auf.children
#t1 = list(auf.children)
#q = auf.find_all('a')
#q1 = auf.find_all('a', recursive=False)
#q1.source
#q1[0].text
#q1[0].find('div', attrs={'class': 'card-sale__title'})
#q1[0].find('div', attrs={'class': 'card-sale__title'}).text

#s = 'asfafs'