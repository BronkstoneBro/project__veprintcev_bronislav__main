from bs4 import BeautifulSoup
import requests

from application.save_to_json import save_to_json


def scrape_product(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    catalog_container = soup.find('div', class_='usedProductNext')
    product_items = catalog_container.find_all('div', class_='itemTitle')
    product_prices = catalog_container.find_all('span', class_='price contractPrice')

    if len(product_items) == len(product_prices):
        return [
            {'name': name.text.strip(), 'price': price.text.strip()}
            for name, price in zip(product_items, product_prices)
        ]
    print("Количество названий и цен не совпадает.")
    return None


url = 'https://autoliga.net.ua/catalog/volkswagen/-tiguan-ii-15-17/-bamper-peredniy/1/'

if data := scrape_product(url):
    folder_path = '../../import_json'
    save_to_json(data, folder_path, url)
else:
    print("Данные не были сохранены из-за ошибки.")
