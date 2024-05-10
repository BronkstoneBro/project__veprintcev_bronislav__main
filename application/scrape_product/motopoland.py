from bs4 import BeautifulSoup
import requests
from application.save_to_json import save_to_json
def scrape_product(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    catalog_container = soup.find('section', class_='main-catalog')
    product_items = catalog_container.find_all('span', class_='catalog-name__text')
    product_prices = catalog_container.find_all('div', class_='price')

    if len(product_items) == len(product_prices):
        data = []
        for name, price in zip(product_items, product_prices):
            name_text = name.text.strip()
            price_text = price.text.strip().replace('\n', '').replace('купить', '').strip()
            data.append({
                'name': name_text,
                'price': price_text
            })
        return data
    else:
        print("Количество названий и цен не совпадает.")
        return None


url = 'https://motopoland.com.ua/catalog/volkswagen-tiguan-ii--bamper-perednyy/1/'
if data := scrape_product(url):
    folder_path = '../../import_json'
    save_to_json(data, folder_path, url)
else:
    print("Данные не были сохранены из-за ошибки.")
