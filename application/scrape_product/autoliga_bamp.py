import re
from typing import Optional, List, Dict
from bs4 import BeautifulSoup
import requests
import logging

import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_product(url: str) -> Optional[List[Dict[str, str]]]:  # Optional - это тип, который позволяет указать,
    # что функция может возвращать значение указанного типа или None. List - это тип, который представляет собой
    # список элементов указанного типа. Dict - это тип, который представляет собой словарь с ключами и значениями
    # указанных типов.
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе к {url}: {e}")
        return None

    try:
        return parse_html(response.text)
    except Exception as e:
        logger.error(f"Ошибка при обработке HTML: {e}")
        return None


def parse_html(html: str) -> Optional[List[Dict[str, str]]]:
    soup = BeautifulSoup(html, 'lxml')
    catalog_container = soup.find('div', class_='content-wrapper-items show-next--white')
    if not catalog_container:
        logger.error("Не удалось найти контейнер с товарами на странице.")
        return None

    product_items = catalog_container.find_all('div', class_='itemTitle')
    product_prices = catalog_container.find_all('span', class_='price')
    product_images = catalog_container.find_all('div', class_='productImgWrapper')
    product_links = catalog_container.find_all('a', class_='js-open-allg-modal')

    return extract_product_data(product_items, product_prices, product_images, product_links)


def extract_product_data(product_items, product_prices, product_images, product_links) -> Optional[
    List[Dict[str, str]]]:
    if len(product_items) != len(product_prices) or len(product_items) != len(product_images) or len(
            product_items) != len(product_links):
        logger.error("Количество названий, цен, изображений и ссылок не совпадает.")
        return None

    data = []
    for name, price_tag, image_tag, link_tag in zip(product_items, product_prices, product_images, product_links):
        price_string = price_tag.text.strip()
        if match := re.search(r'(\d+\s*грн)', price_string):
            price_in_hryvnia = match[1].replace('грн', '').strip()
            product_name = name.text.strip()
            product_url = link_tag['href']
            image_url = image_tag.find('img')['data-src']
            data.append({
                'name': product_name,
                'price': price_in_hryvnia,
                'product_url': product_url,
                'image_url': image_url
            })
        else:
            logger.warning(f"Не удалось извлечь цену для товара: {name.text.strip()}")

    return data


def save_to_json(data: List[Dict[str, str]], folder_path: str, url: str) -> None:
    import os
    file_name = f"{sanitize_filename(url)}.json"
    file_path = os.path.join(folder_path, file_name)

    os.makedirs(folder_path, exist_ok=True)  # os.makedirs() - функция, которая создает директорию и все
    # промежуточные директории, если они не существуют. Параметр exist_ok=True позволяет функции не вызывать
    # исключение, если директория уже существует.

    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Данные успешно сохранены в {file_path}")
    except IOError as e:
        logger.error(f"Ошибка при сохранении данных в файл: {e}")


def sanitize_filename(url: str) -> str:
    if url.startswith('https://'):
        url = url[len('https://'):]
    elif url.startswith('http://'):     # startswith() - метод строки, который возвращает True, если строка
        # начинается с указанного значения, и False в противном случае.
        url = url[len('http://'):]

    return re.sub(r'[\/:*?"<>|]', '_', url)


url = 'https://autoliga.net.ua/catalog/volkswagen/-tiguan-ii-15-17/-bamper-peredniy/1/'

if data := scrape_product(url):
    folder_path = '../../import_json'
    save_to_json(data, folder_path, url)
else:
    logger.error("Данные не были сохранены из-за ошибки.")


# ALL this description for me and my education