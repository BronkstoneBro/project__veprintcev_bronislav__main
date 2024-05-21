from typing import List, Optional
from bs4 import BeautifulSoup
import requests
from application.save_to_json import save_to_json


def scrape_product(url: str) -> Optional[List[dict]]:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    catalog_container = soup.find('section', class_='main-catalog')
    if not catalog_container:
        print("Секция с каталогом не найдена.")
        return None

    product_items = catalog_container.find_all('span', class_='catalog-name__text')
    product_elements = catalog_container.find_all('a', class_='catalog-item')

    if len(product_items) != len(product_elements):
        print("Количество названий и элементов не совпадает.")
        return None

    data = []
    for name, element in zip(product_items, product_elements):
        name_text = name.text.strip()
        price_text = element['data-price']
        product_url = element['href']
        product_image = element['data-image']
        data.append({
            'name': name_text,
            'price': price_text,
            'url': product_url,
            'image': product_image
        })
    return data


url = 'https://motopoland.com.ua/catalog/volkswagen-tiguan-ii--bamper-perednyy/1/'
if data := scrape_product(url):
    folder_path = '../../import_json'
    save_to_json(data, folder_path, url)
else:
    print("Данные не были сохранены из-за ошибки.")

