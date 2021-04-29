import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-porsche/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
           'accept': '*/*'}  # путем словаря имитируем работу браузера
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagenation = soup.find_all('span', class_='mhide')
    if pagenation:
        return int(pagenation[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items:
        grn_price = item.find('span', class_='size16')
        if grn_price:
            grn_price = grn_price.get_text()
        else:
            grn_price = 'Цены нет'
        cars.append({
            'title': item.find('div', class_='proposition_title').get_text(strip=True),
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'grn_price': grn_price,
            'city': item.find('span', class_='item region').get_text(strip=True)
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в Грн', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['grn_price'], item['city']])


def parse():
    URL = input('Введите url: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_page_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            # cars = get_content(html.text)
        save_file(cars, FILE)
        # print(cars)
        print(f'Получено {len(cars)} автомоблей')
        os.startfile(FILE)
    else:
        print('ERROR')


parse()
